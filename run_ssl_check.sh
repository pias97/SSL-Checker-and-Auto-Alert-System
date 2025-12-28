#!/bin/bash
# Navigate to the project directory
cd /home/ubuntu/monitoring/ssl-alert

# Activate the Python virtual environment
source venv/bin/activate

# Write timestamp of last run in log
echo "------ Script run at $(date '+%Y-%m-%d %H:%M:%S') ------" >> ssl_checker.log

# Run the SSL checker Python script
python ssl_check.py >> ssl_checker.log 2>&1