#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Jerry'
import logging
import random
import time
import json
import itchat
import schedule
import requests
from config import *
from threading import Thread

sig = 1


def say_good_morning(lz):
    morning_words = random.choice(morining_words)
    itchat.send(morning_words, toUserName = lz)
    time.sleep(10)
    if joke_or_love:
        words = say_love()
    else:
        words = get_tuling_response('讲个笑话')
    # 今天你对我爱搭不理，明天我还来找你
    itchat.send(words, toUserName = lz)


def eat_something(lz):
    itchat.send('小🐎哥小🐎哥，午饭时间到啦，记得吃饭，少吃零食哦', toUserName = lz)


def say_good_night(lz):
    itchat.send('小🐎哥，夜深了，该睡觉啦', toUserName = lz)


def get_tuling_response(_info):
    api_url = tuling_url
    data ={
        'key':tuling_key,#自行注册获得
        'info':_info,
        'userid':'haha'
    }
    # 发送数据到指定网址，获取网址返回的数据
    res = requests.post(api_url,data).json()
    # 给用户返回的内容
    return res['text']


@itchat.msg_register(itchat.content.TEXT,isFriendChat=True)
def text_reply(msg):
    # 获取好友发送的文本消息
    # 返回同样的文本消息
    content = msg['Content']
    # 将好友的消息发送给机器人去处理，处理的结果就是返回给好友的消息
    returnContent = get_tuling_response(content)
    return returnContent


def say_love():
    # 爬取渣男语录
    url = 'https://api.lovelive.tools/api/SweetNothings/WebSite/1'
    res = requests.get(url)
    data = json.loads(res.text)
    word = data[0]['content']
    return word


def logout():
    """
    登录时间过长会自动退出，退出之后sig置0
    :return:
    """
    global sig
    sig = 0


def login(img_data):
    """
    将二维码通过邮件发送到手机，然后手机扫码登录
    :param img_data:
    :return:
    """
    from email_send import EmailSender
    email_client = EmailSender()
    to_email = [receive]
    img = img_data
    text = '微信登录二维码'
    subject = '微信登录二维码'
    email_client.send_email(to_email, subject, text = text, image = img)


def open_image():
    while True:
        try:
            with open('./QR.png', 'rb') as f:
                img_data = f.read()
                if img_data:
                    login(img_data)
        except BaseException as e:
            continue
        finally:
            time.sleep(60)

def check_sig():
    """
    检查登录状态，如果退出了就重新登录
    :return:
    """
    if sig:
        pass
    else:
        main()

def run_check_sig():
    """
    每隔八个小时候检查一下登录状态
    :return:
    """
    schedule.every(8).hours.do(check_sig)
    while True:
        schedule.run_pending()

def main():
    itchat.auto_login(hotReload = True, exitCallback = logout)
    # 开启自动回复
    if auto_response_enable:
        itchat.run()
    # 根据好友昵称查找好友的信息,返回值是一个列表，有多个元素
    res = itchat.search_friends(friend)
    # 通过索引获取该好友的详细信息
    lz = res[0]['UserName']
    # 每天早中晚定时骚扰
    schedule.every().day.at('08:00').do(say_good_morning, lz)
    # schedule.every().day.at('12:00').do(eat_something, lz)
    # schedule.every().day.at('23:59').do(say_good_night, lz)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    task = [main, open_image, run_check_sig]
    for func in task:
        p = Thread(target = func)
        p.start()



