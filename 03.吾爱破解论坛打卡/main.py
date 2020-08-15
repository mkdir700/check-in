import re
import requests
from requests.cookies import cookiejar_from_dict


class WuAiPoJie(object):

    def __init__(self, cookie: str):
        t = cookie.split("; ")
        print(t)
        # messagetext
        self.cookie = {}
        for d in t:
            k, v = d.split("=", 1)
            self.cookie[k] = v
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "https://www.52pojie.cn/index.php"
        }
        self.session = requests.session()
        self.session.headers = self.headers
        self.session.cookies = cookiejar_from_dict(self.cookie)

    def sign(self):
        # 申请签到任务
        apply = "https://www.52pojie.cn/home.php?mod=task&do=apply&id=2"
        # 执行签到任务
        draw = "https://www.52pojie.cn/home.php?mod=task&do=draw&id=2 "
        resp1 = self.session.get(apply, verify=False)
        resp2 = self.session.get(draw, verify=False)
        status = re.findall('<div id="messagetext" class="alert_error">[\s]+<p>(.*)</p>', resp2.text)
        print(status[0])


def main_handler(event=None, context=None):
    # 填写存有cookie的石墨文档公开地址
    shimo = "https://shimo.im/docs/###/"
    resp = requests.get(shimo)
    cookie = re.findall('class="ql-code-block">(.*)(?=</div></)', resp.text)[0]
    print(cookie)
    w = WuAiPoJie(cookie=cookie)
    w.sign()
    # print("Received event: " + json.dumps(event, indent = 2))
    print("Received context: " + str(context))
    print("Hello world")
    return "Hello World"


if __name__ == '__main__':
    main_handler()
