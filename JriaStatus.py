# -*- coding: utf-8 -*-
import base64
import json
import os.path

import requests
from jira import JIRA
import re

class JiraRestAPI(object):
    # CREATE_META = "{}/rest/api/2/issue/createmeta"  # JIRA_SERVER
    USER_LIST_URL = "{}/rest/api/2/group/member"  # JIRA_SERVER
    PORJECT_LIST_URL = "{}/rest/api/2/project"  # JIRA_SERVER
    ISSUETYPE_URL = "{}/rest/api/2/issue/createmeta/{}/issuetypes"  # JIRA_SERVER, projectIdOrKey
    CREATE_ISSUE_URL = "{}/rest/api/2/issue/"  # JIRA_SERVER

    # testing
    SPECIAL_URL = "{}/rest/api/2/issue/createmeta/{}/issuetypes/{}"  # JIRA_SERVER, projectIdOrKey, issueTypeId
    LIST_PROJECT_ISSUETYPES_URL = "{}/jira/rest/api/2/issue/createmeta/{}/issuetypes?startAt=0&maxResults=50"  # JIRA_SERVER, projectIdOrKey
    GET_ISSUE_URL = "{}/rest/api/latest/issue/{}"  # JIRA_SERVER, issueIdOrKey
    CREATEMETA_URL = "{}/rest/api/2/issue/createmeta"  # JIRA_SERVER


class JiraTool(object):
    def __init__(self, server_addr, username=None, passwd=None, access_token=None):
        self.server_addr = server_addr
        self.username = username
        self.passwd = passwd
        self.access_token = access_token if access_token else None

    def request_jira_reseapi(self, url, method="GET", payload=None):
        try:
            headers = {'Content-Type': 'application/json'}
            if self.access_token is not None:
                headers.update({'Authorization': 'Bearer {}'.format(self.access_token)})
            else:
                auth_base64 = base64.b64encode(self.username + ':' + self.passwd)
                headers.update({'Authorization': 'Basic {}'.format(auth_base64)})

            payload = json.dumps(payload) if payload else {}
            response = requests.request(method, url, headers=headers, data=payload, timeout=10)
            print(response, response.text)
            return response.status_code, response.json()
        except ConnectionError:
            return 500, {}
        except:
            return 500, {}

    def get_jira_user_list(self):
        """only admin user"""
        jira_api = JiraRestAPI.USER_LIST_URL.format(self.server_addr)
        return self.request_jira_reseapi(jira_api, "GET")

    def get_projects_list(self):
        jira_api = JiraRestAPI.PORJECT_LIST_URL.format(self.server_addr)
        return self.request_jira_reseapi(jira_api, "GET")

    def get_special_data(self, projectIdOrKey, issueTypeId):
        jira_api = JiraRestAPI.SPECIAL_URL.format(self.server_addr, projectIdOrKey, issueTypeId)
        return self.request_jira_reseapi(jira_api, "GET")

    def list_project_issuetypes_data(self, projectIdOrKey):
        jira_api = JiraRestAPI.LIST_PROJECT_ISSUETYPES_URL.format(self.server_addr, projectIdOrKey)
        return self.request_jira_reseapi(jira_api, "GET")

    def get_issuetypes(self, projectIdOrKey):
        jira_api = JiraRestAPI.ISSUETYPE_URL.format(self.server_addr, projectIdOrKey)
        return self.request_jira_reseapi(jira_api, "GET")

    def create_issue(self, payload):
        jira_api = JiraRestAPI.CREATE_ISSUE_URL.format(self.server_addr)
        return self.request_jira_reseapi(jira_api, "POST", payload)

    def get_issue_by_id(self, issue_id):
        """"test"""
        jira_api = JiraRestAPI.GET_ISSUE_URL.format(self.server_addr, issue_id)
        return self.request_jira_reseapi(jira_api, 'GET')

    def create_meta(self):
        """test"""
        jira_api = JiraRestAPI.CREATEMETA_URL.format(self.server_addr)
        return self.request_jira_reseapi(jira_api, 'GET')

