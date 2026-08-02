ASHENVAR Port Scanner 🔍
A simple, fast, multithreaded TCP port scanner written in Python — built as part of my cybersecurity learning journey.
Code
✨ Features
🚀 Multithreaded scanning for speed
🎯 Scan a single port, a list, or a range
🏷️ Identifies common services (SSH, HTTP, FTP, RDP, etc.)
📡 Grabs service banners when available
⚙️ Configurable thread count and timeout
📊 Clean, readable terminal output with scan summary
🛠️ Requirements
Python 3.7+
No external dependencies (uses only the standard library)
📦 Installation
Bash
🚀 Usage
Scan the default port range (1–1024) on a target:
Bash
Scan a specific port range:
Bash
Scan specific ports:
Bash
Adjust thread count and timeout:
Bash
Options
Flag
Description
Default
target
IP address or hostname to scan
required
-p, --ports
Port range (1-1024) or list (22,80,443)
1-1024
-t, --threads
Number of concurrent threads
100
--timeout
Socket timeout in seconds
1.0
📸 Example Output
Code
⚠️ Legal Disclaimer
This tool is intended strictly for educational purposes and authorized security testing. Only scan systems you own or have explicit written permission to test. Unauthorized port scanning may violate laws in your country. The author is not responsible for any misuse of this tool.
A safe target to practice on: scanme.nmap.org, which is publicly offered by the Nmap project for testing purposes.
🧭 Roadmap
[ ] Add UDP scanning support
[ ] Export results to JSON/CSV
[ ] Add OS fingerprinting
[ ] Add async version using asyncio
📄 License
MIT License — feel free to use and modify.
Built by ASHENVAR as part of a cybersecurity + Python learning path.
