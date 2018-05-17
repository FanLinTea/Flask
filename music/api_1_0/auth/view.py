#coding:utf8
from . import auth
from flask import render_template,request,jsonify,redirect,url_for
from music.models import User
from music import db,login
import re
from music.email import send_email
from flask_login import login_user,login_required,current_user,logout_user
from music.utils.img_qiniu import imp_up
import time



@auth.route('/login',methods=['GET','POST'])
def login():
    '''登陆'''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('reme')

        if not all([email,password]):
            return render_template('login.html',erro=u'请完整填写数据')
        user = User.query.filter_by(email=email).first()  #  获取当前用户对象
        if not user:
            return render_template('login.html',erro=u'此邮箱未注册')
        if not user.verify_password(password):  #  判断hash密码
            return render_template('login.html',erro=u'密码错误')

        if not user.confirmd:
            return render_template('login.html',erro=u'账号尚未激活')

        login_user(user,remember=remember)
        return redirect(url_for('main.Home'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('Logout.html')

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

    u = User().confirm(token)  # 获取用户id

    if not u:
        return render_template('certif.html',erro=u'你未通过认证,请重新注册')
    user = User.query.filter_by(id=u).first()
    user.confirmd = True
    db.session.add(user)
    db.session.commit()
    return render_template('login.html',ok=u'验证成功，请登陆')

@auth.route('/test')
@login_required
def test():
    '''测试登陆装饰器'''
    return render_template('test.html')


@auth.route('/avatar',methods=['GET','POST'])
@login_required
def avatar():
    '''返回头像的视图
        mark=1：默认头像
        mark=2:用户上传的头像
        '''
    name = current_user.account
    #  如果用户没有设置头像和昵称，则显示默认图片和邮箱
    avatar = current_user.avatar_url
    if not name:
        name = current_user.email
    if not avatar:
        avatar = '../static/timg.jpg'
    return jsonify(name=name,avatar=avatar,mark='1')

@auth.route('/personal',methods=['GET','POST'])
@login_required
def personal():
    '''个人信息页面'''
    if request.method == 'POST':
        email = current_user.email
        name = current_user.account
        avatar_url = current_user.avatar_url
        over = current_user.over
        if not name:
            name = email
        if not avatar_url:
            avatar_url = '../static/timg.jpg'
        return jsonify(name=name,email=email,avatar_url=avatar_url,over=over)

    return render_template('personal.html')

@auth.route('/personal_x',methods=['GET','POST'])
@login_required
def personal_x():
    '''修改个人信息'''
    avatar_url = current_user.avatar_url
    if request.method == 'POST':
        if not avatar_url:
            avatar_url = '../static/timg.jpg'
            return jsonify(avatar_url=avatar_url)
        return jsonify(avatar_url=avatar_url)

@auth.route('/personal_b',methods=['POST','GET'])
@login_required
def personal_b():
    if request.method == 'GET':
        return render_template('personal.html')
    avatar = request.files.get('avatar').read()
    new_name = request.form.get('new')

    user = current_user._get_current_object() # 需要提前获得用户对象，用于头像地址的保存判断

    if len(avatar) > 0:
        # 当用户修改头像时，如果他没有选择头像，那么avatar什么都不会返回，所以不能判断他是不是空值
        avatar = avatar
        url_pattern = imp_up(avatar)  #  只有他选择了头像才上传到七牛云
        user.avatar_url = 'http://p8rknt955.bkt.clouddn.com/' + url_pattern # 只有上传了，才保存头像地址
    if not new_name:
        new_name = current_user.account
        if not new_name:
            new_name = current_user.email


    user.account = new_name
    db.session.add(user)
    db.session.commit()
    # current_user.avatar_url = + avatar

    return render_template('personal.html')


