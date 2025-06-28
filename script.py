import requests

def fetch_servers():
    # لینک‌های جدید
    url1 = "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/V2RAY.txt"
    url2 = "https://raw.githubusercontent.com/DiDiten/HiN-VPN/main/subscription/normal/mix"

    # دریافت داده‌ها
    response1 = requests.get(url1)
    response2 = requests.get(url2)

    # بررسی وضعیت
    if response1.status_code == 200 and response2.status_code == 200:
        # پردازش داده‌ها
        servers1 = response1.text.strip().splitlines()[:50]  # 50 سرور اول
        servers1 = response1.text.strip().splitlines()[:50]  # 50 سرور اول

        # ترکیب داده‌ها
        all_servers = servers1 + servers2

        # ذخیره به فایل
        with open("servers.txt", "w") as f:
            f.write("\n".join(all_servers))
        print("Servers fetched and saved successfully.")
    else:
        print("Error fetching server data.")

if __name__ == "__main__":
    fetch_servers()
