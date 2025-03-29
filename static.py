import requests
from bs4 import BeautifulSoup
import json

# portal 活動查詢網址，免登入
url = "https://portalx.yzu.edu.tw/PortalSocialVB/FMain/PageActivityAll.aspx"

# 拿資料
response = requests.get(url)
response.encoding = response.apparent_encoding

# 解析內容
soup = BeautifulSoup(response.content, "html.parser")

# 定位活動列表
div_activity = soup.find(id="divPageActivityList")
if not div_activity:
    raise Exception("divPageActivityList not found")

# 定位活動列表表格
table = div_activity.find("table", class_="table_1")
if not table:
    raise Exception("table_1 not found")

rows = table.find_all("tr") # 取出每一row

# 建立表格標題行
header = [cell.get_text(separator=" ", strip=True) for cell in rows[0].find_all("td")] + ["ActID"]

rows = rows[1:] # 刪掉標題row
activities = [] # 初始化活動列表

for row in rows:
    cells = row.find_all("td")  # 取出每一column的內容
    row_data = [cell.get_text(separator=" ", strip=True) for cell in cells]

    if row_data:
        link = cells[2].find("a")   # 找有沒有活動連結
        if link:    # 如果有活動連結，把前綴刪掉，保留ActID
            row_data.append(link.get("href").replace("../FPage/FirstToPage.aspx?PassPage=ActDetail&ActID=", ""))
        else:       # 如果沒有活動連結就留空
            row_data.append("")

        activity = dict(zip(header, row_data))  # 把欄位名稱跟資料結合
        activities.append(activity)             # 加入活動列表

# 寫入json
with open("static.json", "w", encoding="utf-8") as jsonfile:
    json.dump(activities, jsonfile, ensure_ascii=False, indent=4)

print("web->json done")
