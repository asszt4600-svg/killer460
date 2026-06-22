# subdomain.py
# tool to enumerate subdomains of a target 

import socket
from utils.colors import Color, print_color

def load_wordlist(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f]
    except:
        print_color("\n[!] can't load the wordlist!", Color.RED)
        return []

# نتاكد اذا الدوماين او السوب دومين موجود  
def check_subdomain(domain, subdomain):
    # ندمج الدومين معى السوب دومين 
    full_domain = f"{subdomain}.{domain}"
    try:
        # نسال dns اذا موجود 
        socket.gethostbyname(full_domain)
        return full_domain  # نرجع الدومين بدل ما نطبعه هنا
    except:
        return None  # ما موجود

def start_subdomain():
    print_color("\n[+] Subdomain Enumeration", Color.CYAN)

    # نطلب الدومين 
    domain = input(f"{Color.YELLOW}[?] Enter target domain: {Color.RESET}")   

    # نحمل ملف الورد ليست 
    wordlist = load_wordlist("wordlists/subdomains.txt")

    # لو الملف فاضي مافيه سوب دوماين يوقف 
    if not wordlist:
        print_color("\n[!] No subdomains to check. Please check the wordlist file.", Color.RED)
        return
    
    print_color(f"\n[*] Checking subdomains for {domain}...", Color.YELLOW)
    print_color(f"[*] Loaded {len(wordlist)} words\n", Color.YELLOW)

    # قائمة نحفظ فيها السب دومينات اللي نلاقيها
    found = []

    # نمر على كل كلمة في الورد ليست ونفحصها
    for subdomain in wordlist:
        result = check_subdomain(domain, subdomain)
        if result:
            found.append(result)

    # نطبع النتائج في النهاية
    print_color("\n[+] Scan finished!", Color.GREEN)
    
    if found:
        print_color(f"[*] Found {len(found)} subdomains:\n", Color.YELLOW)
        for sub in found:
            print_color(f"  ✅ {sub}", Color.GREEN)
    else:
        print_color("[!] No subdomains found.", Color.RED)