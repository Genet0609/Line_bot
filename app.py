from line_bot_api import *
from events.basic import *
from events.oil import*
from events.msg_template import*
import datetime , re , twstock

app = Flask(__name__)

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

@handler.add(MessageEvent,message=TextMessage)
def handler_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    uid = profile.user_id
    message_text = str(event.message.text).lower()
    msg = str(event.message.text).upper().strip()
    emsg = event.message.text

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

    if message_text == "@股價查詢":
        line_bot_api.push_message(uid,
                TextSendMessage("要輸入 # + 股票代號 喔！"))
        
    #查詢股價功能

    if re.match("想知道股價[0-9]",msg):
        stockNumber = msg[2:6]
        btn_msg = stock_reply_other(stockNumber)
        line_bot_api.push_message(uid, btn_msg)
        return 0
    
    if(emsg.startswith("#")):
        text = emsg[1:]
        content = ""

        stock_rt = twstock.realtime.get(text)
        the_datetime = datetime.datetime.fromtimestamp(stock_rt["timestamp"]+8*60*60)
        the_time = the_datetime.strftime("%H:%M:%S")

        content += "%s (%s) %s\n" %(
            stock_rt["info"]["name"],
            stock_rt["info"]["code"],
            the_time)
        
        content += "現價: %s / 開盤: %s\n" %(
            stock_rt["realtime"]["latest_trade_price"],
            stock_rt["realtime"]["open"]
        )

        content += "最高: %s / 最低: %s\n" %(
            stock_rt["realtime"]["high"],
            stock_rt["realtime"]["low"]
        )

        content += "量: %s\n" %(
            stock_rt["realtime"]["accumlate_trade_volume"],
        )

        stock = twstock.Stock(text)
        content += "-----\n"
        content += "最近五日價格: \n"
        price5 = stock.price[-5:][::-1]
        date5 = stock.date[-5:][::-1]
        for i in range (len(price5)):
            content += "[%s] %s\n" %(date5[i].strftime("%Y-%m-%d"),price5[i])
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )

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