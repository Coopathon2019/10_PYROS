import requests
import json

#LINE account information
def Line_config(filename):
    j = 0
    with open(filename,'r') as f:
        j = json.loads(f.readline())
    linebotapi = j['linebotapi']
    handler = j['secret']
    richMenuId = j['richMenuId']
    return linebotapi, handler, richMenuId

line_bot_api, handler, richMenuId = Line_config('./config')

headers = {"Authorization":"Bearer " + line_bot_api,"Content-Type":"application/json"}

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/' + richMenuId,headers=headers)

print(req.text)
