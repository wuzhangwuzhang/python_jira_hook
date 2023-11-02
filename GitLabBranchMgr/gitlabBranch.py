import re
import notify
import gitlab
from datetime import datetime
from GitLabBranchMgr.dateTools import Datetools

# 分支允许存在的时间,超过14天的算过期
BranchCanExitsDays = 14
# 分支记信息
needDeleteBranchDic = {}

def notify2Develop(user, issueMsg):
    notify.FeiShu("SLPKFeiShuTest").set_at_users(user).send(issueMsg)


# anonymous read-only access for public resources (GitLab.com)
gl = gitlab.Gitlab()

# anonymous read-only access for public resources (self-hosted GitLab instance)
gl = gitlab.Gitlab('https://gitlab.uuzu.com/')

gl = gitlab.Gitlab(url='https://gitlab.uuzu.com/', private_token='ojhB2Cm3yuKy_76-wFu9',
                   http_username='zhwu@uuzu.com', http_password="Wz147258")
gl.auth()  # 安全认证

# list all the projects
# projects = gl.projects.list(iterator=True)
# for project in projects:
#     print(project)

needDeleteBranchDic = {}
project = gl.projects.get(3325)  # 项目的id '3325'   gotClient projectId：2183
print(project.description)

# mrs = project.mergerequests.list(iterator=True) for mr in mrs: if mr.attributes['state'] == 'opened': print("id:{0}
# title:{1} 描述:{2} 源分支:{3} 目标分支:{4} 链接:{5} 状态：{6}".format(mr.attributes['iid'], mr.attributes['title'],
# mr.attributes[ 'description'].replace( "\n", ""), mr.attributes[ 'source_branch'], mr.attributes[ 'target_branch'],
# mr.attributes['web_url'], mr.attributes['state']))

patten = r"SLPK-\d+"

branches = project.branches.list(get_all=True)
# branches = project.branches.list(merged=True, iterator=True)

for branch in branches:
    # print(branch.name,branch.protected,branch.web_url,branch.commit['message'],branch.commit['author_name'],branch.commit['created_at'])
    date_string = branch.commit['created_at']
    parsed_date = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f%z")
    # 获取年、月和日
    year = parsed_date.year
    month = parsed_date.month
    day = parsed_date.day
    hour = parsed_date.hour
    minute = parsed_date.minute
    second = parsed_date.second

    match = re.search(patten, branch.name)
    now = datetime.now()
    curYear = now.year
    curMonth = now.month
    curDay = now.day

    dateTools = Datetools()
    createDayOfYear = dateTools.day_of_year(year, month, day)

    curDayOfYear = dateTools.day_of_year(curYear, curMonth, curDay)
    existDays = curDayOfYear - createDayOfYear

    if match:
        if year == curYear and existDays > BranchCanExitsDays:
            result = branch.name.split("/")
            ownerName = result[0]
            if len(result) < 3:
                ownerName = branch.commit['author_name']    #如果个人分支命名不正规,获取最后一次提交人
            if not needDeleteBranchDic.__contains__(ownerName):
                needDeleteBranchDic[ownerName] = []
            needDeleteBranchDic[ownerName].append([branch.commit['author_name'], branch.name, branch.web_url,
                                                   datetime(year, month, day, hour, minute, second), existDays,
                                                   branch.commit['author_email']])

# 创建的分支按日期对字典的键进行升序排序(降序前加负号或者not)
for key in needDeleteBranchDic:
    needDeleteBranchDic[key] = sorted(needDeleteBranchDic[key], key=lambda x: x[3].timestamp())

for key in needDeleteBranchDic.keys():
    tips = f"【请删除不用的分支】\n"
    for item in needDeleteBranchDic[key]:
        tips = tips + "分支:{0} {1} 创建日期:{2}\n".format(item[1], item[2], item[3])
    #notify2Develop(key, tips)
    print(tips)
