# File: port_scanner.py

import socket
import concurrent.futures
import datetime

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def get_service(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    sock.close()
    return port, result

def scan_ports(target, show_closed=False):
    open_ports = []
    closed_ports = []

    print(f"\n{CYAN}{BOLD}[*] Starting full port scan on {target}{RESET}")
    print(f"{CYAN}[*] Scan started at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{CYAN}[*] Scanning all 65535 ports...{RESET}\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=500) as executor:
        futures = []
        for port in range(1, 65536):
            futures.append(executor.submit(scan_port, target, port))

        for future in concurrent.futures.as_completed(futures):
            port, result = future.result()
            if result == 0:
                service = get_service(port)
                open_ports.append((port, service))
                print(f"  {GREEN}{BOLD}[+] Port {port:<6} is OPEN   --> Service: {service}{RESET}")
            else:
                closed_ports.append(port)
                if show_closed:
                    print(f"  {RED}[-] Port {port:<6} is CLOSED{RESET}")

    return open_ports, closed_ports

def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(f"{RED}[-] Could not resolve hostname: {target}{RESET}")
        return None

if __name__ == "__main__":
    target = input(f"{CYAN}Enter the target host: {RESET}")
    show_closed = input(f"{YELLOW}Show closed ports? (y/n): {RESET}").strip().lower() == 'y'

    ip = resolve_target(target)

    if ip:
        print(f"{CYAN}[*] Target: {target} resolved to {ip}{RESET}")
        open_ports, closed_ports = scan_ports(ip, show_closed)

        print(f"\n{CYAN}[*] Scan completed at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")

        if open_ports:
            print(f"\n{BOLD}{GREEN}[*] Summary - Open ports found on {target} ({ip}):{RESET}")
            print(f"  {BOLD}{'Port':<10} {'Service':<20}{RESET}")
            print(f"  {'-'*30}")
            for port, service in sorted(open_ports):
                print(f"  {GREEN}{port:<10} {service:<20}{RESET}")
        else:
            print(f"{RED}[-] No open ports found.{RESET}")

        if show_closed:
            print(f"\n{BOLD}{RED}[*] Summary - Closed ports on {target} ({ip}):{RESET}")
            print(f"  {RED}Total closed ports: {len(closed_ports)}{RESET}")
