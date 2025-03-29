import csv
import requests

# API網址，用static.py產生的檔案
url = "https://raw.githubusercontent.com/yzucse-cc/ops-mid/refs/heads/main/static.json"

# 拿資料
response = requests.get(url)
response.encoding = response.apparent_encoding

# 轉json
data = response.json()

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
