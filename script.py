import requests

def check_ping(server):
    """
    استفاده از سرویس پینگ آنلاین برای بررسی پینگ یک سرور.
    """
    try:
        api_url = f"https://ping.sck.link/api/ping?host={server}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            ping = data.get('ping', None)  # دریافت مقدار پینگ از پاسخ JSON
            if ping is not None:
                return float(ping)
        return None
    except Exception as e:
        print(f"Error pinging {server}: {e}")
    return None


def fetch_servers():
    # لینک‌های سرورها
    url1 = "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ss.txt"
    url2 = "https://raw.githubusercontent.com/miladsa740/Free/main/Free"
    
    # دریافت داده‌ها از لینک‌ها
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    
    if response1.status_code == 200 and response2.status_code == 200:
        # پردازش سرورهای لینک اول
        servers1 = response1.text.strip().splitlines()
        selected_servers = []
        
        for server in servers1:
            # فرض می‌کنیم آدرس سرور در فرمت IP:Port است
            if ":" in server:
                ip = server.split(":")[0]
                ping = check_ping(ip)
                if ping is not None and ping < 500:  # فیلتر پینگ زیر 500 میلی‌ثانیه
                    selected_servers.append(f"{server} | Ping: {ping}ms")
            if len(selected_servers) == 20:  # محدود به 20 سرور
                break

        # ترکیب سرورها (فقط سرورهای انتخاب‌شده)
        all_servers = selected_servers

        # ذخیره سرورها در فایل
        with open("servers.txt", "w") as f:
            f.write("\n".join(all_servers))
        print("Servers with valid ping fetched and saved successfully.")
    else:
        print("Error fetching server data.")


if __name__ == "__main__":
    fetch_servers()