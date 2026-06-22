# subdomain.py
# tool to enumerate subdomains of a target 
import socket
import threading
import platform
from utils.colors import Color, print_color

def load_wordlist(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f]
    except:
        print_color("\n[!] can't load the wordlist!", Color.RED)
        return []

# نتاكد اذا الدوماين او السوب دومين موجود  
def check_subdomain(domain, subdomain, found, lock):
    # ندمج الدومين مع السوب دومين 
    full_domain = f"{subdomain}.{domain}"
    try:
        # نسال dns اذا موجود 
        socket.setdefaulttimeout(1)
        socket.gethostbyname(full_domain)
        # نضيف للقائمة بأمان ونطبع فوراً
        with lock:
            found.append(full_domain)
            print_color(f"  ✅ {full_domain}", Color.GREEN)
    except:
        pass

def start_subdomain():
    print_color("\n[+] Subdomain Enumeration", Color.CYAN)
    
    # نطلب الدومين 
    domain = input(f"{Color.YELLOW}[?] Enter target domain: {Color.RESET}")
    
    threads_count = 75

    # نكشف النظام ونختار الورد ليست المناسبة
    if platform.system() == "Windows":
        wordlist_path = "wordlists/subdomains.txt"
    else:
        wordlist_path = "/usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt"

    # نحمل الورد ليست
    wordlist = load_wordlist(wordlist_path)
    
    # لو الملف فاضي نوقف
    if not wordlist:
        print_color("\n[!] No subdomains to check. Please check the wordlist file.", Color.RED)
        return
    
    print_color(f"\n[*] Checking subdomains for {domain}...", Color.YELLOW)
    print_color(f"[*] Loaded {len(wordlist)} words", Color.YELLOW)
    print_color(f"[*] Press Ctrl+C to stop anytime\n", Color.YELLOW)
    
    # قائمة نحفظ فيها السب دومينات اللي نلاقيها
    found = []
    lock = threading.Lock()
    threads = []

    try:
        # نمر على كل كلمة في الورد ليست ونفحصها
        for subdomain in wordlist:
            # ننتظر لو الثريدز وصلت للحد الأقصى
            while threading.active_count() > threads_count:
                pass
            t = threading.Thread(target=check_subdomain, args=(domain, subdomain, found, lock))
            t.daemon = True
            t.start()
            threads.append(t)

        # ننتظر كل الثريدز تخلص
        for t in threads:
            t.join()

    except KeyboardInterrupt:
        # المستخدم ضغط Ctrl+C
        print_color("\n\n[!] Scan stopped by user", Color.RED)

    # نطبع العدد الكلي في النهاية
    print_color("\n[+] Scan finished!", Color.GREEN)
    print_color(f"[*] Found {len(found)} subdomains", Color.YELLOW)