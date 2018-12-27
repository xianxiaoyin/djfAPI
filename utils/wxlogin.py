#coding:utf8
import requests



class WXLogin(object):
    def __init__(self):
        self.oauth2_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        self.userinfo_url = 'https://api.weixin.qq.com/sns/userinfo'
        self.appid = 'wxfcb904527f9ed7cd'
        self.secret = '8bfbf1a1ed2dc62b6f71517e55032f1b'

    def get_token(self, code):
        data = {
            'appid': self.appid,
            'secret': self.secret,
            'code': code,
            'grant_type': 'authorization_code'
        }

        html = requests.get(url=self.userinfo_url, params=data)
        if html.status_code == 200:
            return html.json()

    def get_info(self, code):
        token = self.get_token(code)
        data = {
            'access_token': token['access_token'],
            'openid': token['openid'],
            'lang': 'zh-CN'
        }

        html = requests.get(url=self.oauth2_url, params=data)
        if html.status_code == 200:
            return html.json()

if __name__ == '__main__':
    wx = WXLogin()
    wx.get_token('033xn15l0rxWlr1jZ26l06Y05l0xn157')



