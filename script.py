import requests
import random
from datetime import datetime

def fetch_servers():
    urls = [
        "https://b1b.blkbmisa.dpdns.org/my-milisa?sub=M7G5",
        "https://n1m.novacell95.qzz.io/m1outlook?sub=m1u",
        "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt",
        "https://raw.githubusercontent.com/RKPchannel/RKP_bypass_configs/refs/heads/main/whitelist.txt",
        # لینک‌های جدید را اینجا اضافه کنید
    ]

    all_lines = []
    
    print(f"🚀 شروع به‌روزرسانی سرورها - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    for idx, url in enumerate(urls, 1):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            lines = [
                line.strip() 
                for line in response.text.splitlines() 
                if line.strip() and "://" in line
            ]
            all_lines.extend(lines)
            print(f"✅ {len(lines)} سرور از لینک {idx} دریافت شد")
        except Exception as e:
            print(f"❌ خطا در لینک {idx} ({url[:60]}...): {e}")

    # حذف تکراری‌ها
    all_lines = list(dict.fromkeys(all_lines))
    random.shuffle(all_lines)

    # ذخیره فایل
    with open("servers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))

    print(f"\n🎉 جمعاً {len(all_lines)} سرور یکتا در servers.txt ذخیره شد.")

    # لینک ترکیبی برای Subconverter (رایگان و آنلاین)
    combined_url = "|".join(urls)
    print("\n🔗 لینک ترکیبی Subconverter:")
    print(combined_url)
    print("\n📌 برای استفاده در Clash:")
    print("1. به https://subconverter.exi.software/convert بروید")
    print("2. Target را روی Clash Meta بگذارید")
    print("3. لینک بالا را در Subscription URL بچسبانید")
    print("4. Convert بزنید و لینک خروجی را در Clash Verge وارد کنید.")

if __name__ == "__main__":
    fetch_servers()
