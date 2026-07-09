import requests
import base64
import random

def fetch_servers():

    urls = [
        "https://b1b.blkbmisa.dpdns.org/my-milisa?sub=M7G5",
        "https://n1m.novacell95.qzz.io/m1outlook?sub=m1u",
        "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt",
        "https://raw.githubusercontent.com/RKPchannel/RKP_bypass_configs/refs/heads/main/whitelist.txt"
    ]

    limits = [None, 300, 200, 100, 100]

    all_servers = []

    def fetch(url, name, limit=None):
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()

            content = r.text.strip()

            try:
                decoded = base64.b64decode(content + "===").decode("utf-8")
                lines = decoded.splitlines() if "://" in decoded else content.splitlines()
            except:
                lines = content.splitlines()

            lines = [x.strip() for x in lines if x.strip()]

            if limit:
                lines = lines[:limit]

            print(f"✅ {name} OK ({len(lines)})")
            return lines

        except Exception as e:
            print(f"❌ {name} ERROR: {e}")
            return []

    for i in range(5):
        all_servers.extend(fetch(urls[i], f"url{i+1}", limits[i]))

    if not all_servers:
        print("❗ هیچ سروری دریافت نشد")
        return

    # حذف تکراری
    all_servers = list(dict.fromkeys(all_servers))

    # shuffle
    random.shuffle(all_servers)

    # خروجی
    with open("servers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_servers))

    print(f"🎉 Done: {len(all_servers)} servers saved")

if __name__ == "__main__":
    fetch_servers()
