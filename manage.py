#coding:utf8
from music import create_app, db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from music.models import User,Music,Collection  # 不导入模型类，将无法创建表，程序找不到


app = create_app('test')
migrate = Migrate(app, db)
manager = Manager(app)  # 让flask程序可以使用命令行模式运行
manager.add_command('db', MigrateCommand)  # 给命令行添加db命令，用来迁移数据库

# @manager.shell
# def make_shell_context():
#     return dict(db=db,User=User,Music=Music)


if __name__ == '__main__':
    # print app.url_map
    manager.run()

