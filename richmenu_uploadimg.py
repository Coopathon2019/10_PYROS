from linebot import (
    LineBotApi, WebhookHandler
)
import json

with open("./rich_menu.png", 'rb') as f:
    with open('./config','r') as con:
        j = json.loads(con.readline())
        line_bot_api = LineBotApi(j['linebotapi'])
        line_bot_api.set_rich_menu_image(j['richMenuId'], "image/jpeg", f)
