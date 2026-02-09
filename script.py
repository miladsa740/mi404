import requests

def fetch_servers():
    url1 = "https://raw.githubusercontent.com/miladsa740/blackbird/refs/heads/main/config.txt"
    url2 = "https://manager.farsonline24.ir"
    url3 = "https://github.com/AvenCores/goida-vpn-configs/raw/refs/heads/main/githubmirror/22.txt"

    all_servers = []

    # تابع کمکی برای دریافت داده از URL
    def fetch_from_url(url, url_name, limit=None):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            print(f"✅ داده‌ها با موفقیت از {url_name} دریافت شدند.")

            lines = response.text.strip().splitlines()

            # اگر limit داده شده بود، محدود کن
            if limit:
                return lines[:limit]

            # اگر limit نداشت → همه خطوط
            return lines

        except requests.RequestException as e:
            print(f"❌ خطا در دریافت داده از {url_name}:\n{e}")
            return []
        except Exception as e:
            print(f"❌ خطایی در پردازش داده‌ها از {url_name} رخ داد:\n{e}")
            return []

    # لینک اول → همه سرورها
    servers1 = fetch_from_url(url1, "url1")

    # لینک دوم و سوم → محدود
    servers2 = fetch_from_url(url2, "url2", limit=70)
    servers3 = fetch_from_url(url3, "url3", limit=70)

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