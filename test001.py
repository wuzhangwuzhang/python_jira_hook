#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import json
import base64
import requests
import logging
import datetime
from jira import JIRA

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
                auth_base64 = base64.b64encode((self.username + ':' + self.passwd).encode())
                headers.update({'Authorization': 'Basic {}'.format(auth_base64.decode())})

            payload = json.dumps(payload) if payload else {}
            response = requests.request(method, url, headers=headers, data=payload, timeout=10)
            # print(response, response.text)
            return response.status_code, response.json()
        except ConnectionError:
            logger.error("jira connect error!!!")
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


def checkJiraIdAndBranchName(jiraId):
    server_addr, username, passwd, access_token = 'https://jira-pro.uuzu.com','SL_bot', 'qwe123',''  #'MjY3Nzc1NjAyNDA2Oir4Hsi4Lc5duGqVvrTPTEg+jB+r'
    jira_tool = JiraTool(server_addr, username, passwd, access_token)
    resultData = jira_tool.get_issue_by_id(jiraId)
    branchNames = []
    if resultData[0] == 200:
        # branchName = resultData[1]['fields']['fixVersions'][0]['name'].split('_')[1]
        fixVersions = resultData[1]['fields']['fixVersions']
        if fixVersions is not None and len(fixVersions) > 0:
            for i in range(len(fixVersions)):
                # print(fixVersions[i]['name'])
                if '_' in fixVersions[i]['name']:
                    versionArgs = fixVersions[i]['name'].split('_')
                    branchNames.append(versionArgs[1].lower())
        # for data in branchNames:
        #     print(data)
        #print("单号:[{0}]存在,可以提交,允许提交分支：{1}".format(jiraId, listtostring(branchNames,',')))
        return True,branchNames
    else:
        #logger.error("单号:[{0}]不存在,禁止提交".format(jiraId))
        return False,branchNames


def print_args(arg):
    print(arg)


def add_MergeURL(jiraId,mergeUrl):
    print(jiraId,mergeUrl)
    jira = JIRA(server="https://jira-pro.uuzu.com", token_auth='NjM4ODc1MzE5OTczOqC2sqwuVg9AizAuZnmqCEIPNF4Y')
    #jira = JIRA(server='https://jira-pro.uuzu.com', basic_auth=('SL_bot', 'qwe123'))
    issue = jira.issue(jiraId)
    print(issue.id)
    for comment in issue.fields.comment.comments:
        print(comment.body)
    mergerLog = "[查看git变更|{0}]".format(mergeUrl)
    jira.add_comment(issue, mergerLog)  # 添加评论
    return

def listtostring(lst, delimiter=''):
    """
    将list转为字符串
    :param lst: list, 待转化为字符串的列表
    :param delimiter: str, 列表中各个元素的分隔符，默认为''
    :return: str, 转化后的字符串
    """
    return delimiter.join(map(str, lst))

def main():
    # $keyword $jiraId $desc $branchName
    argLength = len(sys.argv)
    keyword = ""
    jiraId = ""             #SLPK-27685  jira测试单号
    desc = ""
    refBranchName = ""      #refs/head/hy/dev/SLPK-27685
    mergeUrl = ""
    #print("argLength:{0}".format(argLength))
    if argLength >= 3:
        keyword = sys.argv[1]
        jiraId = sys.argv[2]
        desc = sys.argv[3]
    else:
        logger.error("[python] 参数不对")
        sys.exit(1)

    if argLength > 4:
        refBranchName = sys.argv[4]

    if argLength > 5:
        mergeUrl = sys.argv[5]

    #logger.info("[python]:keyword:{0} jiraId:{1} desc:{2} refname:{3} mergeUrl:{4}".format(keyword, jiraId, desc, refBranchName,mergeUrl))
    result,branchNames = checkJiraIdAndBranchName(jiraId)
    logger.info("jira查询结果:{0} 单号:{1}上可提交分支个数:{2} 单号允许提交分支:{3}".format(result,jiraId,len(branchNames),branchNames))
    if not result:
        print("单号不存在(如果是管理员Merge的,请修改提交日志格式),先找策划或者QA开单吧!")
        #logger.error("单号不存在(如果是管理员Merge的,请修改提交日志格式),先找策划或者QA开单吧!\n")
        sys.exit(1)
    else:
        if refBranchName == "":
            logger.error("远程分支获取失败!")
            sys.exit(1)

        argCount = refBranchName.count("/")
        if argCount == 0:
            logger.error("远程分支格式错误:{0}".format(refBranchName))
            return

        if len(branchNames) == 0:
            if argCount <= 3:
                print('jira单号:{0}提交分支名未指定,请找点咪修改该单号对应的提交分支,如果非要进版本,提交到Dev'.format(jiraId))
                logger.error('jira单号:{0}提交分支名未指定,请找点咪修改该单号对应的提交分支,如果非要进版本,提交到Dev'.format(jiraId))
                sys.exit(1)
            else:
                print('jira单号:{0}提交分支名未指定,功能特性分支，允许提交个人分支'.format(jiraId))
        else:
            # print("refBranchName argCount:",argCount)
            if argCount <= 3:
                remoteName = refBranchName.split('/')[2].lower()
                if remoteName in branchNames:
                    print("提交通过,单号:【{0}】&&分支:【{1}】校验通过,可以提交\n".format(jiraId,refBranchName))
                    logger.info("提交通过,单号:【{0}】&&分支:【{1}】校验通过,可以提交\n".format(jiraId,refBranchName))
                    #add_MergeURL(jiraId,mergeUrl)
                else:
                    # url = "https://jira-pro.uuzu.com/browse/{0}".format(jiraId)
                    logger.info("提交不通过:{0} 分支校验不通过,可以提交到:【{1}】当前提交分支：【{2}】\n".format(jiraId,listtostring(branchNames,','), remoteName))
                    print("提交不通过:{0} 分支校验不通过,可以提交到:【{1}】当前提交分支：【{2}】\n".format(jiraId,listtostring(branchNames,','), remoteName))
                    sys.exit(1)
            else:
                logger.info("个人开发分支:[{0}] 提交检查通过\n".format(refBranchName))

if __name__ == '__main__':
    current_date = datetime.date.today().strftime("%Y")
    filename = "log_{0}.txt".format(current_date)
    print("日志名:{0}".format(filename))
    Log_Format = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(filename=filename,
                        filemode="a",
                        format=Log_Format,
                        level=logging.DEBUG)
    logger = logging.getLogger()
    # main()
    #add_MergeURL('SLPK-19897',"https://gitlab.uuzu.com/xiyou/workspace/-/merge_requests/12523")  #添加评论测试