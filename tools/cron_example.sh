#!/bin/bash
#
# Cron Job Script: Trigger Daily/Weekly Analytics Reports
# --------------------------------------------------------
# Add in crontab (runs every day at 9am):
# 0 9 * * * /path/to/cron_example.sh >> /var/log/brandnbloom-cron.log 2>&1
#
# Environment variables (set in your server):
#   BNB_API_URL="https://your-api-url"
#   BNB_HANDLE="brandnbloom_demo"
#   BNB_EMAIL="demo@example.com"
#   BNB_USER_ID="1"
#
# --------------------------------------------------------

API_URL="${BNB_API_URL:-https://your-api-url}"
HANDLE="${BNB_HANDLE:-brandnbloom_demo}"
EMAIL="${BNB_EMAIL:-demo@example.com}"
USER_ID="${BNB_USER_ID:-1}"

LOG_DATE=$(date +"%Y-%m-%d %H:%M:%S")
RETRY_COUNT=3
SLEEP_BETWEEN=5  # seconds


echo "[$LOG_DATE] Starting scheduled report trigger..."


trigger_report() {
  curl -s -o /tmp/cron_report_response.txt \
       -w "%{http_code}" \
       -X POST "$API_URL/send-report" \
       -H "Content-Type: application/json" \
       -m 20 \
       -d "{\"handle\":\"$HANDLE\",\"email\":\"$EMAIL\",\"user_id\":$USER_ID}"
}


# Retry mechanism
attempt=1
response_code=""

while [ $attempt -le $RETRY_COUNT ]; do
  echo "Attempt $attempt sending report..."

  response_code=$(trigger_report)

  if [ "$response_code" == "200" ] || [ "$response_code" == "201" ]; then
    echo "[$LOG_DATE] Report sent successfully! (HTTP $response_code)"
    exit 0
  else
    echo "[$LOG_DATE] Failed attempt $attempt (HTTP $response_code). Retrying in $SLEEP_BETWEEN seconds..."
    sleep $SLEEP_BETWEEN
  fi

  attempt=$((attempt + 1))
done


# If all attempts fail
echo "[$LOG_DATE] ERROR: All $RETRY_COUNT attempts failed. Last HTTP code: $response_code"
echo "Last response:"
cat /tmp/cron_report_response.txt

exit 1
