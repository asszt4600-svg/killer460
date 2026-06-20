# port scanner 
# tool to scan ports of a target

import socket 
import threading
from utils.colors import Color, print_color

open_ports = []

# قائمة كاملة باسماء البورتات
PORT_NAMES = {
    20: "FTP-Data", 21: "FTP", 22: "SSH", 23: "Telnet",
    25: "SMTP", 53: "DNS", 67: "DHCP", 68: "DHCP",
    69: "TFTP", 80: "HTTP", 110: "POP3", 119: "NNTP",
    123: "NTP", 135: "RPC", 137: "NetBIOS", 138: "NetBIOS",
    139: "NetBIOS", 143: "IMAP", 161: "SNMP", 194: "IRC",
    389: "LDAP", 443: "HTTPS", 445: "SMB", 465: "SMTPS",
    514: "Syslog", 515: "LPD", 554: "RTSP", 587: "SMTP",
    631: "IPP", 636: "LDAPS", 993: "IMAPS", 995: "POP3S",
    1080: "SOCKS", 1194: "OpenVPN", 1433: "MSSQL",
    1521: "Oracle", 1723: "PPTP", 2049: "NFS",
    2082: "cPanel", 2083: "cPanel-SSL", 2222: "SSH-Alt",
    3306: "MySQL", 3389: "RDP", 4444: "Metasploit",
    5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
    6667: "IRC", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    8888: "HTTP-Alt", 9200: "Elasticsearch", 27017: "MongoDB"
}

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except:
        pass

def stealth_scan(ip, start_port, end_port):
    try:
        from scapy.all import IP, TCP, sr1, conf
        conf.verb = 0  # نوقف output الـ scapy

        print_color("\n[!] Stealth Scan wanna permission  Administrator!", Color.YELLOW)

        for port in range(start_port, end_port + 1):
            # نرسل SYN packet بس
            pkt = IP(dst=ip)/TCP(dport=port, flags="S")
            resp = sr1(pkt, timeout=1)

            if resp and resp.haslayer(TCP):
                # لو رد بـ SYN/ACK = مفتوح
                if resp[TCP].flags == 0x12:
                    open_ports.append(port)
                    name = PORT_NAMES.get(port, "Unknown")
                    print_color(f" ✅ Port {port} ({name}) is open", Color.GREEN)
    except Exception as e:
        print_color(f"\n[!] wrong: {e}", Color.RED)

def run_scan(ip, start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(ip, port))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

def validate_ip(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        if not 0 <= int(part) <= 255:
            return False
    return True

def start_scan():
    global open_ports
    open_ports = []

    print_color("\n[+] Port Scanner", Color.CYAN)

    ip = input(f"{Color.YELLOW}[?] Enter target IP: {Color.RESET}")

    if not validate_ip(ip):
        print_color("\n[!] Invalid IP address, please enter a valid IP.", Color.RED)
        return

    # نعطيه 3 خيارات
    print_color("\n[1] Scan range of ports", Color.GREEN)
    print_color("[2] Scan all ports", Color.GREEN)
    print_color("[3] Stealth Scan (requires Admin)", Color.YELLOW)
    choice = input(f"\n{Color.YELLOW}[?] Select option: {Color.RESET}")

    if choice == "1":
        start_port = int(input(f"{Color.YELLOW}[?] Enter start port: {Color.RESET}"))
        end_port = int(input(f"{Color.YELLOW}[?] Enter end port: {Color.RESET}"))
        print_color(f"\n[*] Scanning {ip}...", Color.YELLOW)
        run_scan(ip, start_port, end_port)
    elif choice == "2":
        start_port = 1
        end_port = 65535
        print_color(f"\n[*] Scanning {ip}...", Color.YELLOW)
        run_scan(ip, start_port, end_port)
    elif choice == "3":
        start_port = int(input(f"{Color.YELLOW}[?] Enter start port: {Color.RESET}"))
        end_port = int(input(f"{Color.YELLOW}[?] Enter end port: {Color.RESET}"))
        print_color(f"\n[*] Stealth Scanning {ip}...", Color.YELLOW)
        stealth_scan(ip, start_port, end_port)
    else:
        print_color("\n[!] Invalid choice.", Color.RED)
        return

    # نطبع النتائج
    if open_ports:
        print_color(f"\n[+] Open Ports Found:", Color.GREEN)
        for port in sorted(open_ports):
            name = PORT_NAMES.get(port, "Unknown")
            print_color(f" ✅ Port {port} ({name}) is open", Color.GREEN)
    else:
        print_color("\n[!] No open ports found.", Color.RED)