# !/usr/bin/env python
# -*-coding:utf-8 -*-
import os
from jira import JIRA, Issue


class JiraTool:
    def __init__(self, username, password, project=None):
        self.server = 'https://jira-pro.uuzu.com'
        self.username = username
        self.password = password
        self.project = project
        self.jira_conn = JIRA(server=self.server, basic_auth=(self.username, self.password))  # jira服务器，用户名密码

    def get_projects(self):
        """访问权限的项目列表:[<JIRA Project: key='AR2022011', name='识别', id='12882'>,...]"""
        # for p in self.jira_conn.projects():
        #     print(p.key, p.id, p.name)
        return self.jira_conn.projects()

    def get_project(self, project_id):
        """
        通过项目id/key获取项目主要属性：
        key: 项目的Key
        name: 项目名称
        description: 项目描述
        lead: 项目负责人
        projectCategory: 项目分类
        components: 项目组件
        versions: 项目中的版本
        raw: 项目的原始API数据
        """
        project = {
            'key': self.jira_conn.project(project_id).key,
            'name': self.jira_conn.project(project_id).name,
            'description': self.jira_conn.project(project_id).description,
            'lead': self.jira_conn.project(project_id).lead,
            'components': self.jira_conn.project(project_id).components,
            'versions': self.jira_conn.project(project_id).versions,
            'raw': self.jira_conn.project(project_id).raw
        }
        return project

    def search_jira_jql(self, jql=None, maxnum: int = None):
        """根据jql查询jira,返回[<JIRA Issue: key='PJT-9141', id='302682'>,...]"""
        maxResults = False if maxnum is None else maxnum
        issues = self.jira_conn.search_issues(jql, maxResults=maxResults, json_result=False)
        return issues

    def create_issue(self, issue_dict):
        """
        创建issue,issue_dict = {
        'project': {'id': 10000},
        'summary': 'BUG描述',
        'description': 'BUG详情 \n换行',
        'priority': {'name': 'BUG优先级'},
        'labels': ['标签'],
        'issuetype': {'name': '问题类型-故障'},
        'assignee':{'name': '经办人'} #经办人
        }
        """
        self.jira_conn.create_issue(fields=issue_dict)

    def create_issues(self, issue_list):
        """
        批量创建issue,issue_list = [issue_dict1, issue_dict2, issue_dict3]
        """
        self.jira_conn.create_issues(issue_list)

    def get_issue(self, issue_id):
        """获取issue信息"""
        issue = self.jira_conn.issue(issue_id)
        return issue

    def get_issuefields(self, issue_id):
        """获取issue-fields信息:"""
        issuefields = self.get_issue(issue_id).fields
        fields = {
            'summary': issuefields.summary,
            'assignee': issuefields.assignee,
            'status': issuefields.status,
            'issuetype': issuefields.issuetype,
            'reporter': issuefields.reporter,
            'labels': issuefields.labels,
            'priority': issuefields.priority.name,
            'description': issuefields.description,
            'created': issuefields.created,
            'versions': issuefields.versions,
            'fixVersions': issuefields.fixVersions
        }
        return fields

    def get_summary(self, issue_id):
        """获取issue-summary信息:"""
        issuefields = self.get_issue(issue_id).fields
        return issuefields.summary

    def get_issuelabels(self, issue_id):
        """获取issue-issuelabels信息:"""
        issuefields = self.get_issue(issue_id).fields
        labels = issuefields.labels
        return labels

    def get_status(self, issue_id):
        """查询状态"""
        return self.jira_conn.issue(issue_id).fields.status

    def get_assignee(self, issue_id):
        """查询assignee"""
        return self.jira_conn.issue(issue_id).fields.assignee.name

    def find_description(self, issue_id):
        """查询description信息"""
        return self.jira_conn.issue(issue_id).fields.description

    def update_issue(self, issue_id, issue_dict):
        """
        创建issue,issue_dict = {
        'project': {'id': 10000},
        'summary': 'BUG描述',
        'description': 'BUG详情 \n换行',
        'priority': {'name': 'BUG优先级'},
        'labels': ['标签'],
        'issuetype': {'name': '问题类型-故障'},
        'assignee':{'name': '经办人'} #经办人
        }
        update(assignee={'name': username})
        """
        self.jira_conn.issue(issue_id).update(issue_dict)

    def get_versions(self, jira_key):  # 获取Jira影响版本
        versions = [v.name for v in self.jira_conn.issue(jira_key).fields.versions]
        return versions

    def add_version(self, jira_key, versions_name):  # 为Jira添加影响版本,注意新增的版本在JIRA中是否存在,否则报错
        self.jira_conn.issue(jira_key).add_field_value('versions', {'name': versions_name})

    def del_version(self, jira_key, versions_name):  # 获取Jira影响版本
        oldversions = [i.name for i in self.jira_conn.issue(jira_key).fields.versions]
        newversions = oldversions
        if versions_name in oldversions:
            oldversions.remove(versions_name)
            newversions = oldversions
        versions = [{'name': f} for f in newversions]
        self.jira_conn.issue(jira_key).update(fields={'versions': versions})

    def get_fixversions(self, jira_key):  # 获取Jira影响版本
        fixVersions = [v.name for v in self.jira_conn.issue(jira_key).fields.fixVersions]
        return fixVersions

    def add_fixversions(self, jira_key, fixversions_name):  # 为Jira添加解决版本,注意新增的版本在JIRA中是否存在,否则报错
        self.jira_conn.issue(jira_key).add_field_value('fixVersions', {'name': fixversions_name})

    def del_fixversions(self, jira_key, versions_name):  # 获取Jira影响版本
        oldfixversions = [i.name for i in self.jira_conn.issue(jira_key).fields.fixVersions]
        newfixversions = oldfixversions
        if versions_name in oldfixversions:
            newfixversions.remove(versions_name)
            newfixversions = oldfixversions
        versions = [{'name': f} for f in newfixversions]
        self.jira_conn.issue(jira_key).update(fields={'fixVersions': versions})

    def add_field_value(self, issue_id, key, value):
        issue = self.jira_conn.issue(issue_id)
        issue.add_field_value(field=key, value=value)

    def add_attachment(self, jira_key, picpath):
        """上传附件"""
        issue = self.jira_conn.issue(jira_key)
        with open(picpath, 'rb') as f:
            self.jira_conn.add_attachment(issue, attachment=f)
        f.close()

    def get_comments(self, issue_id):
        """查询comments"""
        comments = self.jira_conn.issue(issue_id).fields.comment.comments
        # return { comment.id:comment.author for comment in comments}
        # return { comment.id:comment.body for comment in comments}
        return comments

    def add_comment(self, jira_key, context, picpath=None):
        """添加comment"""
        if picpath is None or not os.path.exists(picpath):
            comment = context
        else:
            self.add_attachment(jira_key, picpath)
            picname = os.path.basename(picpath)
            comment = f"{context}\r\n!{picname}|thumbnail!"
        self.jira_conn.add_comment(jira_key, comment)

    def update_comment(self, issue_id, comment_id, n_comment):
        """更新comment"""
        issue = self.jira_conn.issue(issue_id)
        comment = self.jira_conn.comment(issue, comment_id)
        comment.update(body=n_comment)

    def delete_comment(self, issue_id, comment_id):
        """删除comment"""
        issue = self.jira_conn.issue(issue_id)
        comment = self.jira_conn.comment(issue, comment_id)
        comment.delete
    def get_transitions(self, issue_id):
        """查询当前权限下问题流程可操作节点"""
        issue = self.jira_conn.issue(issue_id)
        transitions = self.jira_conn.transitions(issue)
        return [(t['id'], t['name']) for t in transitions]

    def update_status(self, issue_id=None, status=None, **kwargs):
        """更新问题流程状态"""
        issue = self.jira_conn.issue(issue_id)
        self.jira_conn.transition_issue(issue, status, **kwargs)

    def close_client(self):  # 关闭链接
        self.jira_conn.close()


