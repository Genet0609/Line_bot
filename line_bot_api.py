from flask import Flask,request,abort
from linebot import (LineBotApi,WebhookHandler,exceptions)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

line_bot_api = LineBotApi("BAhZVLO5jlXYUVfpd2SZLMrE5AraVVZ/l3K348nBOQieNR9gaN+y3ugPEYgq0kAEiCVUi824Kr0RDJ8grBrXGIj/f5907HOS0WafIum7DsyZZiKdMH62dhl1HCrsRp86tXazu0qsKBoe8YF6N2+/KwdB04t89/1O/w1cDnyilFU=")

handler = WebhookHandler("040e02f497904821933c1e56de6bfc14")