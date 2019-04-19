#web app 架設伺服器的code 
from flask import Flask, request, abort #flask架設伺服器沒有畫面 django做網頁 大型專案 

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('G5io7PcjeFo1M8Bluxm9kRG2cTRoQzUjdM8kfbn//tc3IVML/6z/X+NEu3f4dGUkCUKGtCrZGPi3H51dLRFdu11baUCWXw53+tGqQ2Do8QZ0TUiwPWg41fQrlbKU56Oqde8EbJEXjlH/Xnil8wZScwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f7fcfcb81547c7b483b1503667eced8c')

#假設我們有www.line.bot.com(callback)有人來我們網址路徑敲門(發送訊號) 就會觸發以下
@app.route("/callback", methods=['POST']) #callback返回觸發 route:路徑 
def callback():#接收line收訊息後 觸發程式碼 完全不需改
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage) #之後run到這個
def handle_message(event): #event:消費者傳的訊息
    line_bot_api.reply_message(
        event.reply_token, #我們的token 只有我們能回復
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":  #直接被執行 別人寫入 才會開始run
    app.run()


