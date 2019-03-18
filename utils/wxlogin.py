#coding:utf8
import requests



class WXLogin(object):
    def __init__(self):
        self.oauth2_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        self.userinfo_url = 'https://api.weixin.qq.com/sns/userinfo'
        self.code2session = 'https://api.weixin.qq.com/sns/jscode2session'
        self.appid = 'wxf9b2d303252ea012'
        self.secret = '47b6dd25f2bd1a35cc0ea36d7f886146'


    def get_openid_key(self, code):
        data = {
            'appid': self.appid,
            'secret': self.secret,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        html = requests.get(url=self.code2session, params=data)
        print(html.status_code)
        print(html.text)
        if html.status_code == 200:
            return html.json()

    def get_token(self, code):
        data = {
            'appid': self.appid,
            'secret': self.secret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        html = requests.get(url=self.oauth2_url, params=data)
        print(html.status_code)
        print(html.text)
        if html.status_code == 200:
            return html.json()

    def get_info(self, code):
        token = self.get_token(code)
        data = {
            'access_token': token['access_token'],
            'openid': token['openid'],
            'lang': 'zh-CN'
        }

        html = requests.get(url=self.userinfo_url, params=data)
        if html.status_code == 200:
            return html.json()

if __name__ == '__main__':
    wx = WXLogin()
    wx.get_token('033xn15l0rxWlr1jZ26l06Y05l0xn157')



