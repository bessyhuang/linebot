import os
from flask import Flask, request, abort
import requests
from bs4 import BeautifulSoup

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

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))


@app.route("/callback", methods=['POST'])
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
    if event.message.text == '本周新片':
        r = requests.get('http://www.atmovies.com.tw/movie/new/')
        r.encoding = 'utf-8'

        soup = BeautifulSoup(r.text, 'lxml')
        filmTitle = soup.select('div.filmTitle a')

        #print(filmTitle[0]['href'])
        #print("http://www.atmovies.com.tw" + filmTitle[0]['href'])
        '''
        content = ''
        for i in filmTitle:
            content += i.text + '\n' + "http://www.atmovies.com.tw" + i['href'] + '\n\n'
        '''
        content = ''
        for index, i in enumerate(filmTitle):
            content += i.text + '\n' + "http://www.atmovies.com.tw" + i['href'] + '\n\n'
            if index >= 10: #回傳給使用者最多10筆資料
                break
        print(content)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))


    if '成績' in event.message.text:
        raw_msg = event.message.text
        print(raw_msg)

        other, studentID, studentPW = raw_msg.split('\n')
        print(other, studentID, studentPW)

        if studentID != None and studentPW != None:
            payload = {'mail_id': studentID, 'mail_pwd': studentPW}
            rs = requests.session()
            res = rs.post('http://stu.fju.edu.tw/stusql/SingleSignOn/StuScore/SSO_stu_login.asp', data = payload)
            res2 = rs.get('http://stu.fju.edu.tw/stusql/SingleSignOn/StuScore/stu_scoreter.asp')
            soup = BeautifulSoup(res2.content, "html.parser")

            all_td1 = soup.find_all('td', {'align': 'left', 'valign': None})
            list1 = []
            for obj in all_td1:
                list1.append(obj.contents[0].strip())
            print(list1)

            all_td2 = soup.find_all('td', {'align': 'center', 'valign': None})
            list2 = []
            for obj in all_td2:
                list2.append(obj.contents[0])
            new_list2 = []
            for i in range(1, len(list2), 4):
                if i >= 9:
                    #print(list2[i])    #9, 13, 17, 21
                    new_list2.append(list2[i].strip())
            print(new_list2)

            all_td3 = soup.find_all('td', {'align': 'right', 'valign': None})
            list3 = []
            for obj in all_td3:
                list3.append(obj.contents[0].strip())
            print(list3)

            content = ''
            for i in range(len(list1)):
                content += str(list1[i]) + '\t' + str(new_list2[i])+ " 學分" + "\n成績：" + str(list3[i]) + '\n\n'
            #print(content)
            '''
            unit = sum(new_list2)
            subscore = 0
            for i in range(len(list1)):
                    subscore += new_list2[i] * list3[i]
            
            content += '\n\n' + '平均：' + str(subscore / unit)
            '''
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))

if __name__ == "__main__":
    app.run()