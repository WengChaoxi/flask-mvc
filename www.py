# coding: utf-8
from application import app
from flask import request, session, redirect
from common.libs.utils import docResponse

from web.controllers.Example import route_example
app.register_blueprint(route_example, url_prefix='/example')

@app.route('/')
def index():
    return 'hello world'

@app.route('/robots.txt')
def robots():
    return docResponse('web/static/robots.txt')

@app.before_first_request
def func():
    print('只处理第一次请求')
    return None
    
@app.before_request
def visitLimit():
    allow_url = ['/', '/example']
    if request.path in allow_url or session.get('account'):
        return None
    return redirect('/')

@app.after_request
def func(response):
    print('每一次请求之后调用')
    return response

@app.errorhandler(404)
def func(error):
    return '', 404
