import requests
import json
from linebot.models import URIAction

#LINE account information
def Line_config(filename):
    j = 0
    with open(filename,'r') as f:
        j = json.loads(f.readline())
    linebotapi = j['linebotapi']
    handler = j['secret']
    return linebotapi, handler

line_bot_api, handler = Line_config('./config')

headers = {"Authorization":"Bearer " + line_bot_api,"Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 843},
    "selected": "true",
    "name": "my_richmenu",
    "chatBarText": "為卡路里血拚！",
    "areas":[
        {
          "bounds": {"x": 225, "y": 85, "width": 270, "height": 270},
          "action": {"type": "uri", "uri": "line://app/1653449565-3EYpW02O"} # Record
        },
        {
          "bounds": {"x": 825, "y": 85, "width": 270, "height": 270},
          "action": {"type": "uri", "uri": "line://app/1653449565-XaZnpAML"} # Reciept
        },
        {
          "bounds": {"x": 1425, "y": 85, "width": 270, "height": 270},
          "action": {"type": "message", "text": "5張A"} # Liked
        },
        {
          "bounds": {"x": 2000, "y": 85, "width": 270, "height": 270},
          "action": {"type": "uri", "uri": "line://app/1653449565-JeKGp7y2"} # Purchase
        },
        {
          "bounds": {"x": 1050 , "y": 630, "width": 400, "height": 130},
          "action": {"type": "uri", "uri": "line://app/1653449565-JeKGp7y2"} # Purchase
        }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu', 
                       headers=headers,data=json.dumps(body).encode('utf-8'))

print(req.text)