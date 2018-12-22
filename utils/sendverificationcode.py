# coding:utf8

#author: 仙小音
# Time: 2018-12-12
# Desc: 发送短信验证码

import requests

class SendVerificationCode(object):

    def __init__(self, mobile, code):
        self.url = 'https://sms.yunpian.com/v2/sms/single_send.json'
        self.apikey = 'ebab805ae1f2bc0a59da8893066e9275'
        self.mobile = mobile
        self.text = '【仙小音】您的验证码是：{}（5分钟内有效，如非本人操作，请忽略）'.format(code)

    def send(self):
        data = {
            'apikey': self.apikey,
            'mobile': self.mobile,
            'text': self.text,
        }
        html = requests.post(url=self.url, data=data)
        if html.status_code == 200:
            return True
        else:
            return False

if __name__ == '__main__':
    a = SendVerificationCode('15021295585')
    a.send()






