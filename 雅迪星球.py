from datetime import datetime

import requests
# 说明：
# 1. 请先在微信小程序中登录雅迪星球，获取ck，格式为：备注#token  搜这个authorization 不要Bearer只要Bearer后面的内容即可
# 2. 将ck填入ck_list变量中，多个ck以&分隔
# 3.请勿滥用，请遵守相关法律法规
''''''''''''''''''''
# 定义ck变量
ck_list = ""

# 将ck_list拆分成单独的条目
ck_entries = ck_list.split('&')

# 签到接口
sign_url = "https://opmd.yadea.com.cn/api/miniprogram/custom-promotion/memberSign"
# 查询积分接口
query_url = "https://opmd.yadea.com.cn/api/miniprogram/custom-promotion/memberSign/signHistory"

print("-------雅迪星球签到日志------- .by:楠枫 : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print(f"获取ck {len(ck_entries)} 个")

for ck_entry in ck_entries:
    if '#' not in ck_entry:
        print(f"无效的ck条目: {ck_entry}")
        continue

    remark, ck = ck_entry.split('#')
    headers = {
        "authorization": ck,
    }

    # 签到请求
    sign_response = requests.post(sign_url, headers=headers)

    if sign_response.status_code == 200:
        sign_data = sign_response.json()
        if sign_data.get("code") == 200:
            integral = sign_data.get("data")
            print(f"用户名 {remark}: 签到成功，积分: {integral}")
        elif sign_data.get("code") == 500 and sign_data.get("msg") == "今日已签到请勿重复签到!":
            print(f"用户名 {remark}: 今日已签到")
        else:
            print(f"用户名 {remark}: 签到请求失败，响应: {sign_response.text}")
    else:
        print(f"用户名 {remark}: 签到请求失败，状态码: {sign_response.status_code}")

    # 查询积分请求
    query_response = requests.get(query_url, headers=headers)

    if query_response.status_code == 200:
        query_data = query_response.json()
        integral = query_data.get("data", {}).get("integral")
        if integral is not None:
            print(f"用户名 {remark}: 积分:✅ {integral}")
        else:
            print(f"用户名 {remark}: 未找到积分信息")
    else:
        print(f"用户名 {remark}: 查询积分请求失败，状态码: {query_response.status_code}")

print("-------雅迪星球签到日志------- .by:楠枫 : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
