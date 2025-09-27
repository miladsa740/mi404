import requests
import base64

def fetch_servers():
    url1 = "https://raw.githubusercontent.com/mehran1404/Sub_Link/refs/heads/main/V2RAY-Sub.txt"
    url2 = "https://raw.githubusercontent.com/barry-far/V2ray-config/main/All_Configs_Sub.txt"
    url3 = "https://fs.v2rayse.com/share/20250927/khj8oa2jaj.txt"  # لینک سوم (64 بیتی)

    all_servers = []

    def fetch_from_url(url, url_name, base64_decode=False):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.text.strip()

            if base64_decode:
                try:
                    # بعضی لینک‌ها نیاز به پدینگ دارن
                    padded = data + '=' * (-len(data) % 4)
                    data = base64.b64decode(padded).decode('utf-8', errors='ignore')
                except Exception as e:
                    print(f"❌ خطا در دیکد Base64 {url_name}: {e}")
                    return []

            print(f"✅ داده‌ها با موفقیت از {url_name} دریافت شدند.")
            return data.strip().splitlines()[:50]  # ۵۰ خط اول
        except requests.RequestException as e:
            print(f"❌ خطا در دریافت داده از {url_name}:\n{e}")
            return []
        except Exception as e:
            print(f"❌ خطای پردازش {url_name}:\n{e}")
            return []

    # لینک‌های عادی
    servers1 = fetch_from_url(url1, "url1")
    servers2 = fetch_from_url(url2, "url2")
    # لینک سوم که Base64 است
    servers3 = fetch_from_url(url3, "url3", base64_decode=True)

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
        print(f"❌ خطا در ذخیره‌سازی:\n{e}")

if __name__ == "__main__":
    fetch_servers()
