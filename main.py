import urllib.request
import re
import socket
import time
import random
import os

# ==========================================
# 🎯 منابع (Sources)
# ==========================================
SOURCES = [
    # --- Premium GitHub Raw Sources ---
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/tg/mtproto.txt",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-proxies-collector/main/proxies.txt",
    "https://raw.githubusercontent.com/MahsaNetConfigTopic/proxy/main/proxies.txt",
    
    # --- Telegram Channels (Web Preview Mode /s/) ---
    "https://t.me/s/ProxyMTProto",
    "https://t.me/s/TelMTProto",
    "https://t.me/s/Myporoxy",
    "https://t.me/s/ProxyMTProto_tel",
    "https://t.me/s/PewezaVPN",
    "https://t.me/s/asrnovin_ir",
    "https://t.me/s/ProxyHagh",
    "https://t.me/s/iMTProto",
    "https://t.me/s/Proxy_Qavi",
    "https://t.me/s/NoteProxy",
    "https://t.me/s/proxymtprotoj",
    "https://t.me/s/Pen_Musix",
    "https://t.me/s/ShadowProxy66",
    "https://t.me/s/TelMTProto",
    "https://t.me/s/iRoProxy",

  
    # --- 👇 ADD YOUR OWN SOURCES HERE 👇 ---
    # "YOUR_CHANNEL_LINK_OR_RAW_URL",
]
# 🛡️ تنظیمات ایمنی (ضد بن)
TIMEOUT = 1.5       # تایم‌اوت کوتاه
CHECK_LIMIT = 100   # فقط 100 تا رو تست کن (فشار صفر روی سرور)

# ==========================================
# 🛠 توابع (بدون نیاز به requests)
# ==========================================

def fetch_url(url):
    try:
        # استفاده از کتابخانه داخلی پایتون (سبک‌تر از requests)
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except:
        return ""

def check_proxy(server, port):
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        sock.connect((server, int(port)))
        sock.close()
        ping = int((time.time() - start) * 1000)
        return ping
    except:
        return None

def main():
    print("🚀 شروع حالت اکو (Eco Mode)...")
    
    # 1. جمع‌آوری
    proxies = set()
    for url in SOURCES:
        content = fetch_url(url)
        # پیدا کردن لینک‌ها
        matches = re.findall(r'(?:tg://|https://t\.me/)proxy\?server=([^&]+)&port=(\d+)&secret=([a-zA-Z0-9]+)', content)
        for s, p, sec in matches:
            proxies.add((s, p, sec))
            
    print(f"📦 تعداد کل پروکسی‌های یافت شده: {len(proxies)}")

    # 2. قرعه‌کشی (مهمترین بخش ضد بن)
    # به جای تست همه، فقط تعدادی رو رندوم انتخاب میکنیم
    proxy_list = list(proxies)
    if len(proxy_list) > CHECK_LIMIT:
        print(f"🛡️ جهت ایمنی اکانت، فقط {CHECK_LIMIT} مورد به صورت تصادفی تست می‌شوند.")
        selected_proxies = random.sample(proxy_list, CHECK_LIMIT)
    else:
        selected_proxies = proxy_list

    # 3. تست سرعت
    valid_proxies = []
    print("⚡️ در حال تست اتصال...")
    
    for server, port, secret in selected_proxies:
        ping = check_proxy(server, port)
        if ping:
            print(f"✅ زنده: {ping}ms")
            link = f"tg://proxy?server={server}&port={port}&secret={secret}"
            valid_proxies.append({'link': link, 'ping': ping})

    # 4. ذخیره
    # مرتب‌سازی بر اساس پینگ
    valid_proxies.sort(key=lambda x: x['ping'])
    final_links = [p['link'] for p in valid_proxies]
    
    with open("mtproto.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_links))
        
    print(f"\n💎 {len(final_links)} پروکسی سالم ذخیره شد.")

if __name__ == "__main__":
    main()
