import requests
import base64
import random


def fetch_servers():

    urls = [
        "https://morning-rain-8b5d.novinex20.workers.dev/my-milisa?sub=mi7540",
        "https://withered-mouse-3cf1.softfirec60e.workers.dev/m1outlook?sub=m1u",
        "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
        "https://raw.githubusercontent.com/justVisiting992/xray-Config-Collector/main/vless_iran.txt",
        "https://raw.githubusercontent.com/miladsa740/blackbird/refs/heads/main/config.txt"
    ]

    # None یعنی بدون محدودیت
    limits = [
        None,  # لینک اول
        300,   # لینک دوم
        50,   # لینک سوم
        50,   # لینک چهارم
        50    # لینک پنجم
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
