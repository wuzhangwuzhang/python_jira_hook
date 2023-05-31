import http.server
import socketserver
import json
import re
import io
import notify

IP = "172.20.16.21"
PORT = 1314


def string_builder(cSharpFilesDic):
    output = io.StringIO()
    for key in cSharpFilesDic:
        output.write(f"{key} {cSharpFilesDic[key]}")
        output.write('\n')
    result = output.getvalue()
    return result

def notify2Develop(user,issueMsg):
    notify.FeiShu("SLPKBugRobotTest").set_at_users(user).send(issueMsg)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def getMatchFile(self,info):
        # 匹配"c#"和"lua"
        matches = re.findall(r'\b\w+\.(?:cs|lua)\b', info)
        print("info:{0} 匹配到目标:{1}".format(info,matches))
        return matches

    def do_POST(self):
        # - request -

        content_length = int(self.headers['Content-Length'])
        # print('content_length:', content_length)

        if content_length:
            input_json = self.rfile.read(content_length)
            input_data = json.loads(input_json)
        else:
            input_data = None

        # print(input_data)
        #print("提交分支:{0} before:{1} after:{2} develop:{3} developName:{4}".format(input_data['ref'],input_data['before'],input_data['after'],input_data['user_username'],input_data['user_name']))

        commits = input_data['commits']
        # print("commits length:{0}  git push commit len:{1}".format(len(input_data['commits']),input_data['total_commits_count']))

        index = 0
        cSharpFilesDic = {}
        for item in commits:
            index = index + 1
            # print("第{0}次提交 id：{1} message:{2} title:{3}".format(index,item['id'],item['message'],item['title']))

            #git新增
            added = item['added']
            if len(added) > 0:
                for addItem in added:
                    # print("新增的文件:{0}".format(addItem))
                    # 封装测试
                    # scriptFile = self.getMatchFile(addItem)
                    # print("scriptFile:",scriptFile)

                    if addItem.endswith('.cs'):
                        # print("C#新增")
                        cSharpFilesDic[addItem] = f"新增|提交人:{input_data['user_name']}"
                #print("------------------------")

            # git修改
            modified = item['modified']
            if len(modified) > 0:
                for modifyItem in modified:
                    # print("修改的文件:", modifyItem)
                    if modifyItem.endswith('.cs'):
                        # print("C#被修改")
                        cSharpFilesDic[modifyItem] = f"修改|提交人:{input_data['user_name']}"
                #print("------------------------")

            # git删除
            removed = item['removed']
            if len(removed) > 0:
                for removeItem in removed:
                    # print("删除的文件:", removeItem)
                    if removeItem.endswith('.cs'):
                        # print("C#被删除")
                        cSharpFilesDic[removeItem] = f"删除|提交人:{input_data['user_name']}"
                #print("------------------------")

        # - response -
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

        output_data = {'status': 'OK', 'result': 'HELLO WORLD!'}
        output_json = json.dumps(output_data)

        self.wfile.write(output_json.encode('utf-8'))

        #被修改的C#代码
        tips = string_builder(cSharpFilesDic)
        notification = f"分支:【{input_data['ref']}】 发现C#修改:\n{tips}"

        print(notification)
        notify2Develop('zhwu',notification)

Handler = MyHandler

try:
    with socketserver.TCPServer((IP, PORT), Handler) as httpd:
        print(f"Starting http://{IP}:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("Stopping by Ctrl+C")
    httpd.server_close()  # to resolve problem `OSError: [Errno 98] Address already in use`