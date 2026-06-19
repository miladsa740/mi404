import requests
import base64
import random

def fetch_servers():
    url1 = "https://b1b.blkbmisa.dpdns.org/my-milisa?sub=M7G5"
    url2 = "https://n1m.novacell95.qzz.io/m1outlook?sub=m1u"
    url3 = "https://raw.githubusercontent.com/ThomasJasperthecat/sub/refs/heads/main/sublist2.txt"

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

            # حذف خطوط خالی
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
    servers2 = fetch_from_url(url2, "url2", limit=100)
    servers3 = fetch_from_url(url3, "url3", limit=50)

    # ادغام همه کانفیگ‌ها
    all_servers.extend(servers1)
    all_servers.extend(servers2)
    all_servers.extend(servers3)

    if not all_servers:
        print("❗ هیچ سروری دریافت نشد.")
        return

    # حذف کانفیگ‌های تکراری (اختیاری)
    all_servers = list(dict.fromkeys(all_servers))

    # مخلوط کردن کامل
    random.shuffle(all_servers)

    try:
        with open("servers.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(all_servers))

        print(f"✅ {len(all_servers)} سرور در servers.txt ذخیره شد.")

    except Exception as e:
        print(f"❌ خطا در ذخیره فایل:")
        print(e)

if __name__ == "__main__":
    fetch_servers()