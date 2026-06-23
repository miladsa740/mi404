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

    all_lines = list(dict.fromkeys(all_lines))
    random.shuffle(all_lines)

    with open("servers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_lines))

    print(f"🎉 {len(all_lines)} سرور یکتا ذخیره شد.")

    # تولید config.yaml
    generate_clash_config(urls)

def generate_clash_config(sub_urls):
    combined = "|".join(sub_urls)
    encoded_url = urllib.parse.quote(combined)

    # backend جدید و پایدار (sub.dler.io)
    subconverter_url = (
        f"https://sub.dler.io/sub"
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
        f"&insert=false"
    )

    try:
        print("🔄 در حال تبدیل با sub.dler.io ...")
        response = requests.get(subconverter_url, timeout=90)  # تایم‌اوت بیشتر
        response.raise_for_status()

        if len(response.text) < 500:
            raise Exception("پاسخ خیلی کوچک (احتمال خطا)")

        with open("config.yaml", "w", encoding="utf-8") as f:
            f.write(response.text)

        proxy_count = len([line for line in response.text.splitlines() if line.strip().startswith("- name:")])
        print(f"✅ config.yaml با موفقیت ساخته شد! (~{proxy_count} پروکسی)")
        
    except Exception as e:
        print(f"❌ خطا در تولید config.yaml: {e}")
        print("⚠️ فقط servers.txt ذخیره شد. بعداً دستی با Subconverter تست کنید.")

if __name__ == "__main__":
    fetch_servers()
