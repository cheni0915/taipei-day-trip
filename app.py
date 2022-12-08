from flask import *
# 使用 mysql-connector-python 套件連結資料庫
import mysql.connector
import mysql.connector.pooling

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


# 使用connetcion pool連線
dbpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,   # 是否重置資料庫connection pool
    host="localhost",
    user="awstest",
    password="a12345678",
    database="dbtaipei_day_trip"
)


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
    keyword = request.args.get("keyword")
    nowPage = request.args.get("page")
    # 錯誤訊息
    # str.isdigit() 可以判斷字串中是否都是數字 ( 不能包含英文、空白或符號 )
    # 小數點,-也會被視為符號
    if (nowPage == None or nowPage.isdigit() == False):
        return jsonify({
            "error": "true",
            "message": "page輸入錯誤"
        }), 400

    # query string 為str
    nowPage = int(nowPage)

    try:
        # 對資料庫進行操作
        db = dbpool.get_connection()
        cursor = db.cursor(dictionary=True)

        # 沒有給定keyword => 不做篩選
        if keyword == None:
            # 要使用分頁的概念，不會把全部資料一次抓出來，要limit數量
            # limit 0,12    抓出 id 1~12的資料
            # limit 12,12   抓出 id 13~24的資料
            minIndex = nowPage * 12
            limit = 12
            sql_1 = "SELECT * FROM data LIMIT %s,%s"
            val_1 = (minIndex, limit)
            cursor.execute(sql_1, val_1)
            datas = cursor.fetchall()
            lenDatas = len(datas)

            # 搜尋到的資料筆數
            sql_3 = "SELECT COUNT(*) FROM data"
            cursor.execute(sql_3)
            dataCount = cursor.fetchone()
            dataCount = dataCount["COUNT(*)"]

        else:
            minIndex = nowPage * 12
            limit = 12
            sql_2 = f"SELECT * FROM data WHERE CAT = '{keyword}' or name LIKE '%{keyword}%' LIMIT {minIndex},{limit} "
            cursor.execute(sql_2)
            datas = cursor.fetchall()
            lenDatas = len(datas)

            # 搜尋到的資料筆數
            sql_4 = f"SELECT COUNT(*) FROM data WHERE CAT = '{keyword}' or name LIKE '%{keyword}%'"
            cursor.execute(sql_4)
            dataCount = cursor.fetchone()
            dataCount = dataCount["COUNT(*)"]

        # 搜尋到的資料筆數 > 12 => nextPage = 1
        if (dataCount > (nowPage + 1) * 12):
            nextPage = 1
        else:
            nextPage = None

        rtnData = {"nextPage": nextPage, "data": []}

        # 每個分頁最多12筆資料
        for data in datas:
            # images 要以 array string 形式呈現
            data["file"] = data["file"].split()

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

        cursor.close()
        return jsonify(rtnData)

    except Exception as err:
        print(err)
        return jsonify(
            {
                "error": "true",
                "message": "伺服器內部錯誤"
            }
        ), 500
    finally:
        db.close()


# 旅遊景點API
# GET/api/attraction/{attractionId}  根據景點編號取得景點資料
# query string      attractionId 景點編號
# 網址參考: http://140.112.3.5:3000/api/attraction/10
@ app.route("/api/attraction/<attractionId>", methods=["GET"])
def attractionId(attractionId):
    try:
        # 對資料庫進行操作
        db = dbpool.get_connection()
        cursor = db.cursor(dictionary=True)

        sql_1 = "SELECT COUNT(*) FROM data"
        cursor.execute(sql_1)
        dataCount = cursor.fetchone()
        dataCount = dataCount["COUNT(*)"]        # 58

        # str.isdigit() 可以判斷字串中是否都是數字 ( 不能包含英文、空白或符號 )
        # 小數點,-也會被視為符號
        if attractionId.isdigit() == False:
            pass
        elif int(attractionId) >= 1 and int(attractionId) <= dataCount:
            sql_2 = f"SELECT * FROM data WHERE _id = '{attractionId}' "
            cursor.execute(sql_2)
            data = cursor.fetchone()

            # images 要以 array string 形式呈現
            data["file"] = data["file"].split()
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

        cursor.close()
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
    finally:
        db.close()


#  旅遊景點分類
# GET/api/categories  取得景點分類名稱列表
@ app.route("/api/categories")
def categories():
    try:
        # 對資料庫進行操作
        db = dbpool.get_connection()
        cursor = db.cursor()

        sql = "SELECT DISTINCT CAT FROM data "
        cursor.execute(sql)
        datas = cursor.fetchall()
        # print(datas)

        categories = []
        for data in datas:
            # print(e)
            categories += data
        # print(categories)

        cursor.close()
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
    finally:
        db.close()


app.run(port=3000, debug=True, host="0.0.0.0")
