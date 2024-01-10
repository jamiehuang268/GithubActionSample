# 安装依赖 pip3 install requests html5lib bs4 schedule
import os
from datetime import datetime

import requests
import json
from bs4 import BeautifulSoup
import http.client
import json

conn = http.client.HTTPSConnection("www.kdocs.cn")
payload = "{\"Context\":{\"argv\":{},\"data\":\"Sheet2\",\"range\":\"A1\"}}"
headers = {
    'Content-Type': "application/json",
    'AirScript-Token': "1H96cQezhYBDzNdU18Yu5Z"
    }
conn.request("POST", "/api/v3/ide/file/268902559482/script/V2-5gTdSNa64VuXJ5fe4XMRVa/sync_task", payload, headers)
res = conn.getresponse()
data = res.read()
parsed_data = json.loads(data.decode("utf-8"))
print(data.decode("utf-8"))
num_value = parsed_data["data"]["result"]["num"]
txt_value = str(parsed_data["data"]["result"]["txt"]).replace("\n", "")
print(num_value)
print(txt_value)
txt_value = """
123
456
789
"""


# 从测试号信息获取
appID = "wxd7e59e0f23f1df39"
appSecret = "46c19f0d8f36b02f6e09818f268c94c6"
# 收信人ID即 用户列表中的微信号
openId = os.environ.get("oaSMP66cd7YlnxuDuhOJ8u1MTWG8")
# 天气预报模板ID
weather_template_id = os.environ.get("HzoucWPEzFmHgSxT-IxPQqJb0o6iaZ6iT25Nzv_rTzk")




def get_access_token():

    url = 'https://api.weixin.qq.com/cgi-bin/token'

    params = {
        'grant_type': 'client_credential',
        'appid': appID,
        'secret': appSecret
    }

    response = requests.get(url, params=params)
    json_response = response.json()
    access_token = json_response.get('access_token')
    print(access_token)
    return access_token


def get_weather(my_city):
    urls = ["http://www.weather.com.cn/textFC/hb.shtml",
            "http://www.weather.com.cn/textFC/db.shtml",
            "http://www.weather.com.cn/textFC/hd.shtml",
            "http://www.weather.com.cn/textFC/hz.shtml",
            "http://www.weather.com.cn/textFC/hn.shtml",
            "http://www.weather.com.cn/textFC/xb.shtml",
            "http://www.weather.com.cn/textFC/xn.shtml"
            ]
    for url in urls:
        resp = requests.get(url)
        text = resp.content.decode("utf-8")
        soup = BeautifulSoup(text, 'html5lib')
        div_conMidtab = soup.find("div", class_="conMidtab")
        tables = div_conMidtab.find_all("table")
        for table in tables:
            trs = table.find_all("tr")[2:]
            for index, tr in enumerate(trs):
                tds = tr.find_all("td")
                # 这里倒着数，因为每个省会的td结构跟其他不一样
                city_td = tds[-8]
                this_city = list(city_td.stripped_strings)[0]
                if this_city == my_city:

                    high_temp_td = tds[-5]
                    low_temp_td = tds[-2]
                    weather_type_day_td = tds[-7]
                    weather_type_night_td = tds[-4]
                    wind_td_day = tds[-6]
                    wind_td_day_night = tds[-3]

                    high_temp = list(high_temp_td.stripped_strings)[0]
                    low_temp = list(low_temp_td.stripped_strings)[0]
                    weather_typ_day = list(weather_type_day_td.stripped_strings)[0]
                    weather_type_night = list(weather_type_night_td.stripped_strings)[0]

                    wind_day = list(wind_td_day.stripped_strings)[0] + list(wind_td_day.stripped_strings)[1]
                    wind_night = list(wind_td_day_night.stripped_strings)[0] + list(wind_td_day_night.stripped_strings)[1]

                    # 如果没有白天的数据就使用夜间的
                    temp = f"{low_temp}——{high_temp}摄氏度" if high_temp != "-" else f"{low_temp}摄氏度"
                    weather_typ = weather_typ_day if weather_typ_day != "-" else weather_type_night
                    wind = f"{wind_day}" if wind_day != "--" else f"{wind_night}"
                    return this_city, temp, weather_typ, wind
def get_daily_love():
    # 每日一句情话
    url = "https://api.lovelive.tools/api/SweetNothings/Serialization/Json"
    r = requests.get(url)
    all_dict = json.loads(r.text)
    sentence = all_dict['returnObj'][0]
    daily_love = sentence
    return daily_love


def send_weather(access_token, weather):
    today = datetime.now().date()
    today_str = today.strftime("%Y年%m月%d日")

    openId = "oaSMP66cd7YlnxuDuhOJ8u1MTWG8"
    weather_template_id = "HzoucWPEzFmHgSxT-IxPQqJb0o6iaZ6iT25Nzv_rTzk"

    body = {
        "touser": openId,
        "template_id": weather_template_id,
        "url": "https://weixin.qq.com",
        "data": {
            "date": {
                "value": today_str
            },
            "region": {
                "value": weather[0] if weather[0] is not None else ""
            },
            "weather": {
                "value": weather[2] if weather[2] is not None else ""
            },
            "temp": {
                "value": weather[1] if weather[1] is not None else ""
            },
            "wind_dir": {
                "value": txt_value
            },
            "today_note": {
                "value": txt_value
            }
            # Add more data fields as needed
        }
    }

    # Construct the request data following the provided example
    request_data = {
        "grant_type": "client_credential",
        "appid": "APPID",  # Replace with your actual app ID
        "secret": "APPSECRET",  # Replace with your actual app secret
        "force_refresh": False
    }

    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(access_token)
    headers = {'Content-Type': 'application/json'}  # Set content type to JSON

    print(requests.post(url, data=json.dumps(body), headers=headers, params=request_data).text)

# Note: Replace "APPID" and "APPSECRET" with your actual app ID and app secret.



def weather_report(this_city):
    # 1.获取access_token
    access_token = get_access_token()
    #access_token = "76_2NYJC6lD7A6EYPTP5h3ljdjAnK0RwFMpQw45tdNJJ4zPnJlPncZru8cFf1Ilop02NZRR4SbQ_UT-idN7wKLohJbpYDxAN01426tdNNN_HL984QrZ-zw4UoFQ2qwKYHaAHACQZ"

    # 2. 获取天气
    weather = get_weather(this_city)
    print(f"天气信息： {weather}")
    # 3. 发送消息
    send_weather(access_token, weather)



if __name__ == '__main__':
    weather_report("苏州")
