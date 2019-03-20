#!/usr/bin/env
# -*-coding:utf-8-*-
# @Author  : E🚀M

from random import Random
from django.core.mail import send_mail,EmailMessage

from users.models import EmailVerifyRecord
from Lmusic.settings import EMAIL_FROM
from django.template import loader

def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == "update_email":
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == 'register':
        email_title = '听·音乐 激活链接'
        # email_body = '请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}'.format(code)
        email_body = loader.render_to_string(
            "email_register.html",  # 需要渲染的html模板
            {
                "active_code": code  # 参数
            }
        )

        msg = EmailMessage(email_title, email_body, EMAIL_FROM, [email])
        msg.content_subtype = "html"
        send_status = msg.send()
        # send_status =  send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
