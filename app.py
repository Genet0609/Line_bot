from line_bot_api import *
from events.basic import *
from events.oil import*
from events.msg_template import*
from events.EXRate import*
from model.mongodb import*
import datetime , re , twstock
import schedule
import time

app = Flask(__name__)

# 抓取使用者關心的股票
def cache_users_stock():
    db = constructor_stock()
    nameList = db.list_collection_names()
    users = []
    for i in range(len(nameList)):
        collect = db [nameList[i]]
        cel = list(collect.find({"tag":"stock"}))
        users.append(cel)
    return users

@app.route("/callback",methods = ["POST"])
def callback():

    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body,signature)
    except IndentationError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handler_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id
    message_text = str(event.message.text).lower()
    msg = str(event.message.text).upper().strip()
    emsg = event.message.text
    user_name = profile.display_name

    stockNumber = None

    ##### 選單 #####

    if message_text == '@使用說明':
        #about_us_event(event)
        Usage(event)

    if message_text == '@油價':
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )

    ##### 股價 #####

    if message_text == "@股票":
        line_bot_api.push_message(uid,
                TextSendMessage("@股票 之後，要輸入 # + 股票代號 喔！"))
    
    
        
#股票查詢
    if re.match("想知道股價[0-9]", msg):
        stockNumber = msg[5:9]
        btn_msg = stock_reply_other(stockNumber)
        line_bot_api.push_message(uid, btn_msg)
        return 0

    if re.match("關注[0-9]{4}[<>][0-9]", msg):
        stockNumber = msg[2:6]
        line_bot_api.push_message(uid, TextSendMessage("加入股票代號"+stockNumber))
        content = write_my_stock(uid,user_name,stockNumber,msg[6:7],msg[7:])
        line_bot_api.push_message(uid, TextSendMessage(content))
        return 0
    
    if re.match("股票清單",msg):
        line_bot_api.push_message(uid,TextSendMessage("在幫你查詢股票囉！"))
        content = show_stock_setting(user_name,uid)
        line_bot_api.push_message(uid,TextSendMessage(content))
        return 0
    
    #刪除存在資料庫裏面的股票
    if re.match('刪除[0-9]{4}',msg):
        content = delete_my_stock(user_name,msg[2:])
        line_bot_api.push_message(uid, TextSendMessage(content))
        return 0
    #清空存在資料庫裏面的股票
    if re.match('清空股票',msg):
        content = delete_my_allstock(user_name,uid)
        line_bot_api.push_message(uid, TextSendMessage(content))
        return 0
    
    ######################股價提醒##################
    if re.match("關閉提醒", msg):
        import schedule
        schedule.clear()
        line_bot_api.push_message(uid,TextSendMessage("那我就不提醒你啦！"))

    if re.match("股價提醒", msg):
        import schedule
        import time
        # 查看當前股價
        def look_stock_price(stock, condition, price, userID):
            print(userID)
            url = 'https://tw.stock.yahoo.com/q/q?s=' + stock
            list_req = requests.get(url)
            soup = BeautifulSoup(list_req.content, "html.parser")
            getstock= soup.findAll('span')[11].text
            content = stock + "當前股市價格為: " +  getstock
            if condition == '<':
                content += "\n篩選條件為: < "+ price
                if float(getstock) < float(price):
                    content += "\n符合" + getstock + " < " + price + "的篩選條件"
                    line_bot_api.push_message(userID, TextSendMessage(text=content))
            elif condition == '>':
                content += "\n篩選條件為: > "+ price
                if float(getstock) > float(price):
                    content += "\n符合" + getstock + " > " + price + "的篩選條件"
                    line_bot_api.push_message(userID, TextSendMessage(text=content))
            elif condition == "=":
                content += "\n篩選條件為: = "+ price
                if float(getstock) == float(price):
                    content += "\n符合" + getstock + " = " + price + "的篩選條件"
                    line_bot_api.push_message(userID, TextSendMessage(text=content))
        def job():
            print('HH')
            line_bot_api.push_message(uid,TextSendMessage("買囉、買囉、買囉！"))
            dataList = cache_users_stock()
            # print(dataList)
            for i in range(len(dataList)):
                for k in range(len(dataList[i])):
                    # print(dataList[i][k])
                    look_stock_price(dataList[i][k]['favorite_stock'], dataList[i][k]['condition'], dataList[i][k]['price'], dataList[i][k]['userID'])
        schedule.every(5).seconds.do(job).tag('daily-tasks-stock'+uid,'second') #每10秒執行一次
        #schedule.every().hour.do(job) #每小時執行一次
        #schedule.every().day.at("17:19").do(job) #每天9點30執行一次
        #schedule.every().monday.do(job) #每週一執行一次
        #schedule.every().wednesday.at("14:45").do(job) #每週三14點45執行一次
        # 無窮迴圈
        while True: 
            schedule.run_pending()
            time.sleep(1)
    
    if (emsg.startswith('#')):
        text = emsg[1:]
        content =''

        stock_rt = twstock.realtime.get(text)
        my_datetime = datetime.datetime.fromtimestamp(stock_rt['timestamp']+8*60*60)
        my_time = my_datetime.strftime('%H:%M:%S')

        content +='%s (%s) %s\n' % (
            stock_rt['info']['name'],
            stock_rt['info']['code'],
            my_time)
        
        content += '現價: %s / 開盤: %s\n'%(
            stock_rt['realtime']['latest_trade_price'],
            stock_rt['realtime']['open'])
        content += '最高: %s / 最低:%s\n'%(
            stock_rt['realtime']['high'],
            stock_rt['realtime']['low'])
        
        content += '量: %s\n'%(stock_rt['realtime']['accumulate_trade_volume'])

        stock = twstock.Stock(text)
        content += '-----\n'
        content += '最近五日價格: \n'
        price5 = stock.price[-5:][::-1]
        date5 = stock.date[-5:][::-1]
        for i in range(len(price5)):
            content += '[%s] %s\n' % (date5[i].strftime("%Y-%m-%d"), price5[i])
        line_bot_api.reply_message(
            event.reply_token, 
            TextSendMessage(text=content)
        )


    # 匯率區 #

    if message_text == '@匯率':
        message = show_Button()
        line_bot_api.reply_message(event.reply_token, message)
        line_bot_api.push_message(uid,
                TextSendMessage("可以輸入 換匯JPY/CNY/100 試試看喔！"))

    if re.match("幣別種類", emsg):
        message = show_Button()
        line_bot_api.reply_message(event.reply_token, message)

    if re.match("查詢匯率[A-Z]",msg):
        msg=msg[4:]
        content = show_Button()
        line_bot_api.reply_message(event.reply_token,message)
    
    if re.match("換匯[A-Z]{3}/[A-Z{3}]",msg):
        line_bot_api.push_message(uid,TextSendMessage("幫你換錢錢！"))
        content = getExchangeRate(msg)
        line_bot_api.push_message(uid,TextSendMessage(content))

# 封鎖與加入好友

user_status = {}

@handler.add(FollowEvent)
def handler_follow(event):
    welcome_message = about_us_event(event)
    user_id = event.source.user_id

    if user_status.get(user_id) == 1:
        block_message = """哇哈哈！莉飄兒大人果然還是最好的，對吧？"""
        line_bot_api.push_message(user_id, TextSendMessage(text=block_message))

    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))
    
    user_status[user_id] = 0

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id
    # 將使用者狀態設置為 1（解除封鎖後再重新加入好友）
    user_status[user_id] = 1



if __name__ == '__main__':
    app.run()