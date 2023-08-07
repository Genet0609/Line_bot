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


    
@handler.add(FollowEvent)
def handler_follow(event):
    welcome_message = """哈囉！你好哇！恭喜你已經成為了莉飄兒大人的部下！"""
    
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=welcome_message))
    

@handler.add(UnfollowEvent)
def handle_unfollow(event):
    block_message = """哇哈哈！莉飄兒大人果然還是最好的，對吧？"""
    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=block_message))

if __name__ == '__main__':
    app.run()