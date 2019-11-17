from flask import Flask, request, abort
from flask import render_template
from flask import send_file
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import psycopg2
import random
import json
from datetime import datetime
from collections import Counter
import pandas as pd
import time
import warnings
warnings.filterwarnings("ignore")
import math
import os


app = Flask(__name__, static_url_path='/cartlories/static')
datasets_dir = os.path.join(app.root_path,'Datasets')
cal_file = os.path.join(datasets_dir, 'cal.csv')
receipt_file = os.path.join(datasets_dir, 'receipt.csv')
nutrition_file = os.path.join(datasets_dir, 'nutrition.json')

#LINE account information
def Line_config(filename):
    j = 0
    with open(filename,'r') as f:
        j = json.loads(f.readline())
    linebotapi = LineBotApi(j['linebotapi'],timeout=10)
    handler = WebhookHandler(j['secret'])
    db = j['database']
    pwd = j['password']
    return linebotapi, handler, db, pwd

line_bot_api, handler, db, pwd = Line_config('./config')


#LINE callback setup
@app.route("/cartlories/callback", methods=['POST'])
def callback():
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Get user profile
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    name = profile.display_name
    user_says = event.message.text
    # Reply
    if '我想看看我的收藏' in user_says:
        # Connect to db
        try:
            conn = psycopg2.connect(database=db,user=db,password=pwd)
            cur = conn.cursor()
            print('Db connection has been established')
        except:
            print('Failed to connect db')
        # Record userid and dishname
        cmd = "SELECT Dishname FROM Liked WHERE Userid='" + user_id + "';"
        cur.execute(cmd)
        rows = cur.fetchall()
        conn.close()
        if len(rows) > 0:
            c = Counter(rows)
            contents = [0] * min(10,len(c.keys()))
            for i in range(0,min(10,len(c.keys()))):
                dishid = list(c.keys())[i]
                dish = dishid[-1].split('-')[-1]
                nutrition = get_nutrition(nutrition_file,dish)
                contents[i] = BubbleContainer(
                    direction='ltr',
                    hero=ImageComponent(
                        url=get_nutrition(nutrition_file,dish)['photo'],
                        size='full',
                        aspect_ration='1:1',
                        aspect_mode='cover'
                    ),
                    body=BoxComponent(
                        layout='vertical',
                        contents=[
                            TextComponent(text=dish,weight='bold',size='1g'),
                            TextComponent(text=nutrition['nutrition']['卡路里']),
                            TextComponent(text='可補充到'),
                            TextComponent(text='您已紀錄' + str(c[dishid]) + '次！')
                        ]
                    ),
                    footer=BoxComponent(
                        layout='vertical',
                        contents=[
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(
                                label='查看食譜詳情',
                                uri='/cartlories/dishdetail?dishname=' + dish + '&nop=1')),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(
                                label='和朋友分享食譜',
                                uri='')),
                        ButtonComponent(
                            style='link',
                            height='sm',
                            action=URIAction(
                                label='加入買菜卡',
                                uri=''))]))
            carousel = CarouselContainer(contents=contents)
            line_bot_api.reply_message(event.reply_token,
                FlexSendMessage(alt_text="flex_msg",contents=carousel))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text='還沒有記錄喔，趕快開始記錄吧！'))

# Receipt card
@app.route('/cartlories/card/receipt')
def receipt():
    j = pd.read_json(nutrition_file)
    # HTML code for stars
    stars = []
    star = '<i class="fa fa-star"></i>'
    halfstar = '<i class="fa fa-star-half-o"></i>'
    emptystar = '<i class="fa fa-star-o"></i>'
    # Pic, cal, and difficulty for each dish
    receipt = {i:[j[i]['photo'],j[i]['nutrition']['卡路里'].split(' ')[0]] for i in j}
    # Calculate stars
    print(get_menu(cal_file,['麻婆豆腐'],3))
    print(get_receipt(receipt_file,'麻婆豆腐'))
    print(get_nutrition(nutrition_file,'麻婆豆腐'))
    return render_template('ReceiptCard.html', receipt=receipt)


