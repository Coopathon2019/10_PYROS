from linebot import (
    LineBotApi, WebhookHandler
)
import json

#LINE account information
def Line_config(filename):
    j = 0
    with open(filename,'r') as f:
        j = json.loads(f.readline())
    linebotapi = LineBotApi(j['linebotapi'])
    handler = WebhookHandler(j['secret'])
    richMenuId = j['richMenuId']
    return linebotapi, handler, richMenuId

line_bot_api, handler, richMenuId = Line_config('./config')

line_bot_api.delete_rich_menu(richMenuId)
