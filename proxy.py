import shutil
import requests
from io import BytesIO
from flask_cors import CORS

from flask import Flask, send_file, Response, make_response, request


URL_BASE = 'https://200.123.180.122:5743'
SALDO = '/rest/getSaldoCaptcha/'
app = Flask(__name__)
CORS(app, supports_credentials=True)


def get():
    res = requests.get(URL_BASE + '/captcha.png', verify=False)
    cookie = res.headers['Set-Cookie']
    body = BytesIO(res.content)
    return body, cookie


@app.route("/")
def index():
    res = requests.get(URL_BASE, verify=False)
    cookie = res.headers['Set-Cookie']
    jsession = cookie.split(';')[0].split('=')[1]
    response = make_response()
    response.set_cookie('JSESSIONID', jsession)
    return response


@app.route("/captcha.png")
def hello():
    body, cookie = get()
    jsession = cookie.split(';')[0].split('=')[1]
    response = make_response(body.read())
    response.headers['Content-Type'] = 'image/png'
    response.set_cookie('JSESSIONID', jsession)
    return response


@app.route("/rest/getSaldoCaptcha/<tarjeta>/<captcha>")
def saldo(tarjeta, captcha):
    jsessionid = request.cookies['JSESSIONID']
    url = URL_BASE + SALDO + tarjeta + '/' + captcha
    res = requests.get(url, verify=False, cookies={'JSESSIONID': jsessionid})
    return res.content
