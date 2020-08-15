import re
import requests
from requests.cookies import cookiejar_from_dict


class EduCoder(object):

    def __init__(self, cookie: str):
        d = {}
        for item in cookie.split("; "):
            k, v = item.split("=")
            d[k] = v
        self.session = requests.session()
        self.session.cookies = cookiejar_from_dict(d)

    def sign(self):
        api = "https://www.educoder.net/api/users/attendance.json"
        resp = self.session.post(api, verify=False)
        if resp.status_code == 200:
            return "签到成功"


def main_handler(event=None, context=None):
    shimo = "https://shimo.im/docs/###/"
    resp = requests.get(shimo)
    cookie = re.findall('class="ql-code-block">(.*)(?=</div></)', resp.text)[0]
    # print(cookie)
    e = EduCoder(cookie)
    e.sign()
    # print("Received event: " + json.dumps(event, indent = 2))
    print("Received context: " + str(context))
    print("Hello world")
    return "Hello World"


if __name__ == '__main__':
    main_handler()
