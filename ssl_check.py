import socket
import ssl
import requests
import json
import os
from datetime import datetime, timezone
from cryptography import x509
from cryptography.hazmat.backends import default_backend

# ==========================
# Config
# ==========================
SITES_FILE = "sites.txt"
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_IDS = ["-100456456177", "-10024564564383"]  # list of chat IDs
LOG_FILE = "ssl_checker.log"
ALERT_THRESHOLD = 5   # alert when certificate has 5 or fewer days left

# ==========================
# Telegram notify
# ==========================
def send_telegram(msg: str):
    for chat_id in TELEGRAM_CHAT_IDS:   # loop through all chat IDs
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": chat_id, "text": msg, "parse_mode": "Markdown"})
        except Exception as e:
            print(f"Telegram send failed for {chat_id}: {e}")

# ==========================
# SSL expiry checker
# ==========================
def get_ssl_expiry(hostname, port=443, retries=2):
    for _ in range(retries):
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                    der_cert = ssock.getpeercert(binary_form=True)
                    cert = x509.load_der_x509_certificate(der_cert, default_backend())
                    expiry_date = cert.not_valid_after.replace(tzinfo=timezone.utc)
                    return expiry_date
        except:
            continue
    return None

# ==========================
# Write last 2 runs nicely
# ==========================
def update_log(run_results):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    block = [f"Run: {now}\n"]
    for site, status in run_results:
        block.append(f"{site} → {status}\n")
    block.append("\n")

    # Read previous log blocks
    old_blocks = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            content = f.read().strip()
            if content:
                old_blocks = content.split("\n\n")

    # Keep only the latest 2 runs
    all_blocks = [("\n".join(block)).strip()] + old_blocks
    all_blocks = all_blocks[:2]

    with open(LOG_FILE, "w") as f:
        f.write("\n\n".join(all_blocks))

# ==========================
# Main
# ==========================
def main():
    alerts = []
    run_results = []

    try:
        with open(SITES_FILE, "r") as f:
            sites = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        send_telegram(f"❌ SSL Checker failed: '{SITES_FILE}' not found.")
        return

    for site in sites:
        expiry = get_ssl_expiry(site)
        if expiry:
            now = datetime.now(timezone.utc)
            days_left = (expiry - now).days

            if days_left <= ALERT_THRESHOLD:
                alerts.append(f"{site} → {days_left} days left (expires {expiry.date()})")
                run_results.append((site, f"{days_left} days left (ALERT)"))
            else:
                run_results.append((site, f"{days_left} days left (OK)"))
        else:
            run_results.append((site, "❌ SSL check failed"))

    # Case 1: Some sites expiring soon
    if alerts:
        alert_msg = "🚨 *SSL Expiry Alert* 🚨\n\n" + "\n".join(alerts)
        send_telegram(alert_msg)
    else:
    # Case 2: No expiry problem
        run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = f"✅ Last run at {run_time}\nNo expiring SSL certificates found in 5 days."
        send_telegram(msg)
        run_results.append(("All sites", "No expiry within 5 days"))


    update_log(run_results)

if __name__ == "__main__":
    main()