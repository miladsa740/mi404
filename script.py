import requests

def fetch_servers():
    url1 = "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY_RAW.txt"
    url2 = "https://raw.githubusercontent.com/DiDiten/HiN-VPN/main/subscription/normal/mix"

    try:
        response1 = requests.get(url1, timeout=10)
        response1.raise_for_status()  # اگر status code غیر از 200 باشه، خطا می‌ندازه
    except requests.RequestException as e:
        print(f"خطا در دریافت داده از url1:\n{e}")
        return

    try:
        response2 = requests.get(url2, timeout=10)
        response2.raise_for_status()
    except requests.RequestException as e:
        print(f"خطا در دریافت داده از url2:\n{e}")
        return

    try:
        servers1 = response1.text.strip().splitlines()[:50]
        servers2 = response2.text.strip().splitlines()[:50]

        all_servers = servers1 + servers2

        with open("servers.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(all_servers))

        print("✅ سرورها با موفقیت دریافت و ذخیره شدند.")

    except Exception as e:
        print(f"❌ خطایی در پردازش یا ذخیره‌سازی داده‌ها رخ داد:\n{e}")

if __name__ == "__main__":
    fetch_servers()
