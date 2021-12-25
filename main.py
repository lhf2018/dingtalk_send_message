import json
import time
import requests
import hmac
import hashlib
import base64
import urllib.parse
import random


def get_news():
    channel = [
        "头条",
        "新闻",
        "国内",
        "国际",
        "政治",
        "财经",
        "体育",
        "娱乐",
        "军事",
        "教育",
        "科技",
        "NBA",
        "股票",
        "星座",
        "女性",
        "健康",
        "育儿"
    ]
    news_url = "https://api.jisuapi.com/news/get?channel=" + channel[
        random.randint(0, 15)] + "&start=0&num=10&appkey=840dba1a7e1a9394"
    news_header = {
        "Charset": "UTF-8"
    }
    response = requests.post(url=news_url, headers=news_header)
    return response.json()['result']['list']


def send_message(dingtalk_webhook_accesstoken, dingtalk_secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = dingtalk_secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, dingtalk_secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    dingtalk_webhook = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(
        dingtalk_webhook_accesstoken,
        timestamp, sign)
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    new_list = get_news()
    text = "**"+time.strftime("%Y-%m-%d", time.localtime())+" 摸鱼快报**\n\t"
    for i, var in enumerate(new_list):
        text += str(i + 1) + '. ' + "[" + var['title'] + "](" + var['weburl'] + ")\n\t"

    message = {

        "msgtype": "markdown",
        "markdown": {
            "title": "新闻快报",
            "text": text
        },
        "at": {
            "isAtAll": False
        }
    }
    message_json = json.dumps(message)
    # print(text)
    info = requests.post(url=dingtalk_webhook, data=message_json, headers=header)
    print(info.text)


if __name__ == '__main__':
    dingtalk = [
        # 钉钉群机器人对应的accesstoken
        ["accesstoken",
         # 钉钉群机器人对应的secret
         "dingtalk_secret"],
        ["accesstoken",
         "dingtalk_secret"]]
    for i, val in enumerate(dingtalk):
        send_message(val[0], val[1])
