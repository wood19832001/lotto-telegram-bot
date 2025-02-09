import requests
import pandas as pd

# ✅ 確保 header=None 避免把第一行當標題
import os

# 確保程式可以在 GitHub Actions 運行
file_path = "Lotto_Data_New.xlsx" if os.getenv("GITHUB_ACTIONS") else "C:/Users/user/lotto-auto/Lotto_Data_New.xlsx"

df = pd.read_excel(file_path, sheet_name="最佳號碼", header=None, engine="openpyxl")


# ✅ 確保數據完整
if len(latest_numbers) < 7:
    print("⚠ 錯誤：Google Sheets 內的數據不足，請確認資料完整！")
    exit()

# ✅ 格式化發送的訊息
message = f"🎯 最新一期六合彩最佳號碼：\n🔢 {', '.join(map(str, latest_numbers[:6]))}\n⭐ 特別號：{latest_numbers[6]}"
print(f"📤 發送訊息到 Telegram：\n{message}")  # 🛠️ 偵錯用

# ✅ 發送到 Telegram
TELEGRAM_API_URL = f"https://api.telegram.org/botos.getenv("BOT_TOKEN")/sendMessage"
data = {"chat_id": os.getenv("CHAT_ID"), "text": message}
response = requests.post(TELEGRAM_API_URL, data=data)

print(f"📡 伺服器回應：{response.status_code}")  # 🛠️ 偵錯用

if response.status_code == 200:
    print("✅ 成功發送號碼到 Telegram！")
else:
    print(f"❌ 發送失敗，錯誤代碼：{response.status_code}")
