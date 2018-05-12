#coding:utf8
from . import auth
from flask import render_template,request,jsonify,flash
from music.models import User
from music import db
import re
from music.email import send_email
import time


@auth.route('/')
def Home():
    '''首页'''
    return render_template('loginxxxx.html')

@auth.route('/login')
def login():
    '''登陆'''
    return render_template('login.html')

@auth.route('/registered',methods=['GET','POST'])
def registered():
    '''注册视图'''
    if request.method == 'POST':
        dict_data = request.json  # 接受表单数据

        email = dict_data.get('mail')
        password = dict_data.get('password')
        verification = dict_data.get('verification')

        # 判断信息是否完整
        if not all([email,password,verification]):
            return jsonify(erro='请完整填写信息')

        #  判断邮箱格式
        if not re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$',email):
            return jsonify(erro='邮箱格式不正确')

        if User.query.filter_by(email=email).first():
            return jsonify(erro='邮箱以存在，请更换注册邮箱')

        #  密码不能少于8位
        if len(password) < 8:
            return jsonify(erro='密码不能少于8位')

        #  保存到数据库
        try:
            usr = User(email=email,password=password)
            db.session.add(usr)
            db.session.commit()
        except:
            return jsonify(erro='数据库爆炸了')


        token = usr.generate_token()
        #  构造邮件信息
        tmp = '<p>欢迎使用LuJiang-Music,</p><p>点击链接完成您的用户认证</p><a href="http://127.0.0.1:5000/certified/%s">www.LuJiang.com</a>' %token
        send_email(to=[email],tmp=tmp,subject='LuJiang的用户认证')  # subject有默认值，LuJiang

        return jsonify(email=email)
    return render_template('registered.html')


@auth.route('/certified/<token>')
def certif(token):
    '''验证邮箱的视图'''
    print token
    u = User().confirm(token)  # 获取用户id
    print u
    if not u:
        return render_template('certif.html',erro=u'你未通过认证,请重新注册')
    user = User.query.filter_by(id=u).first()
    user.confirmd = True
    db.session.add(user)
    db.session.commit()
    return render_template('login.html')
