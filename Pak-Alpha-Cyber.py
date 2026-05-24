# Is script ka mukammal maqsad "Target Network Reconnaissance" 
# hai. Yeh check karti hai ke aapka apna network kahan se connect
# hai, kisi target domain ke kitne mazeed raste (subdomains) hain,
# aur un subdomains ya servers ke kaun se ports open hain. Yeh cyber
# security testing ka sabse pehla aur zaroori buniyadi framework hota
# hai.Agar aap is script ke andar mazeed koi features jaise
# Banner Grabbing (open ports par chalne wale software ka 
# version nikalna) ya Directory Buster add karna chahte hain, 
# to mujhe batayein!

import os
import sys
import time
import socket
import threading
import json
import urllib.request
from queue import Queue

# Terminal Colors
R = "\033[1;91m" # Red
G = "\033[1;92m" # Green
Y = "\033[1;93m" # Yellow
C = "\033[1;96m" # Cyan
W = "\033[0m"    # White

print_lock = threading.Lock()

def clear_screen():
    # Windows par 'cls' aur Linux/Termux par 'clear' chalayega
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear_screen()
    print(f"{Y}>>  WELCOME TO SHADOW DOMAIN  <<{W}")
    print(f"{R} ☠️  ᴀʟᴘʜᴀ-ᴄʏʙᴇʀ-ᴄᴏᴍᴍᴀɴᴅᴏ  ☠️{W}")
    print(f"{C}="*45 + f"{W}")
    print(f"{G}[+] Platform : {sys.platform}")
    print(f"[+] Python   : {sys.version.split()[0]}")
    print(f"[+] Status   : System Fully Operational{W}")
    print(f"{C}="*45 + f"{W}\n")

def get_ip_info():
    print(f"{C}[*] Fetching Network and IP Information...{W}\n")
    try:
        # Local IP Detection
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(f"{G}[✔] Local IP Address  : {local_ip}{W}")
        
        # Public IP & Location Info via Live API
        req = urllib.request.Request("http://ip-api.com", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            print(f"{G}[✔] Public IP Address : {data.get('query')}{W}")
            print(f"{G}[✔] ISP / Provider    : {data.get('isp')}{W}")
            print(f"{G}[✔] Country / City    : {data.get('country')} ({data.get('city')}){W}")
    except Exception as e:
        print(f"{R}[✘] Network Error: Unable to fetch public details ({e}){W}")
    input(f"\n{Y}Press Enter to return to Menu...{W}")

def port_worker(target, queue):
    while not queue.empty():
        port = queue.get()
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1.0)
            result = s.connect_ex((target, port))
            if result == 0:
                with print_lock:
                    print(f"{G}[✔] Port {port:5} : OPEN{W}")
            s.close()
        except:
            pass
        queue.task_done()

def fast_port_scanner():
    target = input(f"{C}[?] Enter Target IP or Domain: {W}").strip()
    if not target: return
    
    try:
        target_ip = socket.gethostbyname(target)
        print(f"\n{Y}[*] Scanning Target IP: {target_ip}{W}")
    except socket.gaierror:
        print(f"{R}[✘] Invalid Domain or IP Address!{W}")
        time.sleep(2)
        return

    print(f"{C}[*] Starting Multi-Threaded Port Scan (Top 1024 Ports)...{W}\n")
    queue = Queue()
    for port in range(1, 1025):
        queue.put(port)

    # Spawning 100 concurrent threads for fast heavy scanning
    for _ in range(100):
        t = threading.Thread(target=port_worker, args=(target_ip, queue))
        t.daemon = True
        t.start()
        
    queue.join()
    print(f"\n{G}[+] Scan Complete!{W}")
    input(f"\n{Y}Press Enter to return to Menu...{W}")

def subdomain_scanner():
    domain = input(f"{C}[?] Enter Target Domain (e.g., google.com): {W}").strip()
    if not domain: return
    
    # Common massive list of subdomains for quick scanning
    subdomains = ['www', 'mail', 'ftp', 'admin', 'blog', 'cpanel', 'webmail', 'server', 'ns1', 'ns2', 
                  'autodiscover', 'vpn', 'm', 'secure', 'dev', 'test', 'shop', 'api', 'beta', 'cloud']
    
    print(f"\n{Y}[*] Hunting Subdomains for {domain}...{W}\n")
    found_subs = []
    
    for sub in subdomains:
        target_url = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target_url)
            print(f"{G}[✔] Found: {target_url:25} -> IP: {ip}{W}")
            found_subs.append(target_url)
        except socket.gaierror:
            pass
            
    print(f"\n{G}[+] Total Subdomains Found: {len(found_subs)}{W}")
    input(f"\n{Y}Press Enter to return to Menu...{W}")

def main_menu():
    while True:
        banner()
        print(f"{C}⚡ MAIN INTERFACES:{W}")
        print(f" [{G}1{W}] Target Network & Public IP Recon")
        print(f" [{G}2{W}] Multi-Threaded Heavy Port Scanner")
        print(f" [{G}3{W}] Passive Subdomain Discovery Engine")
        print(f" [{R}0{W}] Exit Commando Suite\n")
        
        choice = input(f"{C}└─╼ select_option: {W}").strip()
        
        if choice == '1':
            banner()
            get_ip_info()
        elif choice == '2':
            banner()
            fast_port_scanner()
        elif choice == '3':
            banner()
            subdomain_scanner()
        elif choice == '0':
            print(f"\n{R}[!] Disconnecting from Shadow Domain... Goodbye!{W}\n")
            sys.exit()
        else:
            print(f"{R}[✘] Invalid Selection!{W}")
            time.sleep(1)

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Script Aborted By Commando.{W}\n")
        sys.exit()
