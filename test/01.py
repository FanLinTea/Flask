#coding:utf8
'''
from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间


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
    # orders = db.relationship("Order", backref="music",lazy='dynamic')
    comment = db.relationship("Comment", backref=db.backref("music",lazy='joined'),foreign_keys=[Comment.music_id],lazy='dynamic')


class User(db.Model,BaseModel):
    """用户"""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64), unique=True)  # 账号
    password_hash = db.Column(db.String(64))
    # username = db.Column(db.String(64), unique=True)
    over = db.Column(db.Integer, default=0) # 余额
    avatar_url = db.Column(db.String(128), nullable=True) # 头像地址
    email = db.Column(db.String(64))
    # orders = db.relationship("Order", backref="user",lazy='dynamic')
    comment = db.relationship("Comment", backref=db.backref("user",lazy='joined'),foreign_keys=[Comment.user_id],lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('非法访问')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):  # 验证密码
        return check_password_hash(self.password_hash, password)


#
# class Collection(db.Model,BaseModel):
#     收藏
#     __tablename__ = 'collection'
#     id = db.Column(db.Integer, primary_key=True)
#     music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Comment(db.Model,BaseModel):
     评论
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(258)) #评论
    # x# user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# class Order(db.Model,BaseModel):
#     订单
#     __tablename__ = 'order'
#     id = db.Column(db.Integer, primary_key=True)
#     music_id = db.Column(db.Integer, db.ForeignKey('music.id'),)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     status = db.Column(db.Enum(
#         "WAIT_PAYMENT",  # 待支付
#         "PAID",  # 已支付
#         "COMPLETE",  # 已完成
#         "CANCELED",  # 已取消
#     ))
'''