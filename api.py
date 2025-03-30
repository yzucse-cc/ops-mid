import csv
import requests
import base64
import json

# API網址，用static.py產生的檔案
url = "https://api.github.com/repos/yzucse-cc/ops-mid/contents/static.json"

# 拿資料
response = requests.get(url)
response.encoding = response.apparent_encoding

# 轉json
data = response.json()

if response.status_code == 200:
    data = response.json()  # 轉json
    base64_content = data.get("content", "").strip()  # 取得 content

    if base64_content:
        decoded_content = base64.b64decode(base64_content).decode("utf-8")  # 解碼 Base64
        data = json.loads(decoded_content)  # 轉json

    if data:    # 如果有資料
        header = data[0].keys() # 取出標題列

        # 寫入csv
        with open("api.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            writer.writerows(data)
        print("json->csv done")

    else:
        print("no data in json")

else:
    print("no json found")
