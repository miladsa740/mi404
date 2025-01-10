import requests

def fetch_servers():
    # لینک‌های جدید
    url1 = "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt"
    url2 = "https://raw.githubusercontent.com/miladsa740/Free/main/Free"

    # دریافت داده‌ها
    response1 = requests.get(url1)
    response2 = requests.get(url2)

    # بررسی وضعیت
    if response1.status_code == 200 and response2.status_code == 200:
        # پردازش داده‌ها
        servers1 = response1.text.strip().splitlines()[:100]  # 100 سرور اول
        servers2 = response2.text.strip().splitlines()        # همه سرورهای لینک دوم

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
