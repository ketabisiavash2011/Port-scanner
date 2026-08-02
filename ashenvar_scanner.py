#!/usr/bin/env python3
"""
ASHENVAR Port Scanner
A simple multithreaded TCP port scanner for educational / authorized security testing.

⚠️ Only scan hosts you own or have explicit written permission to test.
Unauthorized scanning may be illegal in your jurisdiction.
"""

import socket
import sys
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

BANNER = r"""
    _    ____  _   _ _____ _   ___     ___    ____
   / \  / ___|| | | | ____| \ | \ \   / / \  |  _ \
  / _ \ \___ \| |_| |  _| |  \| |\ \ / / _ \ | |_) |
 / ___ \ ___) |  _  | |___| |\  | \ V / ___ \|  _ <
/_/   \_\____/|_| |_|_____|_| \_|  \_/_/   \_\_| \_\

              P O R T   S C A N N E R
          made by ASHENVAR | cybersecurity toolkit
"""

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Alt"
}


def scan_port(target, port, timeout=1.0):
    """Try to connect to a single port. Returns (port, is_open, banner)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                banner = ""
                try:
                    s.settimeout(0.5)
                    banner = s.recv(1024).decode(errors="ignore").strip()
                except Exception:
                    pass
                return port, True, banner
    except socket.error:
        pass
    return port, False, ""


def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[!] Could not resolve hostname: {target}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="ASHENVAR Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1024",
                         help="Port range, e.g. 1-1024 or 80,443,8080 (default: 1-1024)")
    parser.add_argument("-t", "--threads", type=int, default=100,
                         help="Number of concurrent threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=1.0,
                         help="Socket timeout in seconds (default: 1.0)")
    args = parser.parse_args()

    print(BANNER)

    ip = resolve_target(args.target)

    # Parse port list
    ports = []
    if "," in args.ports:
        ports = [int(p) for p in args.ports.split(",")]
    elif "-" in args.ports:
        start, end = map(int, args.ports.split("-"))
        ports = list(range(start, end + 1))
    else:
        ports = [int(args.ports)]

    print(f"[*] Target        : {args.target} ({ip})")
    print(f"[*] Port range    : {args.ports}  ({len(ports)} ports)")
    print(f"[*] Threads       : {args.threads}")
    print(f"[*] Started at    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 55)

    open_ports = []
    start_time = datetime.now()

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_port, ip, p, args.timeout): p for p in ports}
        for future in as_completed(futures):
            port, is_open, banner = future.result()
            if is_open:
                service = COMMON_PORTS.get(port, "unknown")
                extra = f" | banner: {banner[:50]}" if banner else ""
                print(f"[+] Port {port:<6} OPEN   ({service}){extra}")
                open_ports.append(port)

    elapsed = (datetime.now() - start_time).total_seconds()
    open_ports.sort()

    print("-" * 55)
    print(f"[*] Scan finished in {elapsed:.2f} seconds")
    print(f"[*] Open ports ({len(open_ports)}): {open_ports if open_ports else 'none found'}")


if __name__ == "__main__":
    main()
