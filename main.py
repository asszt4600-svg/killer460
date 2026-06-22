# multi_tools in one frame work !
# main.py
# من هنا تبدا متعة الحياة بالنسبه لكيلر
# من هنا راح نبدا في تصميم الشكل (gui) الخاص بكيلر

import os
import time
import sys
from utils.colors import Color, print_color
from modules.port_scanner import start_scan
from modules.ip_info import get_ip_info
from modules.subdomain import start_subdomain
from modules.Network_Scan import start_network_scan
from modules.banner_grab import start_banner_grab
from modules.hash import start_hash
from modules.Ddos_Attack import start_ddos

# دالة الانيميشن - تطبع الحروف وحدة وحدة
def animate_print(text, color, delay=0.02):
    print(color, end="")
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print(Color.RESET)

def banner():
    print_color("""
██╗  ██╗██╗██╗     ██╗     ███████╗██████╗     ██╗  ██╗ ██████╗  ██████╗
██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗    ██║  ██║██╔════╝ ██╔═████╗
█████╔╝ ██║██║     ██║     █████╗  ██████╔╝    ███████║███████╗ ██║██╔██║
██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗    ╚════██║██╔══██║ ████╔╝██║
██║  ██╗██║███████╗███████╗███████╗██║  ██║         ██║╚██████╔╝╚██████╔╝
╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝         ╚═╝ ╚═════╝  ╚═════╝
    """, Color.CYAN)
    animate_print("[ Hacking Framework v1.0  ]", Color.RED)
    animate_print("[ Developed by: killer460 ]\n", Color.YELLOW)

def menu():
    animate_print("\n╔══════════════════╗", Color.CYAN, delay=0.01)
    animate_print("  [1] Port Scanner", Color.GREEN, delay=0.002)
    animate_print("  [2] IP Info", Color.GREEN, delay=0.002)
    animate_print("  [3] Network Scan", Color.GREEN, delay=0.002)
    animate_print("  [4] Subdomain Enum", Color.GREEN, delay=0.002)
    animate_print("  [5] Banner Grab", Color.GREEN, delay=0.002)
    animate_print("  [6] Hash Tools", Color.GREEN, delay=0.002)
    animate_print("  [7] DDOS Attack", Color.GREEN, delay=0.002)
    animate_print("  [0] Exit", Color.RED, delay=0.002)
    animate_print("╚══════════════════╝", Color.CYAN, delay=0.01)

def main():
    banner()

    prompt = f"{Color.CYAN}$ {Color.RESET}"

    while True:
        choice = input(prompt)

        if choice == "methods":
            os.system("cls" if os.name == "nt" else "clear")
            banner()
            menu()
            prompt = f"{Color.CYAN}killer460 $ {Color.RESET}"
            continue

        elif choice == "1":
            start_scan()

        elif choice == "2":
            get_ip_info()

        elif choice == "3":
            start_network_scan()

        elif choice == "4":
            start_subdomain()

        elif choice == "5":
            start_banner_grab()

        elif choice == "6":
            start_hash()

        elif choice == "7":
            start_ddos()

        elif choice == "0" or choice == "exit":
            animate_print("\n[+] Exiting... get out hahah !\n", Color.RED)
            break

        elif choice in ["cls", "clear"]:
            os.system("cls" if os.name == "nt" else "clear")
            banner()

        else:
            print_color("\n[!] invalid choice ! ", Color.RED)

if __name__ == "__main__":
    main()