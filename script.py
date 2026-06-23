import requests
import base64
import random
import yaml  # اضافه شدن کتابخانه پردازش YAML

def fetch_servers():
    url1 = "https://b1b.blkbmisa.dpdns.org/my-milisa?sub=M7G5"
    url2 = "https://n1m.novacell95.qzz.io/m1outlook?sub=m1u"
    url3 = "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt"

    # لینک‌های جدید را اینجا قرار بده
    url4 = "https://raw.githubusercontent.com/LimeHi/LimeVPN/main/LimeVPN.txt"
    url5 = "https://raw.githubusercontent.com/RKPchannel/RKP_bypass_configs/refs/heads/main/whitelist.txt"

    all_servers = []

    def fetch_from_url(url, url_name, limit=None):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            print(f"✅ داده‌ها با موفقیت از {url_name} دریافت شدند.")

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

            if limit is not None:
                lines = lines[:limit]

            return lines

        except requests.RequestException as e:
            print(f"❌ خطا در دریافت داده از {url_name}:")
            print(e)
            return []

        except Exception as e:
            print(f"❌ خطایی در پردازش داده‌ها از {url_name}:")
            print(e)
            return []

    # دریافت کانفیگ‌ها
    servers1 = fetch_from_url(url1, "url1")
    servers2 = fetch_from_url(url2, "url2", limit=300)
    servers3 = fetch_from_url(url3, "url3", limit=200)
    servers4 = fetch_from_url(url4, "url4", limit=100)
    servers5 = fetch_from_url(url5, "url5", limit=100)

    # ادغام همه کانفیگ‌ها
    all_servers.extend(servers1)
    all_servers.extend(servers2)
    all_servers.extend(servers3)
    all_servers.extend(servers4)
    all_servers.extend(servers5)

    if not all_servers:
        print("❗ هیچ سروری دریافت نشد.")
        return

    # حذف کانفیگ‌های تکراری
    all_servers = list(dict.fromkeys(all_servers))

    # مخلوط کردن کامل همه کانفیگ‌ها
    random.shuffle(all_servers)

    # ذخیره خروجی به صورت ساختار یافته در فایل YAML
    try:
        # ساخت یک دیکشنری ساختاریافته برای فایل YAML
        yaml_structure = {
            "total_servers": len(all_servers),
            "servers": all_servers
        }

        with open("servers.yaml", "w", encoding="utf-8") as f:
            # dump کردن داده‌ها با استایل استاندارد و پشتیبانی از متون فارسی/کاراکترهای خاص
            yaml.dump(yaml_structure, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        print(f"✅ {len(all_servers)} سرور با موفقیت در فایل servers.yaml ذخیره شد.")

    except Exception as e:
        print("❌ خطا در ذخیره فایل YAML:")
        print(e)

if __name__ == "__main__":
    fetch_servers()
