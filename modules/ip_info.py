# ip informations 
# tool to get informations about any ip address .

import requests
from utils.colors import Color, print_color
from modules.port_scanner import validate_ip  # نختصر الوقت ونحط البورت سكانر هنا 

def get_ip_info():
    print_color("\n[+] IP Info", Color.CYAN)
    
    # نطلب من المستخدم الـ IP
    ip = input(f"{Color.YELLOW}[?] Enter IP: {Color.RESET}")
    
    # نتحقق من الـ IP
    if not validate_ip(ip):
        print_color("\n[!] IP غلط! مثال: 192.168.1.1", Color.RED)
        return
    
    print_color(f"\n[*] fatching ip info {ip}...", Color.YELLOW)
    
    try:
        # نرسل طلب للـ API
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        
        if data["status"] == "success":
            print_color("\n╔══════════════════════════════╗", Color.CYAN)
            print_color(f"  🌍 Country:   {data['country']}", Color.GREEN)
            print_color(f"  🏙️  City:      {data['city']}", Color.GREEN)
            print_color(f"  📡 ISP:       {data['isp']}", Color.GREEN)
            print_color(f"  🔢 ASN:       {data['as']}", Color.GREEN)
            print_color(f"  🕐 Timezone:  {data['timezone']}", Color.GREEN)
            print_color(f"  📍 Latitude:  {data['lat']}", Color.GREEN)
            print_color(f"  📍 Longitude: {data['lon']}", Color.GREEN)
            print_color("╚══════════════════════════════╝", Color.CYAN)
        else:
            print_color("\n[!] ما قدرنا نجيب المعلومات!", Color.RED)
    
    except:
        print_color("\n[!] في مشكلة بالاتصال بالإنترنت!", Color.RED)