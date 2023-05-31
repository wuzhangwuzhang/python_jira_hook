#!usr/bin/python
# -*- coding: utf-8 -*-
import requests,sys, json,hashlib,time,os,time,base64,hmac

s_feishu_robot = {
    "Xlsx2LuaRobot":{
        "url":"https://open.feishu.cn/open-apis/bot/v2/hook/a06b8f53-f194-4a96-925f-e869ca98c33b",
        "sign":"SkXhfpf1Y9ho5TULL0h8lh",
        "group_name":"配置表相关工具 程序开发"
    },
    "SLPKBuildRobot":{
        "url":"https://open.feishu.cn/open-apis/bot/v2/hook/c222bd3e-88c3-400c-b70d-eedd0f974740",
        "sign":"gOGAi3NZeWMi5nuGSnUokb",
        "group_name":"丝路打包通知群"
    },
    "SLPKBugRobotTest": {
        "url": "https://open.feishu.cn/open-apis/bot/v2/hook/30c64c00-0394-4158-ad45-1461a6fb4359",
        "sign": "xDWcGOgJf17LaTMOL1jtZf",
        "group_name": "测试"
    },
     "SLPKBugRobot": {
         "url": "https://open.feishu.cn/open-apis/bot/v2/hook/aec8820d-4d11-4f8f-9acd-34c3ee26d385",
         "sign": "thS4xmPbea2QDmAOceJfoh",
         "group_name": "thS4xmPbea2QDmAOceJfoh"
     }

}

class FeiShu(object):
    def __init__(self, robot_name):
        self.robot_name = robot_name
        self.users_info = ""

    def set_at_users(self,*users):
        self.users_info = "".join(map(self._at_user,users))
        return self

    def send(self,text):
        robot_url = s_feishu_robot[self.robot_name]["url"]
        tryTimes = 3
        while tryTimes>0:
            try:
                res = requests.post(robot_url, headers=self._headers(), json=self._body(text))
                print(res.json())
                return self
            except Exception as e:
                print(e)
            tryTimes = tryTimes-1
        raise Exception('------飞书推送失败-----')

    def _headers(self):
        return { "Content-Type": "application/json"}

    def _body(self,text):
        str_timestamp = str(int(round(time.time())))
        return {
            "timestamp": str_timestamp,
            "sign": self._gen_sign(str_timestamp),
            "msg_type": "text",
            "content": {"text": self.users_info + text}
        }

    def _gen_sign(self,timestamp):
        secret = s_feishu_robot[self.robot_name]["sign"]
        # 拼接timestamp和secret
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def _at_user(self,user_id):
        return "<at user_id='%s'>%s</at>" % (user_id,user_id)


def main():
    feishu_xlsx2lua = FeiShu("Xlsx2LuaRobot")
    feishu_xlsx2lua.set_at_users("gull","linych").send("he he")

if __name__ == '__main__':
    robot = FeiShu("SLPKBugRobotTest")
