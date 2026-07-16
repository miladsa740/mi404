import requests
import base64
import random


def fetch_servers():

    urls = [
        "https://mi7540.blkbmisa.dpdns.org/my-milisa?sub=mi7540",
        "https://n1m.novacell95.qzz.io/m1outlook?sub=m1u",
        "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt",
        "https://raw.githubusercontent.com/justVisiting992/xray-Config-Collector/main/vless_iran.txt",
        "https://raw.githubusercontent.com/miladsa740/blackbird/refs/heads/main/config.txt"
    ]

    # None یعنی بدون محدودیت
    limits = [
        None,  # لینک اول
        300,   # لینک دوم
        200,   # لینک سوم
        150,   # لینک چهارم
        100    # لینک پنجم
    ]

    all_servers = []

    def fetch(url, name, limit=None):
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()

            content = r.text.strip()

            try:
                decoded = base64.b64decode(content + "===").decode("utf-8")
                if "://" in decoded:
                    lines = decoded.splitlines()
                else:
                    lines = content.splitlines()
            except Exception:
                lines = content.splitlines()

            lines = [x.strip() for x in lines if x.strip()]

            if limit is not None:
                lines = lines[:limit]

            print(f"✅ {name} OK ({len(lines)})")
            return lines

        except Exception as e:
            print(f"❌ {name} ERROR: {e}")
            return []

    for i, url in enumerate(urls):
        all_servers.extend(fetch(url, f"url{i+1}", limits[i]))

    if not all_servers:
        print("❗ هیچ سروری دریافت نشد")
        return

    # حذف موارد تکراری
    all_servers = list(dict.fromkeys(all_servers))

    # مخلوط کردن همه کانفیگ‌ها
    random.shuffle(all_servers)

    # ذخیره در فایل
    with open("servers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_servers))

    print(f"🎉 Done: {len(all_servers)} servers saved")


if __name__ == "__main__":
    fetch_servers()
