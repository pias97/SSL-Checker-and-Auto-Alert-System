# SSL-Checker-and-Auto-Alert-System
A ready-to-use Python script that checks when SSL certificates will expire, sends alerts to Telegram, and gives daily confirmation messages.
---

## Features
- ✅ Daily SSL expiry checks for multiple endpoints.
- ✅ Alerts 5 days before expiry + on expiry, and will keep on alerting until SSL renewal.
- ✅ Telegram notifications for real-time monitoring.
- ✅ Store logs for the last 2 runs.


---

## Demo Endpoints
- youtube.com
- google.com
- github.com

---

## Setup

### Clone the repo
```bash
git clone https://github.com/pias97/SSL-Checker-and-Auto-Alert-System.git
cd SSL-Checker-and-Auto-Alert-System
```

### Create virtual environment and activate (For first time only, ` run_ssl_check.sh` file will do it repeatedly next time)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure your Telegram bot credentials
Edit `ssl_checker.py` and add your `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`.

## Usage
You can just run this command to see the instant result.
```bash
python3 ssl_checker.py
```
For repeating daily, follow this procedure
```bash
crontab -l
```
Navigate to the EOF and add `0 5 * * * /home/ubuntu/monitoring/ssl-alert/run_ssl_check.sh` It will keep repeating the script and send alerts. 
