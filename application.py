# coding: utf-8
from flask import Flask as FlaskBase
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import os
from jobs.tasks.timer import SchedulerConfig
from common.libs.utils import correctPath

db = SQLAlchemy()
scheduler = APScheduler() # 定时任务

class Flask(FlaskBase):
    def __init__(self, import_name, static_folder, template_folder, root_path):
        super(Flask, self).__init__(import_name, static_folder=static_folder, template_folder=template_folder, root_path=root_path)
        
        self.config.from_pyfile(correctPath('config/config.py'))
        db.init_app(self)
        
        self.config.from_object(SchedulerConfig())
        scheduler.init_app(self)
        scheduler.start()

static_path = correctPath('web/static')
templates_path = correctPath('web/templates')
app = Flask(__name__, static_folder=static_path, template_folder=templates_path, root_path=os.getcwd())

from flask_cors import CORS
CORS(app, supports_credentials = True) # 解决跨域问题
