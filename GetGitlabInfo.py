import sys

import gitlab
import logging

# gl = gitlab.Gitlab(url='http://192.168.255.129', private_token='c5uU93yXCFDob4USp6aN')
gl = gitlab.Gitlab(url='https://gitlab.uuzu.com/', private_token='tvAcuyt8xAjS3_9bYxTR',http_username='zhwu@uuzu.com',http_password="Wz147258")

gl.auth()  # 安全认证
# result = []
# for each in gl.projects.list(all=True):
# 	# each是每个项目的信息，这里只保存名称和ID，如果想要其他信息，可以自行打印出来，按需获取
# 	result.append([each.name, each.id])
# print(result)

all_owned_projects = gl.projects.list(owned=True, get_all=True)

## 获取所有project
# projects = gl.projects.list(all=True)
# for project in projects:
# 	print (project.name,project.id,project.http_url_to_repo)

# workspace 3325 https://gitlab.uuzu.com/xiyou/workspace.git

project = gl.projects.get(3325)    #项目的id '3325'
members = project.members
users = members.list(all=True)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
)
logging.debug('This message is skipped as a level is set as INFO')
logging.info('So should this')
logging.warning('And this, too')
# logging.error('Testing non-ASCII character, Ø and ö')

for user in users:
    if True:
        # 修改用户属性权限
        # logging.info("正在处理当前用户: {user}".format(user=user.username))
        # user.can_create_group = False
        # user.projects_limit = 0
        # user.save()
        logging.info(
            "用户名：{user} ,名字:{name}, ID:{id} access_level:{access_level} project_id:{project_id}".format(
                user=user.username, name=user.name, id=user.id,access_level = user.access_level,project_id = user.project_id))

# commit = project.commits.list(all=True)[0]  #获取最新的提交人信息，这里我取的第一个人的
# git_name =commit.committer_name   #可以直接提取用户信息里的name,也可以获取提交的id,created_at,message
