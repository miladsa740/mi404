import requests
import base64
import random
import yaml

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

            print(f"✅ دریافت شد: {url_name}")

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
        print("❗ هیچ سروری دریافت نشد")
        return

    # حذف تکراری
    all_servers = list(dict.fromkeys(all_servers))

    # shuffle
    random.shuffle(all_servers)

    # =========================
    # 1. ذخیره servers.txt
    # =========================
    with open("servers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_servers))

    print(f"✅ servers.txt ساخته شد ({len(all_servers)})")

    # =========================
    # 2. ساخت Mihomo / Clash Meta YAML
    # =========================
    proxies = []

    for i, node in enumerate(all_servers):
        if node.startswith("vmess://"):
            proxies.append({
                "name": f"vmess-{i}",
                "type": "vmess",
                "server": "example.com",
                "port": 443,
                "uuid": "uuid",
                "alterId": 0,
                "cipher": "auto",
                "tls": True
            })

        elif node.startswith("vless://"):
            proxies.append({
                "name": f"vless-{i}",
                "type": "vless",
                "server": "example.com",
                "port": 443,
                "uuid": "uuid",
                "tls": True
            })

        elif node.startswith("trojan://"):
            proxies.append({
                "name": f"trojan-{i}",
                "type": "trojan",
                "server": "example.com",
                "port": 443,
                "password": "password"
            })

        elif node.startswith("ss://"):
            proxies.append({
                "name": f"ss-{i}",
                "type": "ss",
                "server": "example.com",
                "port": 8388,
                "cipher": "aes-128-gcm",
                "password": "password"
            })

    config = {
        "mixed-port": 7890,
        "allow-lan": True,
        "mode": "rule",
        "proxies": proxies,
        "proxy-groups": [
            {
                "name": "PROXY",
                "type": "select",
                "proxies": [p["name"] for p in proxies]
            }
        ],
        "rules": [
            "MATCH,PROXY"
        ]
    }

    with open("flclashmi.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)

    print("✅ flclashmi.yaml ساخته شد")


if __name__ == "__main__":
    fetch_servers()
