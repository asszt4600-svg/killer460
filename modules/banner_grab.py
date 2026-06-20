# banner_grab.py
# اداة جلب معلومات السيرفس من البورت

import socket
from utils.colors import Color, print_color

# دالة تجلب البانر من البورت
def grab_banner(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # تايم اوت ثانيتين عشان ما ننتظر كثير
        sock.settimeout(2)
        # نتصل بالبورت
        sock.connect((ip, port))
        # نرسل طلب عشان السيرفس يرد بمعلوماته
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        # نستقبل الرد - 1024 يعني اقصى عدد bytes نستقبله
        banner = sock.recv(1024).decode("utf-8", errors="ignore")
        sock.close()
        return banner.strip()
    except:
        return None

# الدالة الرئيسية
def start_banner_grab():
    print_color("\n[+] Banner Grab", Color.CYAN)

    # نطلب الـ IP
    ip = input(f"{Color.YELLOW}[?] Enter target IP: {Color.RESET}")

    # نطلب البورت
    port = int(input(f"{Color.YELLOW}[?] Enter port: {Color.RESET}"))

    print_color(f"\n[*] Grabbing banner from {ip}:{port}...", Color.YELLOW)

    # نجلب البانر
    banner = grab_banner(ip, port)

    # نطبع النتيجة
    if banner:
        print_color("\n[+] Banner found:\n", Color.GREEN)
        print_color(f"{banner}", Color.CYAN)
    else:
        print_color("\n[!] No banner found.", Color.RED)