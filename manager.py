# coding: utf-8
from www import app
from application import db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
# DB 迁移
migrate = Migrate(app, db) # 使用Migrate绑定app和db
manager.add_command('db',MigrateCommand) # 添加迁移脚本的命令到manager中

# Sever 管理
server = Server(host='127.0.0.1', port=app.config['SERVER_PORT'], use_debugger=True, use_reloader=True)
manager.add_command('runserver', server)

# 数据迁移方法
# python manager.py db init
# python manager.py db migrate
# python manager.py db upgrade

if __name__ == '__main__':
    # app.run()
    try:
        import sys
        sys.exit(manager.run())
    except Exception as e:
        import traceback
        traceback.print_exc()