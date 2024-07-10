import requests
import json
from datetime import datetime
''''''''''''''''''''
# 说明：
# 1. 请先在微信小程序中登录霸王茶姬，获取ck，格式为：备注#token  搜这个qm-user-token
# 2. 将ck填入bwcjck变量中，多个ck以&分隔
# 3.一天运行一次
# 4.请勿滥用，请遵守相关法律法规
''''''''''''''''''''
# 禁用SSL验证
requests.packages.urllib3.disable_warnings()

# 内置的ck变量
bwcjck = ""

# 签到接口
sign_url = "https://webapi2.qmai.cn/web/cmk-center/sign/takePartInSign"

# 查询积分接口
points_url = "https://webapi2.qmai.cn/web/cmk-center/common/getCrmAvailablePoints"

# 签到统计接口
sign_stats_url = "https://webapi2.qmai.cn/web/cmk-center/sign/userSignStatistics"

# 解析用户输入的ck
cks = bwcjck.split('&')

print("-------霸王茶姬签到日志------- .by:楠枫 : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
print(f"获取ck {len(cks)} 个")

for ck in cks:
    if '#' not in ck:
        print(f"无效的ck格式: {ck}")
        continue
    parts = ck.split('#')
    if len(parts) != 2:
        print(f"无效的ck格式: {ck}")
        continue
    备注, token = parts
    headers = {
        "qm-from": "wechat",
        "qm-user-token": token,
        "content-type": "application/json",
    }

    data = {
        "activityId": "947079313798000641",
    }

    # 签到
    sign_response = requests.post(sign_url, headers=headers, data=json.dumps(data), verify=False)

    if sign_response.status_code == 200:
        sign_data = sign_response.json()
        if sign_data.get('status'):
            print(f"用户名 {备注}: 成功签到")
        else:
            print(f"用户名 {备注}: 今日已签到")
    else:
        print(f"用户名 {备注}: 签到失败，状态码 {sign_response.status_code}")

    # 检查ck是否过期
    if sign_response.status_code == 401 or (sign_response.status_code == 200 and sign_data.get('code') == 401):
        print(f"用户名 {备注}: ck已过期")
        continue

    # 查询签到统计信息
    sign_stats_response = requests.post(sign_stats_url, headers=headers, data=json.dumps(data), verify=False)

    if sign_stats_response.status_code == 200:
        sign_stats_data = sign_stats_response.json()
        sign_days = sign_stats_data.get('data', {}).get('signDays', 0)
        next_sign_days = sign_stats_data.get('data', {}).get('nextSignDays', 0)
        next_reward_list = sign_stats_data.get('data', {}).get('nextRewardList', [{}])

        if next_reward_list:
            next_reward = next_reward_list[0].get('rewardList', [{}])[0]
            reward_name = next_reward.get('rewardName', '无')
            send_num = next_reward.get('sendNum', '未知')
            reward_show_extra = next_reward.get('rewardShowExtra', {})
            expired_date_str = reward_show_extra.get('expiredDateStr', '')

            if reward_name == '积分奖励':
                reward_info = f"{reward_name}{send_num}积分"
            elif reward_name == '买一赠一券（签到打卡30天专享）':
                reward_info = f"{reward_name}(有效期：{expired_date_str}){send_num}张"
            else:
                reward_info = f"{reward_name}{send_num}"

            print(f"连续签到天数:🎉 {sign_days}")
            print(f"距离下一个奖励还有 {next_sign_days} 天")
            print(f"下一个奖励: {reward_info}")
        else:
            print(f"连续签到天数:🎉 {sign_days}")
            print(f"距离下一个奖励还有 {next_sign_days} 天")
            print(f"下一个奖励: 无")
    else:
        print(f"签到统计查询失败，状态码 {sign_stats_response.status_code}")

    # 查询积分
    points_params = {
        "appid": "wxafec6f8422cb357b"
    }

    points_response = requests.get(points_url, headers=headers, params=points_params, verify=False)

    if points_response.status_code == 200:
        points_data = points_response.json()
        if points_data.get('status'):
            print(f"积分:✅ {points_data.get('data')}")
        else:
            print(f"积分查询失败:❌️ {points_data.get('message')}")
    else:
        print(f"积分查询失败，状态码 {points_response.status_code}")

    # 检查ck是否过期
    if points_response.status_code == 401 or (points_response.status_code == 200 and points_data.get('code') == 401):
        print(f"用户名 {备注}: ck已过期")

print("-------霸王茶姬签到日志------- .by:楠枫 : " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
