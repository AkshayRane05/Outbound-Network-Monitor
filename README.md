# Outbound Connection Monitor

A lightweight, high-performance Python utility for monitoring outbound network connections from your system in real-time. This tool helps identify potentially suspicious connections by flagging domains based on customizable patterns.

![Connection Monitor Screenshot](https://raw.githubusercontent.com/AkshayRane05/outbound-connection-monitor/main/screenshot.png)

## Features

- **Real-time Connection Monitoring**: Track all established outbound network connections
- **Smart DNS Resolution**: Efficiently resolves IP addresses to domain names
- **Suspicious Connection Detection**: Flags potentially suspicious domains based on configurable patterns
- **Performance Optimized**: Uses caching and parallel processing for minimal system impact
- **Process Identification**: Shows which processes are making network connections
- **Simple Interface**: Clear, organized terminal output with refresh capability

## Requirements

- Python 3.6+
- psutil library
- Administrator/root privileges (to access process information)

## Installation

### Option 1: System-wide installation (not recommended for Kali Linux)

1. Clone this repository:

   ```bash
   git clone https://github.com/username/outbound-connection-monitor.git
   cd outbound-connection-monitor
   ```

2. Install dependencies:

   ```bash
   # For most systems
   pip install psutil

   # For Debian/Ubuntu
   sudo apt install python3-psutil
   ```

### Option 2: Using a virtual environment (recommended, especially for Kali Linux)

1. Clone the repository:

   ```bash
   git clone https://github.com/username/outbound-connection-monitor.git
   cd outbound-connection-monitor
   ```

2. Make sure you have the virtual environment package:

   ```bash
   # For Kali Linux
   sudo apt install python3-venv
   ```

3. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies in the virtual environment:
   ```bash
   pip install psutil
   ```

### Special notes for Kali Linux

Kali Linux implements PEP 668, which prevents direct pip installations to the system Python. You have three options:

1. Install from apt (if available):

   ```bash
   sudo apt install python3-psutil
   ```

2. Use a virtual environment as shown above (recommended)

3. Use pipx for isolated application installation:
   ```bash
   # Install pipx if not already installed
   sudo apt install pipx
   # Install the application in an isolated environment
   pipx install psutil
   ```

## Usage

Run the script with administrator/root privileges (required to see all system processes):

### Windows

```bash
# Run Command Prompt as Administrator, then:
python connection_monitor.py
```

### Linux/macOS

```bash
sudo python3 connection_monitor.py
```

### Kali Linux with virtual environment

```bash
# If using a virtual environment, activate it first:
source venv/bin/activate

# Then run with sudo (sudo will use system Python by default, so we specify the path):
sudo venv/bin/python connection_monitor.py
```

### Platform-Specific Notes

- **Windows**: Some process information may be limited unless running as Administrator
- **Linux**: Use `sudo` to ensure access to all process information
- **Kali Linux**: Follow the virtual environment instructions above to avoid PEP 668 errors
- **macOS**: Use `sudo` and be aware that additional permissions may be required due to security features

- Press `Enter` to refresh the connections list
- Press `Ctrl+C` to exit the program

## Output Explanation

The monitor displays the following information for each connection:

| Column     | Description                                       |
| ---------- | ------------------------------------------------- |
| PID        | Process ID                                        |
| Process    | Name of the process making the connection         |
| Remote IP  | IP address of the remote endpoint                 |
| Port       | Port number on the remote endpoint                |
| Domain     | Resolved domain name (if available)               |
| Suspicious | ✅ marker indicates potentially suspicious domain |

## Customization

### Modifying Suspicious Patterns

Edit the `SUSPICIOUS_PATTERNS` list in the script to adjust which domain patterns are flagged as suspicious:

```python
SUSPICIOUS_PATTERNS = [
    "unknown", "tor", "crypt",
    "xyz", "top", "onion", r"\d{5,}", "dyn", "no-ip"
]
```

### Adjusting Thread Pool Size

For systems with varying resources, you can adjust the number of parallel DNS lookups:

```python
# Change max_workers to suit your system
with ThreadPoolExecutor(max_workers=30) as executor:
```

## Performance

The monitor is designed to be efficient by:

- Caching DNS resolutions to avoid repeated lookups
- Caching process information to reduce system calls
- Using parallel DNS resolution with ThreadPoolExecutor
- Only resolving new connections since the last scan
- Tracking and displaying execution time for performance monitoring

Performance may vary across operating systems due to differences in how network information is exposed by the OS. Windows typically processes network information differently than Unix-based systems.

## Use Cases

- System monitoring and administration
- Network security analysis
- Detecting unwanted connections
- Educational tool for understanding network traffic
- Troubleshooting network-related issues

## License

MIT License - See LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgments

- Thanks to the psutil developers for their excellent library
- Inspired by various network monitoring tools and security best practices
