#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import base64
import requests

class JiraRestAPI(object):
    # Base Request URL
    USER_LIST_URL = "{}/rest/api/2/group/member"  # JIRA_SERVER
    PORJECT_LIST_URL = "{}/rest/api/2/project"  # JIRA_SERVER
    ISSUETYPE_URL = "{}/rest/api/2/issue/createmeta/{}/issuetypes"  # JIRA_SERVER, projectIdOrKey
    CREATE_ISSUE_URL = "{}/rest/api/2/issue/"  # JIRA_SERVER

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
            # print(response, response.text)
            return response.status_code, response.json()
        except ConnectionError:
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

    def get_issue_by_id(self, issue_id):
        jira_api = JiraRestAPI.GET_ISSUE_URL.format(self.server_addr, issue_id)
        return self.request_jira_reseapi(jira_api, 'GET')

    def add_comment(self, jira_key,context):
        """添加comment"""
        comment = context
        self.jira_conn.add_comment(jira_key, comment)


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
        # print("单号：{0} 存在,可以提交,提交分支：{1}".format(jiraId, branchName))
        return True,branchName
    else:
        # print("单号：{0} 不存在,禁止提交 {1}".format(jiraId, branchName))
        return False,branchName


def print_args(arg):
    print(arg)


def main():
    # $keyword $jiraId $desc $branchName
    keyword = sys.argv[1]
    jiraId = sys.argv[2]
    desc = sys.argv[3]
    branchName = sys.argv[4]
    print("keyword:{0} jiraId:{1} desc:{2} refname:{3}".format(keyword, jiraId, desc, branchName))
    result = checkJriaIdAndBranchName(jiraId)
    if result[0] == False:
        print("单号不存在,先找策划或者QA开单吧!")
        sys.exit(1)
    else:
        jiraBranchName = result[1]
        if len(result[1]) == 0:
            print('jira单号:{0}提交分支名未指定,请找点咪修改该单号对应的提交分支,如果非要进版本,提交到Dev'.format(jiraId))
            sys.exit(1)
        else:
            remoteName = branchName.split('/')[2].lower()
            jiraBranchName = jiraBranchName.lower()
            if jiraBranchName == remoteName:
                print("提交通过:单号&分支正确,可以提交")
                sys.exit(0)
            else:
                #url = "https://jira-pro.uuzu.com/browse/{0}".format(jiraId)
                print("提交不通过:{0} 分支校验不通过,应该提交到:【{1}】当前提交分支：【{2}】".format(jiraId,jiraBranchName, remoteName))
                sys.exit(1)
            sys.exit(0)

if __name__ == '__main__':
    main()
