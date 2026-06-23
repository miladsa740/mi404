import requests
import random
from datetime import datetime
import urllib.parse

def fetch_servers():
    urls = [
        "https://b1b.blkbmisa.dpdns.org/my-milisa?sub=M7G5",
        "https://n1m.novacell95.qzz.io/m1outlook?sub=m1u",
        "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt",
        "https://raw.githubusercontent.com/RKPchannel/RKP_bypass_configs/refs/heads/main/whitelist.txt",
        # لینک جدید اضافه کنید
    ]

    print(f"🚀 شروع به‌روزرسانی - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    all_lines = []
    for idx, url in enumerate(urls, 1):
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            lines = [line.strip() for line in response.text.splitlines() if line.strip() and "://" in line]
            all_lines.extend(lines)
            print(f"✅ {len(lines)} سرور از لینک {idx}")
        except Exception as e:
            print(f"❌ خطا در لینک {idx}: {e}")

    # حذف تکراری و شافل
    all_lines = list(dict.fromkeys(all_lines))
    random.shuffle(all_lines)

    with open("servers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))

    print(f"🎉 {len(all_lines)} سرور یکتا ذخیره شد.")

    # === تولید config.yaml با Subconverter ===
    generate_clash_config(urls)

def generate_clash_config(sub_urls):
    # لینک ترکیبی
    combined = "|".join(sub_urls)
    encoded_url = urllib.parse.quote(combined)

    # یکی ازインスタンス‌های پایدار Subconverter
    subconverter_url = (
        f"https://subconverter.exi.software/sub"
        f"?target=clash"
        f"&url={encoded_url}"
        f"&config=https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.ini"
        f"&emoji=true"
        f"&list=false"
        f"&tfo=false"
        f"&scv=true"
        f"&fdn=false"
        f"&sort=false"
        f"&new_name=true"
    )

    try:
        print("🔄 در حال تبدیل با Subconverter...")
        response = requests.get(subconverter_url, timeout=60)
        response.raise_for_status()

        # ذخیره config.yaml
        with open("config.yaml", "w", encoding="utf-8") as f:
            f.write(response.text)

        print("✅ config.yaml با موفقیت تولید و ذخیره شد!")
        print(f"   تعداد پروکسی تقریبی: {len([line for line in response.text.splitlines() if '- name:' in line])}")

    except Exception as e:
        print(f"❌ خطا در تولید config.yaml: {e}")
        # fallback: فقط servers.txt
        print("⚠️ فقط servers.txt ذخیره شد.")

if __name__ == "__main__":
    fetch_servers()