if __name__ == '__main__':
    # jiratool = JiraTool(username='SL_bot', password='qwe123')
    jiratool = JiraTool(username='zhwu', password='Wz147258')
    jira_key = "SLPK-19897"
    issue = jiratool.get_issue(jira_key)
    print(issue)
    # # 获取用户所有project
    # projects = jiratool.get_projects()
    # print(projects)
    # for p in projects:
    #     print(p.key,p.id,p.name)

    # # 获取project信息
    # project = jiratool.get_project('SLPK')
    # print(project)

    # # jql查询jira问题
    # jql = '********'
    # issues = jiratool.search_jira_jql(jql)
    # print(issues)
    # # jira_key
    # for i in issues:
    #     print(i.key)
    # jira_key = [i.key for i in issues]
    # print(jira_key)

    # labels = []
    # for issue in issues:
    #     issueinfo = jiratool.get_issuefields(issue)
    #     labels.extend(list(issueinfo['labels']))
    #     print(issue,','.join(list(issueinfo['labels'])))
    #
    # keys = sorted(set(labels)-set(('***','***')))
    # print(keys)
    # dd = {k:labels.count(k) for k in keys}
    #
    # for k in keys:
    #     print(k,labels.count(k))
    # print(sum(list(dd.values())))

    # # 添加附件
    # picpath = r'E:\Attachments\PJT-7533.png'
    # jiratool.add_attachment('PJT-7984',picpath)
    #
    # 添加注释+附件
    # context = r"[查看git变更|{0}]".format("http://www.baidu")
    # jiratool.add_comment(jira_key,context)

    # 测试无权限更新或者删除评论 FUCK
    # for commit in issue.fields.comment.comments:
    #     if int(commit.id) > 227181:
    #         print(commit.body)
    #         commit.update(body='updated comment body')
    #         commit.delete()

    # # # 获取issue信息
    # issueinfo = jiratool.get_issuefields(jira_key)
    # print(issueinfo)
    # # labels = list(issueinfo['labels'])

    # jira_key = 'PJT-7669'
    #
    # # # 查询当前权限下问题流程可操作节点
    # transitions = jiratool.get_transitions(jira_key)
    # print(transitions)
    #
    # # # 获取issue-status信息
    # status = str(jiratool.get_status(jira_key))
    # assignee = jiratool.get_assignee(jira_key)
    # print(assignee)
    # print(status,type(status))
    # # 修改状态
    # jiratool.update_status(jira_key, 31, customfield_12017=examine)

    # # 获取issue-description信息,修改描述信息
    # description = jiratool.find_description('PJT-12537')
    # print(description,type(description))
    # description = description + "\n版本号：v10.0.1 test"
    # jiratool.update_issue('PJT-12537',{'description': description})

    # 获取issue-标签
    # labels = jiratool.get_issuelabels(issue)
    # # 添加或删除标签
    # labels.append("CICD")
    # # labels.remove("CICD")
    # jiratool.update_issue('PJT-9676',{'labels': labels})

    # # 修改优先级
    # jiratool.update_issue('PJT-9676',{'priority': {'name': 'High'}})

    # # # 获取comment
    # comments = jiratool.get_comments('PJT-7470')
    # print(comments)
    # for comment in comments:
    #     if comment.author.displayName in ('***','***'):
    #         print(comment.id,comment.body)

    # 添加影响版本
    # jira_key = "PJT-9145"
    # jiratool.add_version(jira_key,"PJT_V14.1.0")

    # 添加修复版本
    #jira_key = "PJT-11454"
    # jiratool.add_fixversions(jira_key,"PJT_V14.1.0")

    #versions = jiratool.get_versions(jira_key)
    #print(versions)

    # versions = jiratool.del_version(jira_key,"PJT_V14.1.0")
    # print(versions)
    #fixversions = jiratool.get_fixversions(jira_key)
    #print(fixversions)
    #jiratool.add_fixversions(jira_key, "PJT_V14.1.0")
    #fixversions = jiratool.get_fixversions(jira_key)
    #print(fixversions)

    #jiratool.del_fixversions(jira_key, "PJT_V14.1.0")
    #fixversions = jiratool.get_fixversions(jira_key)
    #print(fixversions)