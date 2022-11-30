from flask import *
# 使用 mysql-connector-python 套件連結資料庫
import mysql.connector

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


# 連線資料庫
db = mysql.connector.connect(
    host="localhost",
    user="awstest",
    password="a12345678",
    database="dbtaipei_day_trip"
)

# 對資料庫進行操作
# 使用指標  cursor()
cursor = db.cursor()


# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


# 旅遊景點API
# GET/api/attractions   取得景點資料列表
# page      min:0  取得分頁，每頁12筆資料
# keyword   完全對比景點分類，模糊對比景點名稱，沒有給定不做篩選
@app.route("/api/attractions", methods=["GET"])
def api_attractions():
    cursor = db.cursor(dictionary=True)
    keyword = request.args.get("keyword")
    nowPage = request.args.get("page")

    # 錯誤訊息
    # str.isdigit() 可以判斷字串中是否都是數字 ( 不能包含英文、空白或符號 )
    # 小數點,-也會被視為符號
    if (nowPage == None or nowPage.isdigit() == False):
        return jsonify({
            "error": "true",
            "message": "page需為數字"
        }), 400

    # query string 為str
    nowPage = int(nowPage)

    try:
        sql = f"SELECT * FROM data WHERE CAT = '{keyword}' or name LIKE '%{keyword}%' "
        cursor.execute(sql)
        datas = cursor.fetchall()

        lenDatas = len(datas)  # 總抓取資料長度
        if (lenDatas > (nowPage + 1) * 12):
            nextPage = 1
        else:
            nextPage = None

        rtnData = {"nextPage": nextPage, "data": []}

        # nowPage = 0  (0,11)
        # nowPage = 1  (12,23)...
        # 塞入指定需要資料 為datas index = (nowPage *12 ~ nowPage *12 +11)
        for idx, data in enumerate(datas):
            # 判斷需要的datas index
            # nowPage = 0  (0,11)
            minIndex = nowPage * 12
            maxIndex = nowPage * 12 + 11

            # nowPage = 1   lenDatas = 18
            # 會取出(datas[12] ~ datas[17])
            if maxIndex > lenDatas:
                maxIndex = lenDatas - 1

            if (idx >= minIndex and idx <= maxIndex):
                filterData = {
                    "id": data["_id"],
                    "name": data["name"],
                    "category": data["CAT"],
                    "description": data["description"],
                    "address": data["address"],
                    "transport": data["direction"],
                    "mrt": data["MRT"],
                    "lat": data["latitude"],
                    "lng": data["longitude"],
                    "images": data["file"]
                }
                # 每跑完一次迴圈，資料裝進rtnData["data"]裡面一次
                rtnData["data"].append(filterData)
        return jsonify(rtnData)

    except Exception as err:
        print(err)
        return jsonify(
            {
                "error": "true",
                "message": "伺服器內部錯誤"
            }
        ), 500


# 旅遊景點API
# GET/api/attraction/{attractionId}  根據景點編號取得景點資料
# query string      attractionId 景點編號
# 網址參考: http://140.112.3.5:3000/api/attraction/10
@ app.route("/api/attraction/<attractionId>", methods=["GET"])
def attractionId(attractionId):
    cursor = db.cursor(dictionary=True)

    sql_1 = "SELECT COUNT(*) FROM data"
    cursor.execute(sql_1)
    dataNum = cursor.fetchone()
    dataNum = dataNum["COUNT(*)"]        # 58

    try:
        # str.isdigit() 可以判斷字串中是否都是數字 ( 不能包含英文、空白或符號 )
        # 小數點,-也會被視為符號
        if attractionId.isdigit() == False:
            pass
        elif int(attractionId) >= 1 and int(attractionId) <= dataNum:
            sql_2 = f"SELECT * FROM data WHERE _id = '{attractionId}' "
            cursor.execute(sql_2)
            data = cursor.fetchone()
            # print(data)
            return jsonify(
                {
                    "data": {
                        "id": data["_id"],
                        "name": data["name"],
                        "category": data["CAT"],
                        "description": data["description"],
                        "address": data["address"],
                        "transport": data["direction"],
                        "mrt": data["MRT"],
                        "lat": data["latitude"],
                        "lng": data["longitude"],
                        "images": data["file"]
                    }
                }
            ), 200
        return jsonify(
            {
                "error": "true",
                "message": "景點編號不正確"
            }
        ), 400
    except Exception as err:
        print(err)
        return jsonify(
            {
                "error": "true",
                "message": "伺服器內部錯誤"
            }
        ), 500


#  旅遊景點分類
# GET/api/categories  取得景點分類名稱列表
@ app.route("/api/categories")
def categories():
    try:
        sql = "SELECT DISTINCT CAT FROM data "
        cursor.execute(sql)
        datas = cursor.fetchall()
        # print(datas)
        categories = []
        for data in datas:
            # print(e)
            categories += data
        # print(categories)

        return jsonify(
            {
                "data": categories
            }
        ), 200
    except Exception as err:
        print(err)
        return jsonify(
            {
                "error": "true",
                "message": "伺服器內部錯誤"
            }
        ), 500


app.run(port=3000, debug=True, host="0.0.0.0")
