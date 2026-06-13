import requests
import base64

def fetch_servers():
    url1 = "https://raw.githubusercontent.com/miladsa740/blackbird/refs/heads/main/config.txt"
    url2 = "https://raw.githubusercontent.com/ThomasJasperthecat/sub/main/sublist1.txt"
    url3 = "*****"

    all_servers = []

    def fetch_from_url(url, url_name, limit=None):
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            content = response.text.strip()

            lines = []

            # تلاش برای دیکود Base64
            try:
                padding = '=' * (-len(content) % 4)
                decoded = base64.b64decode(content + padding)
                decoded_text = decoded.decode("utf-8")

                if any(
                    proto in decoded_text.lower()
                    for proto in (
                        "vmess://",
                        "vless://",
                        "trojan://",
                        "ss://",
                        "ssr://",
                        "hy2://",
                        "hysteria://",
                        "tuic://"
                    )
                ):
                    lines = [
                        line.strip()
                        for line in decoded_text.splitlines()
                        if line.strip()
                    ]
                    print(f"✅ {url_name} (Base64) دریافت شد.")
                else:
                    raise Exception("Not subscription format")

            except Exception:
                lines = [
                    line.strip()
                    for line in content.splitlines()
                    if line.strip()
                ]
                print(f"✅ {url_name} (Text) دریافت شد.")

            if limit is not None:
                return lines[:limit]

            return lines

        except requests.RequestException as e:
            print(f"❌ خطا در دریافت {url_name}:")
            print(e)
            return []

        except Exception as e:
            print(f"❌ خطا در پردازش {url_name}:")
            print(e)
            return []

    # لینک اول بدون محدودیت
    servers1 = fetch_from_url(url1, "url1")

    # لینک دوم و سوم محدود
    servers2 = fetch_from_url(url2, "url2", limit=10)
    servers3 = fetch_from_url(url3, "url3", limit=10)

    all_servers.extend(servers1)
    all_servers.extend(servers2)
    all_servers.extend(servers3)

    # حذف موارد تکراری
    all_servers = list(dict.fromkeys(all_servers))

    if not all_servers:
        print("❗ هیچ کانفیگی دریافت نشد.")
        return

    try:
        with open("servers.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(all_servers))

        print(
            f"✅ تعداد {len(all_servers)} کانفیگ در فایل servers.txt ذخیره شد."
        )

    except Exception as e:
        print(f"❌ خطا در ذخیره فایل:")
        print(e)

if __name__ == "__main__":
    fetch_servers()
