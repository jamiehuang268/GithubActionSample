import http.client
import json
from wxauto import WeChat
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
txt_value = parsed_data["data"]["result"]["txt"]
print(num_value)
print(txt_value)


wx = WeChat()
who = '文件传输助手'
for i in range(1):
    wx.SendMsg(txt_value, who)
#

print('发送完成！')
