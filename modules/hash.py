# hash.py
# اداة الهاش - كسر وتوليد
import hashlib
import threading
from utils.colors import Color, print_color

# متغير يوقف كل الثريدات لما نلاقي الباسورد
found = threading.Event()

def identify_hash_type(hash_input):
    length = len(hash_input)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA1"
    elif length == 64:
        return "SHA256"
    else:
        return "Unknown"

# دالة تحول الكلمة لهاش حسب النوع
def hash_word(word, hash_type):
    if hash_type == "MD5":
        return hashlib.md5(word.encode()).hexdigest()
    elif hash_type == "SHA1":
        return hashlib.sha1(word.encode()).hexdigest()
    elif hash_type == "SHA256":
        return hashlib.sha256(word.encode()).hexdigest()

# دالة يشغلها كل thread على جزء من الـ wordlist
def crack_chunk(words_chunk, hash_input, hash_type):
    for word in words_chunk:
        if found.is_set():
            return
        parts = word.strip().split(" ")
        word = parts[-1] if len(parts) > 1 else parts[0]
        if not word:
            continue
        hashed = hash_word(word, hash_type)
        if hashed == hash_input:
            found.set()
            print_color(f"\n[+] Password found: {word}", Color.GREEN)
            return

# دالة لكسر الهاشات عن طريق wordlist
def crack_hash(hash_input, wordlist_path):    
    hash_type = identify_hash_type(hash_input)
    print_color(f"\n[+] Hash Type: {hash_type}", Color.YELLOW)

    try: 
        with open(wordlist_path, "r", errors="ignore") as f:
            words = f.readlines()
    except:
        print_color("\n[!] Can't load the wordlist!", Color.RED)
        return

    print_color(f"\n[*] Loaded {len(words)} words", Color.YELLOW)
    print_color("[*] Cracking...\n", Color.YELLOW)

    found.clear()

    chunk_size = len(words) // 4
    chunks = [
        words[0:chunk_size],
        words[chunk_size:chunk_size*2],
        words[chunk_size*2:chunk_size*3],
        words[chunk_size*3:]
    ]

    threads = []
    for chunk in chunks:
        t = threading.Thread(target=crack_chunk, args=(chunk, hash_input, hash_type))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    if not found.is_set():
        print_color("\n[!] Hash not found in the wordlist.", Color.RED)

# دالة توليد الهاش
def generate_hash():
    print_color("\n[+] Hash Generator", Color.CYAN)
    
    # نطلب الباسورد
    password = input(f"{Color.YELLOW}[?] Enter password: {Color.RESET}")

    # نعطيه خيار نوع الهاش
    print_color("\n[1] MD5", Color.GREEN)
    print_color("[2] SHA1", Color.GREEN)
    print_color("[3] SHA256", Color.GREEN)
    hash_type = input(f"{Color.YELLOW}[?] Choose hash type: {Color.RESET}").strip()

    if hash_type == "1":
        print_color(f"\n[+] MD5: {hashlib.md5(password.encode()).hexdigest()}", Color.CYAN)
    elif hash_type == "2":
        print_color(f"\n[+] SHA1: {hashlib.sha1(password.encode()).hexdigest()}", Color.CYAN)
    elif hash_type == "3":
        print_color(f"\n[+] SHA256: {hashlib.sha256(password.encode()).hexdigest()}", Color.CYAN)
    else:
        print_color("\n[!] Invalid choice!", Color.RED)

# الدالة الرئيسية
def start_hash():
    print_color("\n[+] Hash Tools", Color.CYAN)

    # نعطيه خيارين
    print_color("\n[1] Crack Hash", Color.GREEN)
    print_color("[2] Generate Hash", Color.GREEN)
    choice = input(f"{Color.YELLOW}[?] Choice: {Color.RESET}")

    if choice == "1":
        # نطلب الهاش
        hash_input = input(f"{Color.YELLOW}[?] Enter the hash to crack: {Color.RESET}").strip()

        hash_type = identify_hash_type(hash_input)
        if hash_type == "Unknown":
            print_color("\n[!] Unsupported hash type!", Color.RED)
            return

        print_color("\n[1] Use passwords wordlist", Color.GREEN)
        print_color("[2] Use custom wordlist", Color.GREEN)
        wchoice = input(f"{Color.YELLOW}[?] Choice: {Color.RESET}")

        if wchoice == "1":
            wordlist_path = "wordlists/passwords_wordlist.txt"
        else:
            wordlist_path = input(f"{Color.YELLOW}[?] Enter wordlist path: {Color.RESET}")

        crack_hash(hash_input, wordlist_path)

    elif choice == "2":
        generate_hash()
    else:
        print_color("\n[!] Invalid choice!", Color.RED)