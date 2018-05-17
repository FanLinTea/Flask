#coding:utf8
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


Collection = db.Table("collection",
                db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
                db.Column("music_id", db.Integer, db.ForeignKey('music.id')),
                db.Column('id',db.Integer,primary_key=True))

class Music(db.Model,BaseModel):
    """音乐"""
    __tablename__ = 'music'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    singer = db.Column(db.String(64))   # 歌手
    heat = db.Column(db.Integer, nullable=True)  # 热度
    # date = db.Column(db.Time)  # 创建时间
    price = db.Column(db.Integer, default=0)    # 价格
    image_url = db.Column(db.String(128), nullable=True)  # 歌曲图片地址


class User(db.Model,BaseModel,UserMixin):
    """用户"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64), unique=True)  # 角色名
    password_hash = db.Column(db.String(250))
    # username = db.Column(db.String(64), unique=True)
    over = db.Column(db.Integer, default=200) # 余额
    avatar_url = db.Column(db.String(128), nullable=True) # 头像地址
    email = db.Column(db.String(64))
    confirmd = db.Column(db.Boolean, default=False)

    Musics = db.relationship('Music',
                                secondary=Collection,
                                backref=db.backref('user', lazy='dynamic'),
                                lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('非法访问')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):  # 验证密码
        return check_password_hash(self.password_hash, password)

    def generate_token(self,expires=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        print token
        try:
            data = s.loads(token)
            print data
        except:
            return False
        id = data.get('confirm')

        # self.confirmd = True
        # db.session.add(self)
        return id

from . import login
@login.user_loader
def load_user(userid):
    '''当用户登陆后，login通过用户id返回用户对象'''
    return User.query.get(int(userid))

# class Collection(db.Model,BaseModel):
#     '''收藏'''
#     __tablename__ = 'collection'
#     id = db.Column(db.Integer, primary_key=True)
#     mid = db.Column(db.Integer,db.ForeignKey('User.id'))
#     uid = db.Column(db.Integer,nullable=False)
