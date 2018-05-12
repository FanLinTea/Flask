# Collection = db.Table("collection",
#                       db.Column("tuser_id", db.Integer, db.ForeignKey('tuser.id')),
#                       db.Column("music_id", db.Integer, db.ForeignKey('music.id')))
#
# class Music(db.Model):
#     __tablename__ = 'music'
#
#     id = db.Column(db.Integer, primary_key=True)
#
#
# class tUser(db.Model):
#     __tablename__ = 'tuser'
#
#     id = db.Column(db.Integer, primary_key=True)
#     Musics = db.relationship('Music',
#                                secondary=Collection,
#                                backref=db.backref('tuser', lazy='dynamic'),
#                                lazy='dynamic'
#                                )


# import re
#
# sd = re.match(r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$','929066992@qq.com')
# print sd.group()

class A():
    a = 'aa'
    b = 'bb'

b = A(a='ls',b='cs')
print b.a
