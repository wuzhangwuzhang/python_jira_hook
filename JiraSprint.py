from jira import JIRA
import requests

jira = JIRA('https://jira-pro.uuzu.com/', basic_auth=('zhwu', 'Wz147258'))

cookies = jira._session.cookies # 获取jira对象中的cookie
headers = {
    "Accept": "application/json",
}

base_url = "https://jira-pro.uuzu.com"  # jira服务的域名

board_url = base_url + "/rest/agile/1.0/board/?projectKeyOrId=SLPK"  # 获取board的api接口
# projectKeyOrId这个字段需要填写项目的key
res = requests.get(board_url, headers=headers, cookies=cookies)
print(res.json())