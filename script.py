import requests
import random
from datetime import datetime
import urllib.parse
import os

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

    print(f"🎉 {len(all_lines)} سرور یکتا در servers.txt ذخیره شد.")

    # تلاش برای ساخت config.yaml
    success = generate_clash_config(urls)
    if not success:
        print("⚠️ config.yaml ساخته نشد. فقط servers.txt آپدیت شد.")

def generate_clash_config(sub_urls):
    combined = "|".join(sub_urls)
    encoded_url = urllib.parse.quote(combined)

    # لیست backendهای فعال (به ترتیب امتحان می‌شوند)
    backends = [
        "https://sub.v1.mk/sub",           # FeiYang - بسیار پایدار
        "https://id9.cc/sub",              # PinYun
        "https://bianyuan.xyz/sub",        # Edge
        "https://subconverter.exi.software/sub",
    ]

    config_url = "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/config/ACL4SSR_Online_Full.ini"

    for base_url in backends:
        subconverter_url = (
            f"{base_url}?target=clash"
            f"&url={encoded_url}"
            f"&config={urllib.parse.quote(config_url)}"
            f"&emoji=true&list=false&tfo=false&scv=true&fdn=false&sort=false&new_name=true"
        )

        try:
            print(f"🔄 تلاش با {base_url} ...")
            response = requests.get(subconverter_url, timeout=90)
            
            if response.status_code == 200 and len(response.text) > 1000 and "proxies:" in response.text.lower():
                with open("config.yaml", "w", encoding="utf-8") as f:
                    f.write(response.text)
                
                proxy_count = sum(1 for line in response.text.splitlines() if line.strip().startswith("- name:"))
                print(f"✅ config.yaml با موفقیت ساخته شد! (~{proxy_count} پروکسی)")
                return True
            else:
                print(f"   پاسخ نامعتبر ({len(response.text)} کاراکتر)")
        except Exception as e:
            print(f"   خطا: {e}")

    print("❌ همه backendها شکست خوردند.")
    return False

if __name__ == "__main__":
    fetch_servers()
