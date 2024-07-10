from datetime import datetime

import requests
import json
import random
''''''''''''''''''''
# 说明：
# 1. 请先登录https://panservice.mail.wo.cn/h5/activitymobile/scratch?activityId=mcGM6BOC2%2FXPOJnsZQYjNw%3D%3D，获取ck，格式为：备注#token  搜这个access-token
# 2. 将ck填入ck_list变量中，多个ck以&分隔
# 3.ck会过期，请及时更新
# 4.请勿滥用，请遵守相关法律法规
''''''''''''''''''''

# 填写ck
ck_list = " "

# 随机生成 User-Agent
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
]
user_agent = random.choice(user_agents)

# 随机生成 sec-ch-ua
sec_ch_ua = '"Chromium";v="122", "Not(A:Brand";v="24", "Android WebView";v="122"'

# 随机生成 sec-ch-ua-mobile
sec_ch_ua_mobile = "?1"

# 随机生成 sec-ch-ua-platform
sec_ch_ua_platform = '"Android"'

# 随机生成 accept-language
accept_languages = [
    "en-US,en;q=0.9",
    "zh-CN,zh;q=0.8",
    "es-ES,es;q=0.7",
    "fr-FR,fr;q=0.6"
]
accept_language = random.choice(accept_languages)

ck_entries = ck_list.split('&')

print("-------联通抽奖-------  : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print(f"获取ck {len(ck_entries)} 个")

for ck_entry in ck_entries:
    remark, ck = ck_entry.split('#')

    url = "https://panservice.mail.wo.cn/wohome/v1/lottery"

    headers = {
        "Host": "panservice.mail.wo.cn",
        "content-length": "98",
        "sec-ch-ua": sec_ch_ua,
        "sec-ch-ua-mobile": sec_ch_ua_mobile,
        "access-token": ck,
        "user-agent": user_agent,
        "content-type": "application/json",
        "accept": "application/json, text/plain, */*",
        "client-id": "10086",
        "sec-ch-ua-platform": sec_ch_ua_platform,
        "origin": "https://panservice.mail.wo.cn",
        "x-requested-with": "com.tencent.mm",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://panservice.mail.wo.cn/h5/activitymobile/scratch?activityId=mcGM6BOC2%2FXPOJnsZQYjNw%3D%3D",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": accept_language
    }

    data = {
        "bizKey": "newLottery",
        "bizObject": {
            "lottery": {
                "activityId": "mcGM6BOC2/XPOJnsZQYjNw==",
                "type": 3
            }
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    response_data = response.json()

    if response_data["meta"]["message"] is None:
        print(f"用户名 {remark}: 今日已经抽过奖了")
        print("抽奖结果: 没有抽奖次数")
    elif response_data["meta"]["message"] == "success":
        prize_name = response_data["result"]["prizeName"]
        print(f"用户名 {remark}: 抽奖结果: {prize_name}")
    else:
        print(f"用户名 {remark}: ck 无效或已过期")

print("-------联通抽奖-------  : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