# Purchase card
@app.route('/cartlories/card/purchase', methods=['GET'])
def purchase():
    return render_template('PurchaseCard.html')


# Record the dish, able to handle uploaded images
@app.route('/cartlories/card/record', methods=['GET','POST'])
def record():
    if request.method == 'POST':
        try:
            conn = psycopg2.connect(database=db,user=db,password=pwd)
            cur = conn.cursor()
            print('Db connection has been established')
        except:
            print('Failed to connect db')
        cmd = "INSERT INTO Record"
        print(request.form)
    return render_template('RecordCard.html')


# Dish detail
@app.route('/cartlories/dishdetail', methods=['GET','POST'])
def dishdetail():
    try:
        dishname = request.args.get('dishname')
        people = int(request.args.get('nop'))
    except:
        abort(404)
    ingredients = get_menu(cal_file, [dishname], people)
    dish_info = get_nutrition(nutrition_file, dishname)
    steps = get_receipt(receipt_file, dishname)
    return render_template('DishDetail.html', dishname=dishname, ingredients=ingredients, dish_info=dish_info, steps=steps, people=people)


# Route for ajax when clicking like btn
@app.route('/cartlories/like', methods=['GET','POST'])    
def like():
    if request.method == 'POST':
        userid = request.form['userid']
        dishname = request.form['dishname']
        # Connect to db
        try:
            conn = psycopg2.connect(database=db,user=db,password=pwd)
            cur = conn.cursor()
            print('Db connection has been established')
        except:
            print('Failed to connect db')
        # Record userid and dishname
        cmd = "INSERT INTO Liked(Userid,Dishname) VALUES ('" + userid + "','" + dishname + "');"
        cur.execute(cmd)
        conn.commit()
        conn.close()
        return 'OK'
    else:
        userid = request.args.get('userid')
        # Connect to db
        try:
            conn = psycopg2.connect(database=db,user=db,password=pwd)
            cur = conn.cursor()
            print('Db connection has been established')
        except:
            print('Failed to connect db')
        # Get history
        cmd = "SELECT Dishname FROM Liked WHERE userid='" + userid + "';"
        cur.execute(cmd)
        rows = cur.fetchall()
        conn.close()
        return rows


# Route for ajax when operating the basket
@app.route('/cartlories/basket', methods=['GET','POST'])
def basket():
    if request.method == 'POST':
        userid = request.form['userid']
        dishname = request.form['dishname']
        try:
            conn = psycopg2.connect(database=db,user=db,password=pwd)
            cur = conn.cursor()
            print('Db connection has been established')
        except:
            print('Failed to connect db')
        cmd = "INSERT INTO Cart(Userid,Dish,Ingredients) VALUES ('" + userid + "','" + dishname
        ingred = []
        cmd = cmd + "'," + ingred + ");"
        cur.execute(cmd)
        conn.commit()
        conn.close()
        return 'OK'
    else:
        print(request.form['dishname'])
        data=get_menu(cal_file,['麻婆豆腐'])
        print(data)
        return data


@app.route('/cartlories')
def hello():
    return "Hello world"


# 取得需要購買的食材和量
def get_menu(filename, cusines, num = 1):  #cusines 要是list, num 要是 int 預設為 1人份

    data = pd.read_csv(filename, index_col=['食材', '單位'])
    data = data[cusines].dropna(how='all').sum(axis=1)
    receipt = dict(data.index)
    
    a = [j if i == -1.0 else str(round(i*num,2))+' '+j for i, j in zip(list(data),list(receipt.values()))]
       
    return dict(zip(list(receipt.keys()),a))  # 回傳的是 dict

# 個別菜餚的食譜
def get_receipt(filename, name):  #cusines 要是str
    
    receipt = pd.read_csv(filename, index_col=['Step']).dropna(how='all')
    temp = dict(receipt[name].dropna().apply(lambda x: x.split(' ') ))
    dict_receipt = {str(k):[i for i in v] for k,v in temp.items()}
    return dict_receipt  # 回傳的是 dict
    

def get_nutrition(filename, name):
    return dict(pd.read_json(filename)[name])


def main():
    app.run(host='0.0.0.0',port=9487)


if __name__ == "__main__":
    main()    
