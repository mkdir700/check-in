import re
import json
import time
import requests
from requests.cookies import cookiejar_from_dict


class BiliBili(object):

    def __init__(self, cookie: str, csrf: str, sid: str):
        t = cookie.split("; ")
        self.cookie = {}
        for d in t:
            k, v = d.split("=")
            self.cookie[k] = v
        print(self.cookie)
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        }
        self.sid = sid
        self.csrf = csrf
        self.session = requests.session()
        self.session.cookies = cookiejar_from_dict(self.cookie)

    def add_times(self, action_type):
        """
        增加抽奖次数的函数
        :param action_type: 表示获取抽奖次数的方式 3分享 4关注
        :return:
        """
        # sid=dd83a687-c800-11ea-8597-246e966235d8&=3&csrf=65be4e6304047d450bab236aa16d31ec
        api = "https://api.bilibili.com/x/activity/lottery/addtimes"
        data = {
            "sid": self.sid,
            "action_type": action_type,
            "csrf": self.csrf
        }
        resp = self.session.post(api, headers=self.headers, data=data)
        print(resp.text)

    def lottery(self):
        """
        抽奖函数
        参数示例
        sid=dd83a687-c800-11ea-8597-246e966235d8&type=1&=65be4e6304047d450bab236aa16d31ec
        :return:
        """
        api = "https://api.bilibili.com/x/activity/lottery/do"
        data = {
            "sid": self.sid,
            "type": 1,
            "csrf": self.csrf
        }
        while 1:
            resp = self.session.post(api, headers=self.headers, data=data)
            if json.loads(resp.text)['code'] == 75415:
                break
            time.sleep(1)

        # code = 75415  message = "抽奖次数不足"
        print(resp.text)


def get_cookie_and_csrf(url):
    resp = requests.get(url)
    # class="ql-code-block">(.*)(?=</div></)
    data = re.findall('class="ql-code-block">(.*)(?=</div></)', resp.text)[0]
    cookie, csrf = data.split("$$$")
    return cookie, csrf


def main_handler(event=None, context=None):

    # 填写你的石墨文档地址，抓取cookie和csrf
    shimo = "https://shimo.im/docs/###/read"
    # 填写你的B站sid
    sid = "xxx"

    cookie, csrf = get_cookie_and_csrf(shimo)
    b = BiliBili(cookie, csrf, sid)
    b.add_times(3)
    time.sleep(1)
    b.add_times(4)
    b.lottery()
    print("Received event: " + json.dumps(event, indent=2))
    print("Received context: " + str(context))
    print("Hello world")
    return "Hello World"


if __name__ == '__main__':
    main_handler()
