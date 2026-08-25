#!/bin/bash
# Install birthday cron for Kong Da Ge (5/31 each year)
CRON_LINE="0 0 31 5 * /bin/echo '🎂 今天是孔大哥（峯哥）生日！記得給他祝福 🎂' >> ~/Desktop/reminder.txt"

# Get current crontab, remove any existing birthday cron, add new one
(crontab -l 2>/dev/null | grep -v "孔大哥" | grep -v "birthday"; echo "$CRON_LINE") | crontab -

echo "Birthday cron installed. Verifying..."
crontab -l | grep -E "孔大哥|birthday" || echo "WARNING: Birthday cron still not found!"