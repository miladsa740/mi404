import requests

def fetch_servers():
    url1 = "https://icy-bush-0435.coronaalaris2.workers.dev/sub?token=1ede1ce2357450c9a989cb4161c89579"
    url2 = "https://raw.githubusercontent.com/TheConfigs/hcaptcha-configs/main/hcaptchaCONFIGS.txt"
    url3 = "*****"

    all_servers = []

    # تابع کمکی برای دریافت داده از URL
    def fetch_from_url(url, url_name, limit=None):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            print(f"✅ داده‌ها با موفقیت از {url_name} دریافت شدند.")

            lines = response.text.strip().splitlines()

            # اگر limit مشخص شده بود → محدود کن
            if limit is not None:
                return lines[:limit]

            # در غیر اینصورت → همه
            return lines

        except requests.RequestException as e:
            print(f"❌ خطا در دریافت داده از {url_name}:\n{e}")
            return []
        except Exception as e:
            print(f"❌ خطایی در پردازش داده‌ها از {url_name} رخ داد:\n{e}")
            return []

    # لینک اول → بدون محدودیت
    servers1 = fetch_from_url(url1, "url1")

    # لینک دوم و سوم → هرکدوم 40 تا
    servers2 = fetch_from_url(url2, "url2", limit=10)
    servers3 = fetch_from_url(url3, "url3", limit=10)

    all_servers.extend(servers1)
    all_servers.extend(servers2)
    all_servers.extend(servers3)

    if not all_servers:
        print("❗️ هیچ سروری دریافت نشد.")
        return

    try:
        with open("servers.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(all_servers))

        print(f"✅ {len(all_servers)} سرور با موفقیت دریافت و در servers.txt ذخیره شدند.")

    except Exception as e:
        print(f"❌ خطایی در ذخیره‌سازی داده‌ها رخ داد:\n{e}")

if __name__ == "__main__":
    fetch_servers()
