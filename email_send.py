#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'Jerry'
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from config import *

log = logging


class EmailSender(object):


    def __init__(self):
        # 发送邮件的smtp服务器（从QQ邮箱中取得）
        self.smtp_host = smtp_host
        # 用于登录smtp服务器的用户名，也就是发送者的邮箱
        self.smtp_user = smtp_user
        # 授权码，和用户名user一起，用于登录smtp， 非邮箱密码
        self.smtp_pwd = smtp_pwd
        # smtp服务器SSL端口号，默认是465
        self.smtp_port = 465
        # 发送方的邮箱
        self.sender = sender

    def send_email(self, toLst, subject, text = None, image = None):
        '''
        发送邮件
        :param toLst: 收件人的邮箱列表
        :param subject: 邮件标题
        :param body: 邮件内容
        :return:
        '''
        # 邮件内容，格式，编码
        if text:
            text = MIMEText(text, 'plain', 'utf-8')
        if image:
            image = MIMEImage(image, _subtype = 'png')
            image.add_header('Content-Disposition', 'attachment', filename='二维码.png')

        message = MIMEMultipart()
        # 发件人
        message['From'] = self.sender
        # 收件人列表
        message['To'] = ",".join(toLst)
        # 邮件标题
        message['Subject'] = subject
        message.attach(text)
        message.attach(image)
        try:
            # 实例化一个SMTP_SSL对象
            smtpSSLClient = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            # 登录smtp服务器
            loginRes = smtpSSLClient.login(self.smtp_user, self.smtp_pwd)
            log.info("登录结果：loginRes = {}".format(loginRes))
            if loginRes and loginRes[0] == 235:
                log.info("登录成功，code = {}".format(loginRes[0]))
                smtpSSLClient.sendmail(self.sender, toLst, message.as_string())
                log.info("mail has been send successfully. message:{}".format(message.as_string()))
            else:
                log.info("登陆失败，code = {}".format(loginRes[0]))
        except Exception as e:
            log.info("发送失败，Exception: e={}".format(e))
