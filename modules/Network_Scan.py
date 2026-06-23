# network_scan.py
# اداة فحص الاجهزة المتصلة على نفس الشبكة
 
import socket
import threading
import subprocess
import platform
from utils.colors import Color, print_color
from modules.port_scanner import PORT_NAMES
 
# قائمة نحفظ فيها الأجهزة المتصلة
active_hosts = []
 
# دالة تتحقق اذا البورت مفتوح وترجع True او False
def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False
 
# دالة تتحقق اذا الجهاز موجود على الشبكة
def check_host(ip):
    try:
        # نحدد نظام التشغيل تلقائياً
        if platform.system() == "Windows":
            cmd = ["ping", "-n", "1", "-w", "500", ip]
        else:
            # Linux / Mac
            cmd = ["ping", "-c", "1", "-W", "1", ip]
 
        result = subprocess.run(
            cmd,
            capture_output=True
        )
        # لو رد = موجود
        if result.returncode == 0:
            active_hosts.append(ip)
    except:
        pass
 
def run_network_scan(base_ip):
    threads = []
    # نجرب فحص على كل الاي بيات من 1 الى 254
    for i in range(1, 255):
        ip = f"{base_ip}.{i}"
        t = threading.Thread(target=check_host, args=(ip,))
        threads.append(t)
        t.start()
 
    for t in threads:
        t.join()
 
def start_network_scan():
    global active_hosts
    active_hosts = []
 
    print_color("\n[+] Network Scanner", Color.CYAN)
 
    # نطلب من المستخدم يدخل base ip
    base_ip = input(f"{Color.YELLOW}[?] Enter base IP: {Color.RESET}")
 
    print_color(f"\n[*] Scanning {base_ip}.0/24...", Color.YELLOW)
 
    # نشغل الفحص
    run_network_scan(base_ip)
 
    # نطبع النتيجه
    if active_hosts:
        print_color(f"\n[+] Found {len(active_hosts)} active hosts:\n", Color.GREEN)
        for host in sorted(active_hosts):
            print_color(f"  ✅ {host}", Color.GREEN)
            # نفحص البورتات لكل جهاز موجود
            for port, name in PORT_NAMES.items():
                if check_port(host, port):
                    print_color(f"     └── Port {port} ({name})", Color.CYAN)
    else:
        print_color("\n[!] No active hosts found.", Color.RED)
 