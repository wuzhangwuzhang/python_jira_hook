import notify
from jira import JIRA

from developerConfig import developers


def get_bug_inf(bug):
    if (bug.get('inwardIssue')):
        bug_key = bug['inwardIssue']['key']
        bug_info = jr.issue(bug_key)
        info = {'assignee': bug_info.fields.assignee.displayName,
                'creator': bug_info.fields.reporter.displayName}
        issue_item = {
            bug_key: info
        }
        return issue_item
    else:
        return {}

def isContainDevelop(user,list):
    for element in list:
        if user == element:
            return True
    return False

def notify2Develop(user,issueMsg):
    notify.FeiShu("SLPKBugRobot").set_at_users(user).send(issueMsg)

def getIsueInfo(key,value):
    issueMsg = " 您有新的消息，请注意查收，问题数量:{0}\n".format(len(value))
    for index in value:
        data = value[index]
        fixedVersion = ""
        issueTypeName = data.fields.issuetype.name
        issueDesc = data.fields.summary
        if data.fields.fixVersions is not None and len(data.fields.fixVersions) > 0:
            if '_' in data.fields.fixVersions[0].name:
                versionArgs = data.fields.fixVersions[0].name.split("_")
                fixedVersion = versionArgs[1]
            else:
                fixedVersion = data.fields.fixVersions[0].name
        issueURL = "https://jira-pro.uuzu.com/browse/{0}".format(data.key)
        tmpIssueMsg = "【{0}】 {1} {2} {3} {4}".format(issueTypeName, data.key,issueDesc, issueURL,fixedVersion);
        issueMsg += tmpIssueMsg
        issueMsg += "\n"
    print(issueMsg)
    if isContainDevelop(key,developers):
        print("开发者包含：{0}".format(key))
        # notify2Develop(key,issueMsg)
    else:
        print("开发者不包含：{0}".format(key))


if __name__ == '__main__':
    jr = JIRA('https://jira-pro.uuzu.com/', basic_auth=('zhwu', 'Wz147258'))
    projects = jr.projects()  # 查看所有项目
    project = jr.project("SLPK")  # 查看单个项目,需要输入项目的key
    print("项目key=", project.key)
    print("项目名称=", project.name)
    print("项目id=", project.id)
    print("项目影响版本=", project.versions)
    print("项目的模块=", project.components)
    print("项目的原始信息=", project.raw)

    # issue = jr.issue('SLPK-19284')
    # print(issue.fields.assignee.name)

    #'project = SLPK AND issuetype in (TA任务, 任务, 缺陷) AND resolution = Unresolved AND assignee in (currentUser(), membersOf(【丝路】项目组)) order by updated DESC'
    jql = "project = SLPK AND issuetype in (TA任务, 任务, 缺陷) AND status in (待处理, 处理中, 修复中, 挂起, 验收中, 待进行) AND resolution = Unresolved AND assignee in (currentUser(), membersOf(【丝路】项目组)) order by updated DESC"
    issues = jr.search_issues(jql, maxResults=500)

    issuesDic = {}
    issueTotalNumber = 0
    for issue in issues:
        userName = issue.fields.assignee.name
        if userName not in issuesDic:
            # print("key 不存在",issue.fields.assignee.name)
            issuesDic[userName] = {}
            issuesDic[userName][0] = issue
        else:
            # print("key存在",issue.fields.assignee.name)
            length = len(issuesDic[userName])
            issuesDic[userName][length] = issue
        issueTotalNumber = issueTotalNumber + 1
        # print("单号:{0} 处理人:{1} 账号:{2} 单子总数:{3}".format(issue,issue.fields.assignee.displayName,issue.fields.assignee.name,issueTotalNumber))

    # 字典排序
    sorted_dict = dict(sorted(issuesDic.items(), key=lambda item: len(item[1]),reverse=True))

    print("\n问题总数:{0}".format(issueTotalNumber))
    for key in sorted_dict:
        value = sorted_dict[key]
        getIsueInfo(key,value)

