from line_bot_api import *
from events.basic import *
from events.oil import*

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

    # 選單
    if message_text == '@使用說明':
        #about_us_event(event)
        Usage(event)

    if message_text == '@油價':
        content = oil_price()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )
    # 股價

    if message_text == "@股價查詢":
        line_bot_api.push_message(uid,
                TextSendMessage("要輸入 # + 股票代號 喔！"))


    
# 定義一個字典來存儲使用者的狀態，預設狀態為 0（未加入好友）
user_status = {}

@handler.add(FollowEvent)
def handler_follow(event):
    welcome_message = """哈囉！你好哇！恭喜你已經成為了莉飄兒大人的部下！"""
    user_id = event.source.user_id
    
    # 若使用者狀態為 1（解除封鎖後再重新加入好友），則發送特定訊息
    if user_status.get(user_id) == 1:
        block_message = """哇哈哈！莉飄兒大人果然還是最好的，對吧？"""
        line_bot_api.push_message(user_id, TextSendMessage(text=block_message))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=welcome_message))
    
    # 將使用者狀態設置為 0（加入好友）
    user_status[user_id] = 0

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id
    # 將使用者狀態設置為 1（解除封鎖後再重新加入好友）
    user_status[user_id] = 1



if __name__ == '__main__':
    app.run()