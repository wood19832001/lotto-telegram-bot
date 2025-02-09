import os
import requests
import pandas as pd

# ✅ 讀取環境變數（來自 GitHub Secrets）
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ✅ 確保 GitHub Actions 可以找到 Excel 檔案
file_path = "Lotto_Data_New.xlsx" if os.getenv("GITHUB_ACTIONS") else "C:/Users/user/lotto-auto/Lotto_Data_New.xlsx"

# ✅ 讀取 Excel 檔案，確保 header=None 避免把第一行當標題
df = pd.read_excel(file_path, sheet_name="最佳號碼", header=None, engine="openpyxl")

# ✅ 取得最後一行數據
latest_numbers = df.iloc[-1].tolist()

# ✅ 確保數據完整（至少有 7 個號碼）
if len(latest_numbers) < 7:
    print("⚠ 錯誤：Google Sheets 內的數據不足，請確認資料完整！")
    exit()

# ✅ 格式化發送的訊息
message = f"🎯 最新一期六合彩最佳號碼：\n🔢 {', '.join(map(str, latest_numbers[:6]))}\n⭐ 特別號：{latest_numbers[6]}"

# ✅ 確保 `BOT_TOKEN` 和 `CHAT_ID` 正確
if not BOT_TOKEN or not CHAT_ID:
    print("❌ 錯誤：BOT_TOKEN 或 CHAT_ID 未設定，請檢查 GitHub Secrets！")
    exit()

# ✅ 正確的 Telegram API URL
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# ✅ 發送到 Telegram
data = {"chat_id": CHAT_ID, "text": message}
response = requests.post(TELEGRAM_API_URL, data=data)

# ✅ 確認發送結果
if response.status_code == 200:
    print("✅ 成功發送號碼到 Telegram！")
else:
    print(f"❌ 發送失敗，錯誤代碼：{response.status_code}, 錯誤訊息：{response.text}")