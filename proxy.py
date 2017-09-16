import shutil
import requests
from io import BytesIO
from flask import Flask, send_file, Response, make_response, request


URL_BASE = 'https://200.123.180.122:5743'
ID = '3382953'
SALDO = '/rest/getSaldoCaptcha/'
app = Flask(__name__)


def get():
    res = requests.get(URL_BASE + '/captcha.png', verify=False)
    cookie = res.headers['Set-Cookie']
    body = BytesIO(res.content)
    return body, cookie


@app.route("/captcha.png")
def hello():
    body, cookie = get()
    jsession = cookie.split(';')[0].split('=')[1]
    response = make_response(body.read())
    response.headers['Content-Type'] = 'image/png'
    response.set_cookie('JSESSIONID', jsession)
    return response


@app.route("/saldo/<captcha>")
def saldo(captcha):
    jsessionid = request.cookies['JSESSIONID']
    url = URL_BASE + SALDO + ID + '/' + captcha
    res = requests.get(url, verify=False, cookies={'JSESSIONID': jsessionid})
    return res.content
