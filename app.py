#web app 架設伺服器的code 
from flask import Flask, request, abort #flask架設伺服器沒有畫面 django做網頁 大型專案 

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('eDWxVWjfCghFVGeT8uMtTu9ZwxCK2VJhX5w8Pro8fNcb94nupk/knuuL0pFmahqyCUKGtCrZGPi3H51dLRFdu11baUCWXw53+tGqQ2Do8QZ95KP6E4PqaOgWsJawwLTdnBRBx7tsspoZknFKVQ/XGAdB04t89/1O/w1cDnyilFU=')
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
    msg = event.message.text
    r = '很抱歉您說什麼'

    if msg in ['hi', 'Hi']:#在清單裡
        r = 'hi'
    elif msg == '你吃飯了嗎':
        r = '還沒~'
    elif msg == '你是誰':
        r = '我是機器人'
    elif '訂位' in msg:
        r = '你想訂位,是嗎?'
    
    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
    )

        line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
        return


    line_bot_api.reply_message(
        event.reply_token, #我們的token 只有我們能回復
        TextSendMessage(text=r)) #msg功能
       


if __name__ == "__main__":  #直接被執行 別人寫入 才會開始run
    app.run()