def checkJriaIdAndBranchName(jiraId):
    server_addr, username, passwd, access_token = 'https://jira-pro.uuzu.com', 'xxx', 'xxx', 'ODQxOTk4MDcxNjg4OtyE8CzhSnnGpWuY6sHvQjSasrfB'
    jira_tool = JiraTool(server_addr, username, passwd, access_token)
    resultData = jira_tool.get_issue_by_id(jiraId)
    branchName = ""
    if resultData[0] == 200:
        # branchName = resultData[1]['fields']['fixVersions'][0]['name'].split('_')[1]
        fixVersions = resultData[1]['fields']['fixVersions']
        if fixVersions is not None and len(fixVersions) > 0:
            if '_' in fixVersions[0]['name']:
                versionArgs = fixVersions[0]['name'].split('_')
                branchName = versionArgs[1]
        print("单号：{0} 存在,可以提交,提交分支：{1}".format(jiraId, branchName))
        return branchName
    else:
        print("单号：{0} 不存在,禁止提交".format(jiraId))
        return branchName

def getJriaIdCommit(jiraId):
    server_addr, username, passwd, access_token = 'https://jira-pro.uuzu.com', 'xxx', 'xxx', 'ODQxOTk4MDcxNjg4OtyE8CzhSnnGpWuY6sHvQjSasrfB'
    jira_tool = JiraTool(server_addr, username, passwd, access_token)
    resultData = jira_tool.get_issue_by_id(jiraId)
    branchName = ""
    if resultData[0] == 200:
        # branchName = resultData[1]['fields']['fixVersions'][0]['name'].split('_')[1]
        fixVersions = resultData[1]['fields']['fixVersions']
        if fixVersions is not None and len(fixVersions) > 0:
            if '_' in fixVersions[0]['name']:
                versionArgs = fixVersions[0]['name'].split('_')
                branchName = versionArgs[1]
        print("单号：{0} 存在,可以提交,提交分支：{1}".format(jiraId, branchName))
        return branchName
    else:
        print("单号：{0} 不存在,禁止提交".format(jiraId))
        return branchName
        os.path.exists()

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('oldrev', help='old object name stored in the ref')
    # parser.add_argument('newrev', help='new object name stored in the ref')
    # parser.add_argument('refname', help='full name of the ref')

    pushBranchName = "Master"
    # for line in sys.stdin:
    #     try:
    #         args = parser.parse_args(line.strip().split(' '))
    #         pushBranchName = args.refname
    #         print("pldVer:{0} newVer:{1} refName：{2}".format(args.oldrev, args.newrev, args.refname))
    #     except IOError as ex:
    #         # May happen for type=file arguments if the user gives a non-existing file path.
    #         sys.stderr.write(str(ex) + '\n')
    #         sys.exit(1)
    #     except subprocess.CalledProcessError as ex:
    #         sys.stderr.write(str(ex) + '\n')
    #         sys.exit(ex.returncode)

    # jiraBranchName = checkJriaIdAndBranchName('SLPK-19428')
    # if pushBranchName == jiraBranchName:
    #     print("提交校验通过")
    # else:
    #     print("提交校验不通过")
    #
    # jiraBranchName = checkJriaIdAndBranchName('SLPK-13329')
    # if pushBranchName == jiraBranchName:
    #     print("提交校验通过")
    # else:
    #     print("提交校验不通过")


    # jiraBranchName = checkJriaIdAndBranchName('SLPK-18777')
    # if pushBranchName == jiraBranchName:
    #     print("提交校验通过")
    # else:
    #     print("提交校验不通过")

    jira = JIRA(server="https://jira-pro.uuzu.com",token_auth = 'ODQxOTk4MDcxNjg4OtyE8CzhSnnGpWuY6sHvQjSasrfB')
    # print(jira)  # <jira.client.JIRA object at 0x7fa9dab97588>
    # projects = jira.projects()
    # print(projects)
    issue = jira.issue('SLPK-19897')
    print(issue.id)
    for comment in issue.fields.comment.comments:
        print(comment.body)

    #issue.update(fields={"labels": ["Azure", "DevOps"]})  # 更新Labels
    #print(issue.fields.labels)  # 打印Labels
    #issue.delete()  # 直接删除issue（不是修改状态）

    # 21是RELEASED，11是ON GOING，31是BLOCKED，41是IMPLEMENTATION，51是VERIFICATION，61是APPROVED，71是CODE REVIEW，81是INTEGRATING，91是READY FOR QA
    #jira.transition_issue(issue, transition='21')
    # print(issue.fields.status)  # 打印status,注意这里的状态是一开始的状态。分析：可能是close()之后才生效
    # print(issue.fields.issuetype)  # Task
    # commmentLog = "[git提交查看1|https://gitlab.uuzu.com/xiyou/workspace/-/merge_requests/8892]"
    # jira.add_comment(issue, commmentLog)  # 添加评论




