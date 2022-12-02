# 將景點資料存放到資料庫中
# 景點圖片的處理，我們會過濾資料中，不是 JPG 或 PNG 的檔案，
# 景點的每張圖片網址都必須被想辦法儲存在資料庫中。
import json
import mysql.connector

with open("taipei-attractions.json", mode="r", encoding="utf-8") as file:
    data = json.load(file)
# 共58筆資料
data = data["result"]["results"]

# print(data[0])                # []
# print(data[0]["file"])        # str    key-value


# file處理
for e in data:
    # 格式問題
    # 先統一大小寫
    e["file"] = e["file"].replace(".JPG", ".jpg")
    # https連結字串異常修正 .jpghttps .jpg https
    e["file"] = e["file"].replace(".jpghttps", ".jpg https")
    # print(e["file"])    # str

    # 篩選資料
    # 只留 JPG 或 PNG檔案
    list_file = e["file"].split()
    # print(list_file)                  # [ ] 含 jpg.mp3.flv陣列

    filterDatas = []
    for x in list_file:
        if ".jpg" in x:
            filterDatas.append(x)
    print(filterDatas)

    # file不能有, mysql操作會報錯，轉換為兩個空格
    # str_filterDatas = '  '.join(str(v) for v in filterDatas)
    # # print(str_filterDatas)
    # e["file"] = str_filterDatas


try:
    # 連結dbtaipei_day_trip資料庫
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="dbtaipei_day_trip"
    )
    # 對資料庫進行操作
    # 使用指標  cursor()
    cursor = db.cursor()

    for e in data:
        # 資料庫執行
        # sql = f"""INSERT INTO data (rate, direction, name, date,
        # longitude, REF_WP, avBegin, langinfo, MRT, SERIAL_NO, RowNumber,
        # CAT, MEMO_TIME, POI, file, idpt, latitude, description, _id, avEnd,
        # address) VALUES ({value})"""
        sql = f"""INSERT INTO data (
            rate, direction, name, date, longitude, 
            REF_WP, avBegin, langinfo, MRT, SERIAL_NO, 
            RowNumber, CAT,  MEMO_TIME, POI, file, 
            idpt, latitude, description, _id, avEnd, address) 
            VALUES (
            '{e["rate"]}' , '{e["direction"]}', '{e["name"]}', '{e["date"]}', '{e["longitude"]}', 
            '{e["REF_WP"]}', '{e["avBegin"]}', '{e["langinfo"]}', '{e["MRT"]}', '{e["SERIAL_NO"]}', 
            '{e["RowNumber"]}', '{e["CAT"]}', '{e["MEMO_TIME"]}', '{e["POI"]}', '{e["file"]}', 
            '{e["idpt"]}', '{e["latitude"]}', '{e["description"]}', '{e["_id"]}', '{e["avEnd"]}', '{e["address"]}')"""

        cursor.execute(sql)
        db.commit()
    print("ok")

except Exception as err:
    print(err)
