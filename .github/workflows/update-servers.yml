import requests
import base64
import random
import yaml
from urllib.parse import urlparse, parse_qs, unquote
import json

def fetch_servers():
    urls = [
        ("https://b1b.blkbmisa.dpdns.org/my-milisa?sub=M7G5", "url1", None),
        ("https://n1m.novacell95.qzz.io/m1outlook?sub=m1u", "url2", 300),
        ("https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt", "url3", 200),
        ("https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt", "url4", 100),
        ("https://raw.githubusercontent.com/RKPchannel/RKP_bypass_configs/refs/heads/main/whitelist.txt", "url5", 100),
        # لینک‌های جدید را اینجا اضافه کن
    ]

    all_servers = []
    
    def fetch_from_url(url, url_name, limit=None):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            print(f"✅ داده‌ها با موفقیت از {url_name} دریافت شدند.")
            content = response.text.strip()
            
            # تلاش برای دیکد base64
            try:
                padded = content + '=' * (-len(content) % 4)
                decoded = base64.b64decode(padded).decode('utf-8')
                if "://" in decoded:
                    lines = decoded.strip().splitlines()
                else:
                    lines = content.splitlines()
            except:
                lines = content.splitlines()
            
            lines = [line.strip() for line in lines if line.strip() and "://" in line]
            if limit:
                lines = lines[:limit]
            return lines
        except Exception as e:
            print(f"❌ خطا در {url_name}: {e}")
            return []

    for url, name, limit in urls:
        all_servers.extend(fetch_from_url(url, name, limit))

    if not all_servers:
        print("❗ هیچ سروری دریافت نشد.")
        return

    # حذف تکراری‌ها
    all_servers = list(dict.fromkeys(all_servers))
    random.shuffle(all_servers)
    
    # ذخیره لیست خام (اختیاری)
    with open("servers.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_servers))
    print(f"✅ {len(all_servers)} سرور خام در servers.txt ذخیره شد.")

    # تولید config.yaml برای Clash
    clash_config = generate_clash_config(all_servers)
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(clash_config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)
    
    print(f"✅ فایل config.yaml برای Clash آماده شد! ({len(all_servers)} پروکسی)")

def parse_proxy_link(link):
    """پارس ساده لینک‌ها به فرمت Clash (برای انواع رایج)"""
    try:
        if link.startswith("vmess://"):
            # VMess base64
            b64 = link[8:]
            padded = b64 + '=' * (-len(b64) % 4)
            data = json.loads(base64.b64decode(padded).decode('utf-8'))
            return {
                "name": data.get("ps") or f"vmess-{random.randint(1000,9999)}",
                "type": "vmess",
                "server": data.get("add"),
                "port": int(data.get("port")),
                "uuid": data.get("id"),
                "alterId": int(data.get("aid", 0)),
                "cipher": data.get("scy", "auto"),
                "tls": data.get("tls") == "tls" or str(data.get("tls")).lower() == "true",
                "network": data.get("net", "tcp"),
                "ws-opts": {"path": data.get("path", "/")} if data.get("net") == "ws" else None,
            }
        
        elif link.startswith(("trojan://", "trojan-go://")):
            parsed = urlparse(link)
            query = parse_qs(parsed.query)
            return {
                "name": unquote(parsed.fragment) or f"trojan-{random.randint(1000,9999)}",
                "type": "trojan",
                "server": parsed.hostname,
                "port": int(parsed.port or 443),
                "password": parsed.username or parsed.password,
                "sni": query.get("sni", [parsed.hostname])[0],
                "skip-cert-verify": False,
            }
        
        elif link.startswith("ss://"):
            # Shadowsocks ساده
            if "@" in link:
                # جدید
                parsed = urlparse(link)
                method_pass = base64.b64decode(parsed.username + '==').decode() if parsed.username else ""
                method, password = method_pass.split(":", 1) if ":" in method_pass else ("aes-256-gcm", method_pass)
                return {
                    "name": unquote(parsed.fragment) or f"ss-{random.randint(1000,9999)}",
                    "type": "ss",
                    "server": parsed.hostname,
                    "port": int(parsed.port),
                    "cipher": method,
                    "password": password,
                }
        
        # برای انواع دیگر (vless و ...) فعلاً نام می‌گذاریم (Clash Meta بهتر هندل می‌کند)
        return {
            "name": f"proxy-{random.randint(10000,99999)}",
            "type": "ss",  # placeholder - Clash Meta خودش تشخیص می‌دهد اگر subscription باشد
            "server": "127.0.0.1",
            "port": 1080,
        }
    except:
        return None

def generate_clash_config(proxies_list):
    clash_proxies = []
    for link in proxies_list:
        proxy = parse_proxy_link(link)
        if proxy:
            # حذف None ها
            proxy = {k: v for k, v in proxy.items() if v is not None}
            clash_proxies.append(proxy)

    config = {
        "port": 7890,
        "socks-port": 7891,
        "allow-lan": True,
        "mode": "rule",
        "log-level": "info",
        "ipv6": True,
        
        "proxies": clash_proxies,
        
        "proxy-groups": [
            {
                "name": "🚀 Auto",
                "type": "url-test",
                "proxies": [p["name"] for p in clash_proxies[:min(100, len(clash_proxies))]],  # محدود برای سرعت
                "url": "http://www.gstatic.com/generate_204",
                "interval": 300,
                "timeout": 5000
            },
            {
                "name": "🌍 Proxy",
                "type": "select",
                "proxies": ["🚀 Auto", "DIRECT"]
            }
        ],
        
        "rules": [
            "MATCH,🌍 Proxy"
        ]
    }
    return config

if __name__ == "__main__":
    fetch_servers()
