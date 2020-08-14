import json
import hashlib
import aiohttp
import asyncio


# 填写葫芦侠账号密码
config = {
    "account": "###",
    "password": "###",
}


async def get_all_cate(session) -> list:
    category_api = "http://floor.huluxia.com/category/list/ANDROID/2.0"
    params = {
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.0.0.5.3",
        "versioncode": "20141430",
        "_key": "",
        "device_code": "[w]02:00:00:00:00:00[d]4d7d0e99-4fc7-4cbf-8511-27df7ebb1de7",
        "is_hidden": 1}
    async with session.get(category_api, params=params) as resp:
        resp_dict = json.loads(await resp.text())
        cate_list = []
        if resp_dict["status"] == 1:
            for cate in resp_dict["categories"]:
                cate_list.append(cate["categoryID"])
        return cate_list


async def login(session) -> dict:
    """登录"""
    login_api = "http://floor.huluxia.com/account/login/ANDROID/4.0"
    account = config['account']
    password = config['password']
    # 密码采用的是md5加密方式
    hl = hashlib.md5()
    hl.update(password.encode(encoding="utf-8"))
    password = hl.hexdigest()

    params = {
        "platform": 2,
        "gkey": "000000",
        "app_version": "4.0.0.5.3",
        "versioncode": "20141430",
        "_key": "",
        "device_code": "[w]02:00:00:00:00:00[d]4d7d0e99-4fc7-4cbf-8511-27df7ebb1de7",
    }
    data = {
        'account': account,
        'password': password,
        'login_type': 2
    }
    async with session.post(login_api, params=params, data=data) as resp:
        resp_dict = json.loads(await resp.text())
        return {
            "status": resp_dict["status"],
            "_key": resp_dict["_key"] if resp_dict["status"] == 1 else "登录失败"
        }


async def sign_in(session, key, cate_id):
    sign_api = "http://floor.huluxia.com/user/signin/ANDROID/2.1"
    params = {
        "platform": "2",
        "gkey": "000000",
        "app_version": "4.0.0.5.3",
        "versioncode": "20141430",
        "_key": key,
        "device_code": "[w]02:00:00:00:00:00[d]4d7d0e99-4fc7-4cbf-8511-27df7ebb1de7",
        "cat_id": cate_id,
    }
    async with session.get(sign_api, params=params) as resp:
        try:
            sign_result = json.loads(await resp.text())
        except:
            return "请求签到API失败！"
        return {
            "cate_id": cate_id,
            "status": sign_result['status'],
            "msg": sign_result["msg"] if sign_result['status'] != 1 else "签到成功"
        }


async def main():
    async with aiohttp.ClientSession() as session:
        cates = await get_all_cate(session)
        print(set(cates))

        login_resp = await login(session)
        key = login_resp["_key"]

        sign_tasks = []
        for cate in cates:
            sign_tasks.append(asyncio.create_task(sign_in(session, key=key, cate_id=cate)))
        completed, pending = await asyncio.wait(sign_tasks)
        results = [t.result() for t in completed]
        print('results: {!r}'.format(results))


def main_handler(event=None, context=None):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


if __name__ == '__main__':
    main_handler()
