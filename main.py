import requests
import re
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 🎯 SOURCES (Full Scan Mode)
# ==========================================
SOURCES = [
    # --- Premium GitHub Raw Sources ---
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.txt",
    
    # --- Telegram Channels (Web Preview Mode /s/) ---
    "https://t.me/s/ProxyMTProto",
    "https://t.me/s/TelMTProto",
    "https://t.me/s/Myporoxy",
    "https://t.me/s/PewezaVPN",
    "https://t.me/s/ProxyHagh",
    "https://t.me/s/iMTProto",
    "https://t.me/s/Proxy_Qavi",
    "https://t.me/s/NoteProxy",
    "https://t.me/s/proxymtprotoj",
    "https://t.me/s/TelMTProto",
    "https://t.me/s/iRoProxy",

  
    # --- 👇 ADD YOUR OWN SOURCES HERE 👇 ---
    # "YOUR_CHANNEL_LINK_OR_RAW_URL",
]

# ⚙️ Settings
TIMEOUT = 5.0        # 5 seconds timeout (To catch slower proxies)
MAX_THREADS = 50     # Fast scanning

# ==========================================
# 🛠 Functions
# ==========================================

def fetch_proxies():
    print("🔍 Scanning all sources (Full History)...")
    all_proxies = set()
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in SOURCES:
        try:
            print(f"   Downloading: {url}...")
            resp = requests.get(url, headers=headers, timeout=15)
            text = resp.text
            
            # Find ALL links (No limit)
            # Regex for tg:// and https://t.me/proxy
            matches = re.findall(r'(?:tg://|https://t\.me/)proxy\?server=([^&]+)&port=(\d+)&secret=([a-zA-Z0-9]+)', text)
            
            for server, port, secret in matches:
                all_proxies.add((server, int(port), secret))
                
        except Exception as e:
            print(f"   Error grabbing {url}: {e}")
            
    print(f"📦 Total Candidates Found: {len(all_proxies)}")
    return list(all_proxies)

def check_proxy(proxy_data):
    server, port, secret = proxy_data
    try:
        start_time = time.time()
        # TCP Connect Test
        sock = socket.create_connection((server, port), timeout=TIMEOUT)
        sock.close()
        ping = int((time.time() - start_time) * 1000)
        return f"tg://proxy?server={server}&port={port}&secret={secret}", ping
    except:
        return None, None

def main():
    raw_proxies = fetch_proxies()
    working_proxies = []
    
    print(f"⚡️ Starting Connectivity Test (Threads: {MAX_THREADS})...")
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = executor.map(check_proxy, raw_proxies)
        
        for link, ping in results:
            if link:
                working_proxies.append({'link': link, 'ping': ping})

    # Sort by speed
    working_proxies.sort(key=lambda x: x['ping'])
    
    # Extract links
    final_links = [x['link'] for x in working_proxies]
    
    # Save to file
    if final_links:
        with open("mtproto.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_links))
        print(f"\n💎 SUCCESS! Found {len(final_links)} working proxies.")
    else:
        print("\n❌ Failed. No working proxies found.")

if __name__ == "__main__":
    main()
