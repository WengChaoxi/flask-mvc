# coding: utf-8
from flask import request, session, redirect, url_for, send_file, make_response #,jsonify
from functools import wraps
import json, platform, requests, rsa

def handleData():
    # data = request.get_data()  # 获取前端数据
    # data = str(data, 'utf-8')  # 转utf-8
    # data = json.loads(data)  # json转字典
    data = json.loads(request.get_data().decode("utf-8"), strict=False)
    # if data is None:
    #     data = request.form.to_dic()
    # elif data is None:
    #     data = json.loads(request.args().decode("utf-8"), strict=False)
    if data is None:
        data ={}
    return data

def msg(status_code, data=None):
    data_dic = {
        'code': status_code,
    }
    if data:
        data_dic['data'] = data
    # return jsonify(data_dic)
    return json.dumps(data_dic, ensure_ascii=False)

def correctPath(path=''):
    slash = '/'  # Linux路径分割
    if platform.system() == 'Windows':
        slash = r'\\'
        path.replace('/', slash)
    elif platform.system() == 'Linux':
        path.replace(r'\\', slash)
    return path
    
'''  
def bytes2human(n):
    symbols = ('K','M','G','T','P','E','Z','Y')
    prefix = {}
    for i,s in enumerate(symbols):
        prefix[s] = 1<<(i+1)*10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n)/prefix[s]
            return '%.2f%s'%(value,s)
    return '%.2fB'%(n)
'''
from math import log
def bytes2human(n):
    symbols = ('B','K','M','G','T','P','E','Z','Y')
    index = int(log(n,2)//10)
    return '%.2f%s'%(float(n)/(1<<index*10), symbols[index])

def fileResponse(file_path, file_name=None):
    if not file_name:
        file_name = file_path.split(correctPath('/'))[-1]
    response = make_response(send_file(file_path))  # , as_attachment=True, attachment_filename='data.file'))
    response.headers["Cache-Control"] = "max-age=43200"
    response.headers["Content-Type"] = "application/octet-stream"
    from urllib import parse
    file_urlencode = parse.quote(file_name.encode('utf-8'))  # 对中文进行URL编码
    response.headers["Content-Disposition"] = "attachment; filename*=utf-8''%s" % (file_urlencode)
    # response.headers["Content-Length"] = "%d"%total_size
    return response

def login_limit(func): # 装饰器：参数和返回值都是函数
    @wraps(func)
    def inner(*args, **kwargs):
        if session.get('account'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('api_user.login'))
    return inner

def getOpenid(code):
    if code:
        app_id = ''
        app_secret = ''
        req_params = {
            'appid':app_id,
            'secret':app_secret,
            'js_code':code,
            'grant_type': 'authorization_code'
        }
        wx_login_api = 'https://api.weixin.qq.com/sns/jscode2session'
        response = requests.get(wx_login_api, params=req_params)
        openid = response.json().get('openid')  # 得到用户关于当前小程序的OpenID
        if openid:
            # session_key = data['session_key']
            # return (openid, session_key)
            return openid
    return None

def docResponse(path):
    resp = make_response(open(path).read())
    resp.headers['Content-type'] = "application/json;charset=UTF-8"
    return resp

class Rsa():
    # def __init__(self, public_key=None, private_key=None):
    #     self.public_key = public_key
    #     self.private_key = private_key
    # def createRsaKeysPem(self, public_pem_save_path='./public_key.pem', private_pem_save_path='./private_key.pem', bytes=2048):
    #     (pub_key, pri_key) = rsa.newkeys(bytes)
    #     with open(public_pem_save_path, 'wb+') as f:
    #         f.write(pub_key.save_pkcs1('PEM'))
    #     with open(private_pem_save_path, 'wb+') as f:
    #         f.write(pri_key.save_pkcs1('PEM'))
    #     return (pub_key, pri_key)
    def fromPemLoadRsaPubKey(self, path):
        with open(path, 'rb') as f:
            pem = f.read()
            self.public_key = rsa.PublicKey.load_pkcs1(pem)
        return self.public_key
    # def fromPemLoadRsaPriKey(self, path):
    #     with open(path, 'rb') as f:
    #         pem = f.read()
    #         self.private_key = rsa.PrivateKey.load_pkcs1(pem)
    #     return self.private_key
    def encrypt(self, data, public_key=None):
        if public_key is None:
            public_key = self.public_key
        return rsa.encrypt(data, public_key)
    # def decrypt(self, data, private_key=None):
    #     if private_key is None:
    #         private_key = self.private_key
    #     return rsa.decrypt(data, private_key)
_rsa = Rsa()