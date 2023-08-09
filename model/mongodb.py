from pymongo import MongoClient
import datetime

stockDB = "mydb"
dname = "test-good1"

def constructor_stock():
    client = MongoClient("mongodb://dolimit0115:xyz19930609@ac-xmnplkn-shard-00-00.en5twjf.mongodb.net:27017,ac-xmnplkn-shard-00-01.en5twjf.mongodb.net:27017,ac-xmnplkn-shard-00-02.en5twjf.mongodb.net:27017/?ssl=true&replicaSet=atlas-g9xd4h-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client[stockDB]
    return db

# 更新暫存的股票

def update_the_stock(user_name, stockNumber,condition,target_price):
    db = constructor_stock()
    collect = db[user_name]
    collect.update_many({"favorite_stock":stockNumber},{"$set" : {"condition" : condition,"price" : target_price}})
    content = f"股票{stockNumber}更新成功囉！"
    return content

# 新增使用者的股票

def write_stock(userID,user_name,stockNumber,condition,target_price):
    db = constructor_stock()
    collect = db[user_name]
    is_exit = collect.find_one({"favorite_stock":stockNumber})
    if is_exit != None:
        content = update_the_stock(user_name,stockNumber,condition,target_price)
        return content
    
    else:
        collect.insert_one({
            "userID":userID,
            "favorite_stock":stockNumber,
            "condition" : condition,
            "price" : target_price,
            "tag" : "stock",
            "date_info" : datetime.datetime.now()

        })

        return f"{stockNumber} 已經登錄到你的股票清單囉！還不快感謝莉飄兒大人！"
