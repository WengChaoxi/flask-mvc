# coding: utf-8
from application import app
from common.libs.utils import docResponse

# app.register_blueprint()

@app.route('/')
def index():
    return ''

@app.route('/robots.txt')
def robots():
    return docResponse('web/static/robots.txt')

@app.before_first_request
def func():
    print('只处理第一次请求')
    return None
    
@app.before_request
def visitLimit():
    allow_url = ['/']
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