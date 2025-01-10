import requests
import subprocess

def check_ping(server):
    """
    بررسی پینگ یک سرور.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "1", server],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode == 0:
            output = result.stdout
            # پیدا کردن زمان پینگ از خروجی
            for line in output.splitlines():
                if "time=" in line:
                    time = line.split("time=")[-1].split(" ")[0]
                    return float(time)
    except Exception as e:
        print(f"Error pinging {server}: {e}")
    return None


def fetch_servers():
    # لینک‌های سرورها
    url1 = "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/sub/splitted/ss.txt"
    url2 = "https://raw.githubusercontent.com/miladsa740/Free/main/Free"
    
    # دریافت داده‌ها
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    
    if response1.status_code == 200 and response2.status_code == 200:
        # پردازش سرورهای لینک اول
        servers1 = response1.text.strip().splitlines()
        selected_servers1 = []
        
        for server in servers1:
            # فرض می‌کنیم آدرس سرور در فرمت سرور Shadowsocks است (IP:Port)
            if ":" in server:
                ip = server.split(":")[0]
                ping = check_ping(ip)
                if ping is not None and ping < 500:
                    selected_servers1.append(server)
            if len(selected_servers1) == 20:
                break

        # پردازش سرورهای لینک دوم
        servers2 = response2.text.strip().splitlines()

        # ترکیب سرورها
        all_servers = selected_servers1 + servers2

        # ذخیره به فایل
        with open("servers.txt", "w") as f:
            f.write("\n".join(all_servers))
        print("Servers fetched and saved successfully.")
    else:
        print("Error fetching server data.")

if __name__ == "__main__":
    fetch_servers()
