## 脚本介绍

学习通健康信息上报脚本

- 支持腾讯云函数，无需服务器
- 依赖云函数可供多人使用

## 使用方法

**1、 立即使用**

API接口，支持任意方式请求

`https://service-m734xlwq-1259447870.gz.apigw.tencentcs.com/release/xuexitong_heath`

参数：

`name`: 手机号码(必填)

`pwd`: 登录密码(必填)

`schoolid`: 学校id(学号登录必填)   

Get请求示例：

`https://service-m734xlwq-1259447870.gz.apigw.tencentcs.com/release/xuexitong_heath?name=账号&pwd=密码`

---

**2、搭建API**

代码已在腾讯云函数上调试可用

1. 新建腾讯云函数

2. 复制代码至`index.py`

3. 开启`API网关触发`

4. 调用API测试

---

**3、仅个人使用**

1. 新建腾讯云函数

2. 复制代码至`index.py`

3. 在代码内配置个人账号密码

4. 开启`定时触发` 每天一次