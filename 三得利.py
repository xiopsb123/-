from datetime import datetime
import os
import requests
import urllib3

# 说明：
# 1. 请先微信小程序搜逢三得利吧，获取ck，格式为：备注#token 多号用&分隔  搜这个Authorization
# 2. 将ck填入sdl变量中，多个ck以&分隔
# 3.ck会过期，请及时更新
# 4.环境变量是sdlck
# 5.会优先获取内置ck,内置有ck时，会忽略环境变量
# 6.请勿滥用，请遵守相关法律法规

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sign_in_url = 'https://xiaodian.miyatech.com/api/coupon/auth/signIn'
query_url = 'https://xiaodian.miyatech.com/api/coupon/auth/signIn/homePage'

# 内置ck
sdl = ""


if not sdl:
    # 从环境变量中获取 sdlck
    sdl = os.getenv('sdlck')

# 检查是否成功获取到 ck
if not sdl:
    print("没有检测到ck，请在环境变量中设置 sdlck,或者内置sdl设置ck")
else:
    users = sdl.split('&')
    user_count = len(users)

    for user in users:
        user_info = user.split('#')
        username = user_info[0]
        ck = user_info[1]

        headers = {
            'Authorization': ck,
            'HH-FROM': '20230130307725',
            'componentSend': '1',
            'HH-APP': 'wxb33ed03c6c715482',
            'HH-CI': 'saas-wechat-app',
        }

        sign_in_response = requests.post(sign_in_url, headers=headers, verify=False)
        sign_in_response_json = sign_in_response.json()

        if 'code' in sign_in_response_json:
            if sign_in_response_json["code"] == "999":
                sign_in_status = sign_in_response_json["msg"]
            elif sign_in_response_json["code"] == "200":
                sign_in_status = sign_in_response_json["data"]["integralToastText"]
            else:
                sign_in_status = "未知签到响应"
        else:
            sign_in_status = "签到响应中缺少 'code' 键"

        query_response = requests.get(query_url, headers=headers, verify=False)
        query_response_json = query_response.json()

        if query_response.status_code == 200:
            data = query_response_json.get('data', {})

            total_integral = data.get('totalIntegral', 0)
            keep_sign_in_days = data.get('keepSignInDays', 0)
            tomorrow_reward = data.get('tomorrowReward', 'None')
            sign_in_month_day_list = data.get('signInMonthDayList', [])

            signed_in_days_this_month = sum(sign_in_month_day_list)

            if keep_sign_in_days < 7:
                days_until_next_reward = 7 - keep_sign_in_days
            elif keep_sign_in_days < 14:
                days_until_next_reward = 14 - keep_sign_in_days
            elif keep_sign_in_days < 21:
                days_until_next_reward = 21 - keep_sign_in_days
            else:
                days_until_next_reward = 21 - (keep_sign_in_days % 21)

            print("-------三得利-------  : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print(f"获取ck: {user_count}✅")
            print(f"用户名: {username}✅")
            print(f"签到状态: {sign_in_status}✅")
            print(f"用户积分: {total_integral}积分✅")
            print(f"连续签到天数: {keep_sign_in_days}天✅")
            print(f"下一次奖励: {tomorrow_reward}积分✅")
            print(f"下一次奖励还有: {days_until_next_reward}天✅")
            print(f"这个月连续签到的天: {signed_in_days_this_month}天✅")
            print("-------三得利-------  : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        elif query_response.status_code == 401:
            print(f"获取ck多少个: {user_count}")
            print(f"用户名: {username}")
            print(f"ck状态:过期, 请重新获取❌️")
            print("-------三得利-------  : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
            print(f"查询请求失败，状态码: {query_response.status_code}")
