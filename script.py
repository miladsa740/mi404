import requests

def fetch_servers():
    url1 = "https://raw.githubusercontent.com/mehran1404/Sub_Link/refs/heads/main/V2RAY-Sub.txt"
    url2 = "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_Sub.txt"
    url3 = "https://fs.v2rayse.com/share/20250927/khj8oa2jaj.txt" # اضافه کردن لینک سوم

    all_servers = []

    # تابع کمکی برای دریافت داده از URL
    def fetch_from_url(url, url_name):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # اگر status code غیر از 200 باشه، خطا می‌ندازه
            print(f"✅ داده‌ها با موفقیت از {url_name} دریافت شدند.")
            return response.text.strip().splitlines()[:50] # گرفتن 50 خط اول
        except requests.RequestException as e:
            print(f"❌ خطا در دریافت داده از {url_name}:\n{e}")
            return []
        except Exception as e:
            print(f"❌ خطایی در پردازش داده‌ها از {url_name} رخ داد:\n{e}")
            return []

    # دریافت داده از هر سه لینک
    servers1 = fetch_from_url(url1, "url1")
    servers2 = fetch_from_url(url2, "url2")
    servers3 = fetch_from_url(url3, "url3") # دریافت داده از لینک سوم

    all_servers.extend(servers1)
    all_servers.extend(servers2)
    all_servers.extend(servers3) # اضافه کردن سرورهای لینک سوم

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
