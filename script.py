import requests
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# =========================
# تنظیمات
# =========================

URLS = [
    {
        "name": "blackbird",
        "url": "https://m3cz1juspe5-f-hftapxrrs17zqppw11.salisa7474-9d1.workers.dev/sub/normal/G2z%3BZ9cHEZ1%24B.%26s#%F0%9F%92%A6%20BPB%20Normal",
        "limit": None
    },
    {
        "name": "mahsa_sub_1",
        "url": "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_1.txt",
        "limit": 10
    },
    {
        "name": "mahsa_sub_2",
        "url": "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/mci/sub_2.txt",
        "limit": 10
    }
]

OUTPUT_FILE = "servers.txt"

VALID_PROTOCOLS = (
    "vless://",
    "vmess://",
    "trojan://",
    "ss://",
    "ssr://",
    "hy2://",
    "tuic://"
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# لاگ
# =========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================
# ساخت Session با Retry
# =========================

def create_session():
    session = requests.Session()

    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session

# =========================
# اعتبارسنجی کانفیگ
# =========================

def validate_server(line):
    line = line.strip()

    # خالی نباشد
    if not line:
        return False

    # طول غیرعادی نداشته باشد
    if len(line) > 5000:
        return False

    # فقط پروتکل معتبر
    if not line.startswith(VALID_PROTOCOLS):
        return False

    return True

# =========================
# دریافت داده از URL
# =========================

def fetch_from_url(session, url, name, limit=None):
    servers = []

    try:
        logging.info(f"درحال دریافت از {name}")

        response = session.get(
            url,
            headers=HEADERS,
            timeout=(5, 15)
        )

        response.raise_for_status()

        lines = response.text.splitlines()

        # حذف فاصله و خطوط خالی
        lines = [line.strip() for line in lines if line.strip()]

        # اعمال limit
        if limit is not None:
            lines = lines[:limit]

        # اعتبارسنجی
        valid_count = 0
        invalid_count = 0

        for line in lines:
            if validate_server(line):
                servers.append(line)
                valid_count += 1
            else:
                invalid_count += 1

        logging.info(
            f"{name} | معتبر: {valid_count} | نامعتبر: {invalid_count}"
        )

    except requests.exceptions.Timeout:
        logging.error(f"{name} | Timeout")

    except requests.exceptions.HTTPError as e:
        logging.error(f"{name} | HTTP Error: {e}")

    except requests.exceptions.RequestException as e:
        logging.error(f"{name} | Request Error: {e}")

    except Exception as e:
        logging.error(f"{name} | خطای ناشناخته: {e}")

    return servers

# =========================
# حذف موارد تکراری
# =========================

def remove_duplicates(data):
    return list(dict.fromkeys(data))

# =========================
# ذخیره فایل
# =========================

def save_servers(servers, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(servers))

        logging.info(
            f"{len(servers)} سرور در فایل {filename} ذخیره شد."
        )

    except Exception as e:
        logging.error(f"خطا در ذخیره فایل: {e}")

# =========================
# تابع اصلی
# =========================

def main():
    session = create_session()

    all_servers = []

    success_count = 0
    failed_count = 0

    for item in URLS:
        servers = fetch_from_url(
            session=session,
            url=item["url"],
            name=item["name"],
            limit=item["limit"]
        )

        if servers:
            success_count += 1
            all_servers.extend(servers)
        else:
            failed_count += 1

    # حذف duplicate
    all_servers = remove_duplicates(all_servers)

    if not all_servers:
        logging.warning("هیچ سروری دریافت نشد.")
        return

    save_servers(all_servers, OUTPUT_FILE)

    logging.info(f"منابع موفق: {success_count}")
    logging.info(f"منابع ناموفق: {failed_count}")
    logging.info(f"تعداد نهایی سرورها: {len(all_servers)}")

# =========================
# اجرا
# =========================

if __name__ == "__main__":
    main()
