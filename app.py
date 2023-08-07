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
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token,message)

if __name__ == "__main__":
    app.run()