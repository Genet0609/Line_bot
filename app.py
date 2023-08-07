from flask import Flask,request,abort
from linebot import (LineBotApi,WebhookHandler,exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi("BAhZVLO5jlXYUVfpd2SZLMrE5AraVVZ/l3K348nBOQieNR9gaN+y3ugPEYgq0kAEiCVUi824Kr0RDJ8grBrXGIj/f5907HOS0WafIum7DsyZZiKdMH62dhl1HCrsRp86tXazu0qsKBoe8YF6N2+/KwdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("040e02f497904821933c1e56de6bfc14")

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

    emoji = [

                {
                    "index" : 0,
                    "productId": "5ac21c4e031a6752fb806d5b",
                    "emojiId" :"002"
                },
                {
                    "index" : 1,
                    "productId": "5ac21c4e031a6752fb806d5b",
                    "emojiId" :"039"
                },

                {
                    "index" : 2,
                    "productId": "5ac21c4e031a6752fb806d5b",
                    "emojiId" :"052"
                },

                {
                    "index" : 3,
                    "productId": "5ac21c4e031a6752fb806d5b",
                    "emojiId" :"012"
                },

                {
                    "index" : 4,
                    "productId": "5ac21c4e031a6752fb806d5b",
                    "emojiId" :"053"
                },

                {
                    "index" : 5,
                    "productId": "5ac21c4e031a6752fb806d5b",
                    "emojiId" :"002"
                },

                {
                    "index" : 6,
                    "productId": "5ac21c4e031a6752fb806d5b",
                    "emojiId" :"031"
                },

                {
                    "index" : 7,
                    "productId": "5ac21c4e031a6752fb806d5b",
                    "emojiId" :"014"
                }

    ]

    text_message = TextSendMessage(text="""$$$$$$$ 
哈囉！恭喜你已經成為了莉飄兒大人我的部下！""",emojis=emoji)
    
    sticker_message = StickerSendMessage(
        package_id="11537",
        sticker_id="52002748"
    )
    line_bot_api.reply_message(
        event.reply_token,
        [text_message,sticker_message]
    )

if __name__ == "__main__":
    app.run()