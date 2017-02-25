# -*- coding: utf-8 -*-

from requests import get, post
from cookielib import CookieJar
from common import Course
from parser import SchoolException
from time import time
import re

ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0'
accept = 'text/plain, */*; q=0.01'
lang = 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'
xrw = 'XMLHttpRequest'


def header(referer = None, api = False, **kwargs):
    headers = {
        'User-Agent': ua,
        'Accept': accept,
        'Accept-Language': lang
    }

    if referer:
        headers['Referer'] = referer
    if api:
        headers['X-Requested-With'] = xrw

    for key, value in kwargs.items():
        headers[key] = value

    return headers


def match_value(name, text):
    regex = re.search(r'name=\"%s\" value=\"([A-Za-z0-9_\-]*)\"/>' % name, text)
    if not regex:
        return ''
    try:
        return regex.group(1)
    except IndexError:
        return ''


class UESTC():
    def __init__(self, username, password, **kwargs):
        if username == '' or password == '':
            raise SchoolException('用户名或密码为空')

        self.username = username
        self.password = password
        self.logged_in = False
        self.courses = list()
        self.cookies = CookieJar()

    def check_requires_vcode(self):
        url = 'http://idas.uestc.edu.cn/authserver/needCaptcha.html?username=%s&_=%d' % (
            self.username, int(time() * 1000)
        )
        headers = header(referer='http://idas.uestc.edu.cn/authserver/login?'
                                 'service=http://portal.uestc.edu.cn/index.portal')
        r = get(url, headers=headers, cookies=self.cookies)
        for ck in r.cookies:
            self.cookies.set_cookie(ck)

        if r.content.startswith('false'):
            return False
        else:
            return True

    def login(self):
        if self.check_requires_vcode():
            raise SchoolException('需要验证码')

        page = get('http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal', headers=header())
        for c in page.cookies:
            self.cookies.set_cookie(c)

        token = match_value('lt', page.content)
        data = {
            '_eventId': 'submit',
            'dllt': 'userNamePasswordLogin',
            'execution': 'e1s1',
            'lt': token,
            'password': self.password,
            'username': self.username,
            'rmShown': '1'
        }

        signon = post('http://idas.uestc.edu.cn/authserver/login?service=http://portal.uestc.edu.cn/index.portal',
                      headers=header(), data=data, cookies=self.cookies)
        for c in signon.cookies:
            self.cookies.set_cookie(c)
        for history in signon.history:
            for c in history.cookies:
                self.cookies.set_cookie(c)

        if signon.url.startwith('http://portal.uestc.edu.cn'):
            return True
        else:
            raise SchoolException('登录失败')




