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

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/username/outbound-connection-monitor.git
   cd outbound-connection-monitor
   ```

2. Install dependencies:
   ```bash
   pip install psutil
   ```

## Usage

Run the script with administrator/root privileges (required to see all system processes):

```bash
# On Windows
python connection_monitor.py

# On Linux/macOS
sudo python3 connection_monitor.py
```

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
