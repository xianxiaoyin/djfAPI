# coding:utf8
import requests

'''
将输入的中文翻译成维吾尔文
'''

class Translate(object):
    def __init__(self, cfrom, to):
        self.url = 'http://www.mzywfy.org.cn/ajaxservlet'
        self.cfrom = cfrom
        self.to = to

    def runs(self, contents):
        my_list = []
        count = int(len(contents) / 1000 + 1)
        if count > 1:
            for i in range(1, count):
                my_list.append(contents[:1000*i])
            return ''.join([self.run(j) for j in my_list])
        else:
            return self.run(contents)


    def run(self, content):

        data = {
            'src_text': content,
            'from': self.cfrom,
            'to': self.to,
            'url': 2,
        }
        headers = {
            "Referer": "http://www.mzywfy.org.cn/translate.jsp",
        }
        html = requests.post(url=self.url, data=data, headers=headers)
        print(html.status_code)
        print(html.text)
        if html.status_code == 200:
            return html.json()['tgt_text']
        else:
            return '翻译故障'

if __name__ == '__main__':
    a = Translate('zh', 'uy')
    # a = Translate('uy', 'zh')
    mystr = """我是谁"""
    print(a.runs(mystr))

