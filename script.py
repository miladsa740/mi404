import requests
import base64
import random

def fetch_servers():
    url1 = "https://b1b.blkbmisa.dpdns.org/my-milisa?sub=M7G5"
    url2 = "https://n1m.novacell95.qzz.io/m1outlook?sub=m1u"
    url3 = "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt"
    url4 = "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt"
    url5 = "https://raw.githubusercontent.com/RKPchannel/RKP_bypass_configs/refs/heads/main/whitelist.txt"

    all_servers = []

    def fetch_from_url(url, url_name, limit=None):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            print(f"✅ داده‌ها از {url_name} دریافت شد.")

            content = response.text.strip()

            try:
                decoded = base64.b64decode(
                    content + '=' * (-len(content) % 4)
                ).decode('utf-8')

                if "://" in decoded:
                    lines = decoded.strip().splitlines()
                else:
                    lines = content.splitlines()

            except Exception:
                lines = content.splitlines()

            lines = [line.strip() for line in lines if line.strip()]

            if limit:
                lines = lines[:limit]

            return lines

        except Exception as e:
            print(f"❌ خطا در {url_name}: {e}")
            return []

    servers1 = fetch_from_url(url1, "url1")
    servers2 = fetch_from_url(url2, "url2", 300)
    servers3 = fetch_from_url(url3, "url3", 200)
    servers4 = fetch_from_url(url4, "url4", 100)
    servers5 = fetch_from_url(url5, "url5", 100)

    all_servers.extend(servers1)
    all_servers.extend(servers2)
    all_servers.extend(servers3)
    all_servers.extend(servers4)
    all_servers.extend(servers5)

    if not all_servers:
        print("❗ هیچ کانفیگی دریافت نشد.")
        return

    # حذف تکراری‌ها
    all_servers = list(dict.fromkeys(all_servers))

    # شافل
    random.shuffle(all_servers)

    # فایل معمولی
    with open("servers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_servers))

    print(f"✅ {len(all_servers)} کانفیگ در servers.txt ذخیره شد.")

    # فایل Base64 برای FlClash
    subscription_text = "\n".join(all_servers)
    encoded = base64.b64encode(
        subscription_text.encode("utf-8")
    ).decode("utf-8")

    with open("flclashmi.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    print("✅ flclashmi.txt ساخته شد.")

if __name__ == "__main__":
    fetch_servers()
