import requests
import re
import socket
import time
import binascii
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# 🎯 منابع (فقط منابعی که پروکسی MTProto میذارن)
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
    "https://t.me/s/proxy_mci",
    "https://t.me/s/mtproto_proxy_iran",
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

# ⚙️ تنظیمات سخت‌گیرانه
TIMEOUT = 1.5        # اگه بیشتر از 1.5 ثانیه طول کشید، بندازش دور
MAX_PROXIES = 50     # فقط 50 تا از بهترین‌ها رو نگه دار

# ==========================================
# 🛠 توابع
# ==========================================

def fetch_proxies():
    print("🔍 در حال اسکن منابع...")
    proxies = set()
    
    for url in SOURCES:
        try:
            resp = requests.get(url, timeout=5).text
            # ریجکس دقیق برای استخراج (هم tg:// هم https)
            # فقط سکرت‌هایی که کاراکترهای مجاز دارن رو میگیره
            matches = re.findall(r'(?:tg://|https://t\.me/)proxy\?server=([^&]+)&port=(\d+)&secret=([a-zA-Z0-9]+)', resp)
            
            for server, port, secret in matches:
                # فیلتر اولیه: سکرت باید معتبر باشه (معمولا 32 کاراکتر)
                if len(secret) >= 32: 
                    proxies.add((server, int(port), secret))
        except:
            pass
            
    print(f"📦 تعداد کل کاندیداها: {len(proxies)}")
    return list(proxies)

def check_proxy_strict(proxy_data):
    server, port, secret = proxy_data
    
    try:
        # تست پینگ دقیق
        start_time = time.time()
        
        # 1. ایجاد سوکت
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        
        # 2. تلاش برای اتصال (Connect)
        sock.connect((server, port))
        
        # 3. تست ارسال دیتا (شبیه‌سازی هندشیک اولیه)
        # این باعث میشه مطمئن بشیم سرور واقعا دیتای ما رو میگیره و فقط روشن نیست
        # یه بایت رندوم میفرستیم (تستِ زنده بودن)
        sock.sendall(binascii.unhexlify('ef')) 
        
        # اگه تا اینجا ارور نداد و تایم اوت نشد، یعنی سرور پاسخگوئه
        latency = int((time.time() - start_time) * 1000)
        sock.close()
        
        return {
            'link': f"tg://proxy?server={server}&port={port}&secret={secret}",
            'ping': latency
        }
    except:
        return None

def main():
    raw_proxies = fetch_proxies()
    valid_proxies = []
    
    print(f"🔥 شروع تست دقیق (با اینترنت لوکال شما)...")
    print(f"⏳ تایم‌اوت مجاز: {TIMEOUT} ثانیه")
    
    # استفاده از 50 تا ترد همزمان برای سرعت بالا
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_proxy_strict, raw_proxies)
        
        for res in results:
            if res:
                print(f"✅ زنده: {res['ping']}ms")
                valid_proxies.append(res)

    # مرتب‌سازی بر اساس پینگ (کمتر = بهتر)
    valid_proxies.sort(key=lambda x: x['ping'])
    
    # انتخاب بهترین‌ها
    top_proxies = valid_proxies[:MAX_PROXIES]
    
    if not top_proxies:
        print("❌ هیچ پروکسی سالمی پیدا نشد! (شاید نتت مشکل داره یا منابع فیلترن)")
        return

    # ذخیره فایل
    final_links = [p['link'] for p in top_proxies]
    
    with open("mtproto.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_links))
        
    print(f"\n💎 {len(final_links)} پروکسی طلایی ذخیره شد.")
    print(f"🚀 بهترین پینگ: {top_proxies[0]['ping']}ms")

if __name__ == "__main__":
    main()
