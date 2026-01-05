import requests
import re
import html
import random

# ==========================================
# 🎯 منابع (هر چی بیشتر، بهتر)
# ==========================================
SOURCES = [
    # --- Premium GitHub Raw Sources ---
    "https://raw.githubusercontent.com/MahsaNetConfigTopic/proxy/main/proxies.txt",
    
    # --- Telegram Channels (Web Preview Mode /s/) ---
    "https://t.me/s/ProxyMTProto",
    "https://t.me/s/TelMTProto",
    "https://t.me/s/Myporoxy",
    "https://t.me/s/ProxyMTProto_tel",
    "https://t.me/s/ProxyHagh",
    "https://t.me/s/iMTProto",
    "https://t.me/s/Proxy_Qavi",
    "https://t.me/s/NoteProxy",
    "https://t.me/s/proxymtprotoj",
    "https://t.me/s/Pen_Musix",
    "https://t.me/s/TelMTProto",
    "https://t.me/s/iRoProxy",

  
    # --- 👇 ADD YOUR OWN SOURCES HERE 👇 ---
    # "YOUR_CHANNEL_LINK_OR_RAW_URL",
]

# ⚙️ تنظیمات محدودیت
TOTAL_LIMIT = 2000  # کل پروکسی‌ها نباید بیشتر از این بشه

def fetch_and_parse(url, limit_per_source):
    try:
        print(f"📥 دریافت از: {url} ...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        
        # 1. تمیزکاری کدهای HTML (خیلی مهم برای کانال‌های تلگرام)
        text = html.unescape(resp.text)
        
        # 2. استخراج لینک‌ها با ریجکس
        pattern = r'(?:tg://|https://t\.me/)proxy\?server=([^&]+)&port=(\d+)&secret=([^"\s&\n]+)'
        matches = re.findall(pattern, text)
        
        # تبدیل به لینک استاندارد
        proxies = []
        for server, port, secret in matches:
            link = f"tg://proxy?server={server}&port={port}&secret={secret}"
            proxies.append(link)
            
        # 3. برداشتنِ "آخرین‌ها" (جدیدترین‌ها)
        # اگر تعداد پیدا شده بیشتر از سهمیه باشه، از آخر لیست برمیداریم
        if len(proxies) > limit_per_source:
            print(f"   🔹 {len(proxies)} تا پیدا شد -> {limit_per_source} تای آخر انتخاب شد.")
            return proxies[-limit_per_source:] # برش از انتها (جدیدترین‌ها)
        else:
            print(f"   🔹 {len(proxies)} تا پیدا شد (همه انتخاب شدند).")
            return proxies
            
    except Exception as e:
        print(f"   ❌ خطا: {e}")
        return []

def main():
    print("🚀 شروع جمع‌آوری سریع (بدون تست)...")
    
    all_proxies = []
    
    # محاسبه سهمیه هر منبع
    # مثلا اگه 10 تا منبع داریم و ظرفیت 2000 تاست، از هر کدوم 200 تا برمیداریم
    limit_per_source = TOTAL_LIMIT // len(SOURCES)
    print(f"📊 سهمیه هر منبع: {limit_per_source} پروکسی جدید")

    for url in SOURCES:
        fetched = fetch_and_parse(url, limit_per_source)
        all_proxies.extend(fetched)

    # حذف تکراری‌ها (ست کردن)
    unique_proxies = list(set(all_proxies))
    
    # اگر بعد از حذف تکراری‌ها بیشتر از 2000 تا شد، کات میکنیم
    if len(unique_proxies) > TOTAL_LIMIT:
        unique_proxies = unique_proxies[:TOTAL_LIMIT]

    print(f"\n📦 تعداد نهایی پروکسی‌ها: {len(unique_proxies)}")

    # ذخیره در فایل
    if unique_proxies:
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open("mtproto.txt", "w", encoding="utf-8") as f:
            f.write(f"# Updated: {now} UTC\n")
            f.write(f"# Count: {len(unique_proxies)}\n")
            f.write("\n".join(unique_proxies))
        print("💾 فایل ذخیره شد.")
    else:
        print("❌ هیچ پروکسی‌ای پیدا نشد.")

if __name__ == "__main__":
    main()
