# coding:utf8
from threading import Thread
from manage import app
from flask_mail import Message
from flask import render_template
from . import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to,tmp,subject='LuJiang', **kwargs):
    msg = Message(subject=subject,sender=('Lujiang','15811280010@163.com'),recipients=to)
    msg.html = tmp
    msg.body = tmp
    t1 = Thread(target=send_async_email, args=[app, msg])
    t1.start()
    return t1


