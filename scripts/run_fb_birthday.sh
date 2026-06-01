#!/bin/bash
cd /Users/bymyway/.openclaw/workspace/scripts
node fb_birthday_scraper.js >> /tmp/fb_birthday.log 2>&1
echo "[$(date)] done, exit: $?" >> /tmp/fb_birthday.log