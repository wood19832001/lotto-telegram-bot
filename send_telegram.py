import os
import requests
import pandas as pd

# ✅ 讀取環境變數（來自 GitHub Secrets）
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ✅ 檢查 `BOT_TOKEN` 和 `CHAT_ID` 是否設定
if not BOT_TOKEN:
    print("❌ 錯誤：BOT_TOKEN 未設定，請檢查 GitHub Secrets！")
    exit()
if not CHAT_ID:
    print("❌ 錯誤：CHAT_ID 未設定，請檢查 GitHub Secrets！")
    exit()

# ✅ **正確的 Telegram API URL**
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# ✅ 確保 GitHub Actions 可以找到 Excel 檔案
file_path = "Lotto_Data_New.xlsx" if os.getenv("GITHUB_ACTIONS") else "C:/Users/user/lotto-auto/Lotto_Data_New.xlsx"

# ✅ 確保 Excel 檔案存在
if not os.path.exists(file_path):
    print(f"❌ 錯誤：找不到 Excel 檔案 {file_path}，請確認檔案是否已上傳！")
    exit()

# ✅ 讀取 Excel 檔案，確保 header=None 避免把第一行當標題
try:
    df = pd.read_excel(file_path, sheet_name="最佳號碼", header=None, engine="openpyxl")
except Exception as e:
    print(f"❌ 錯誤：讀取 Excel 失敗！\n{str(e)}")
    exit()

# ✅ **確保數據格式正確，移除非數字欄位**
df = df.select_dtypes(include=["number"])  # 只保留數字列
df = df.apply(pd.to_numeric, errors='coerce')  # 轉換為數字，避免錯誤

# ✅ 取得最後一行數據（確保是 6 個普通號碼 + 1 個特別號）
latest_numbers = df.iloc[-1].dropna().astype(int).tolist()[-7:]

# ✅ 確保數據完整（必須是 6 個普通號碼 + 1 個特別號）
if len(latest_numbers) != 7:
    print("❌ 錯誤：Excel 資料格式不正確，請確認「最佳號碼」工作表內有 6 個普通號碼 + 1 個特別號！")
    exit()

# ✅ 格式化發送的訊息（確保號碼格式正確）
message = f"🎯 最新一期六合彩最佳號碼：\n🔢 {', '.join(map(str, latest_numbers[:6]))}\n⭐ 特別號：{latest_numbers[6]}"

# ✅ 發送到 Telegram
data = {"chat_id": CHAT_ID, "text": message}
response = requests.post(TELEGRAM_API_URL, data=data)

# ✅ 確認發送結果
if response.status_code == 200:
    print("✅ 成功發送號碼到 Telegram！")
else:
    print(f"❌ 發送失敗，錯誤代碼：{response.status_code}, 錯誤訊息：{response.text}")
