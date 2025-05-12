import psutil
import socket
from datetime import datetime
import re
import time
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

# Suspicious keywords or patterns
SUSPICIOUS_PATTERNS = ["unknown", "tor", "crypt",
                       "xyz", "top", "onion", r"\d{5,}", "dyn", "no-ip"]

# DNS cache to avoid repeated lookups
dns_cache = {}
# Process name cache
proc_cache = {}
# Last seen connections to avoid redoing work
last_connections = set()


def resolve_domain(ip):
    # Check cache first
    if ip in dns_cache:
        return dns_cache[ip]

    try:
        domain = socket.gethostbyaddr(ip)[0]
        # Cache the result
        dns_cache[ip] = domain
        return domain
    except socket.herror:
        dns_cache[ip] = "Unknown"
        return "Unknown"
    except Exception:
        dns_cache[ip] = "Error"
        return "Error"


def looks_suspicious(domain):
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, domain, re.IGNORECASE):
            return True
    return False


def get_process_name(pid):
    if pid in proc_cache:
        return proc_cache[pid]

    try:
        name = psutil.Process(pid).name()
        proc_cache[pid] = name
        return name
    except:
        proc_cache[pid] = "N/A"
        return "N/A"


def batch_resolve_domains(connections):
    conn_by_ip = defaultdict(list)

    # Group connections by IP to avoid redundant lookups
    for conn in connections:
        if conn.raddr:
            remote_ip = conn.raddr.ip
            conn_by_ip[remote_ip].append(conn)

    # Use thread pool for parallel DNS lookups
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Submit DNS lookups for all unique IPs
        future_to_ip = {executor.submit(
            resolve_domain, ip): ip for ip in conn_by_ip.keys()}

        # Process results as they complete
        for future in future_to_ip:
            future.result()  # This ensures all DNS lookups complete


def analyze_connections():
    global last_connections

    print(
        f"\n[+] Analyzing Connections @ {datetime.now().strftime('%H:%M:%S')}")
    print("{:<6} {:<25} {:<18} {:<6} {:<50} {}".format(
        "PID", "Process", "Remote IP", "Port", "Domain", "⚠️  Suspicious?"
    ) + "\n")

    # Get all established connections
    connections = [
        conn for conn in psutil.net_connections(kind='inet')
        if conn.status == 'ESTABLISHED' and conn.raddr
    ]

    # Create a set of current connections for comparison
    current_connections = {
        (conn.pid, conn.raddr.ip, conn.raddr.port) for conn in connections
    }

    # Find new connections that weren't in the last scan
    new_connections = current_connections - last_connections

    # Only perform DNS lookups on new connections
    new_conns = [
        conn for conn in connections
        if (conn.pid, conn.raddr.ip, conn.raddr.port) in new_connections
    ]

    # Batch resolve domains for new connections
    batch_resolve_domains(new_conns)

    # Update last_connections for next iteration
    last_connections = current_connections

    # Sort connections by PID for more organized output
    connections.sort(key=lambda c: c.pid)

    # Display the connections
    for conn in connections:
        pid = conn.pid
        proc_name = get_process_name(pid)
        remote_ip = conn.raddr.ip
        port = conn.raddr.port
        domain = dns_cache.get(remote_ip, "Unknown")
        flagged = "       ✅" if looks_suspicious(domain) else ""

        print("{:<6} {:<25} {:<18} {:<6} {:<50} {}".format(
            pid, proc_name, remote_ip, port, domain, flagged
        ))


if __name__ == "__main__":
    try:
        while True:
            start_time = time.time()
            analyze_connections()
            end_time = time.time()
            print(
                f"\n[i] Scan completed in {end_time - start_time:.2f} seconds")
            input("\n[Enter] to refresh | Ctrl+C to exit...")
    except KeyboardInterrupt:
        print("\n[!] Stopped.")
