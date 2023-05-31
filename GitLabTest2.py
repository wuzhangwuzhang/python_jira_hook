# import gitlab
#
#
# class GitlabAPI(object):
#
#     def __init__(self, *args, **kwargs):
#         # self.gl = gitlab.Gitlab('https://xxxxxxxxxxx.com', private_token='xxxxxxxxxx',api_version = '3')
#         self.gl = gitlab.Gitlab(url='https://gitlab.uuzu.com/', private_token='tvAcuyt8xAjS3_9bYxTR',
#                            http_username='zhwu@uuzu.com', http_password="Wz147258")
#
#         def get_user_id(self, username):
#             """
#             通过用户名获取用户id
#             :param username:
#             :return:
#             """
#             user = self.gl.users.get_by_username(username)
#             return user.id
#
#         def get_group_id(self, groupname):
#             """
#             通过组名获取组id
#             :param groupname:
#             :return:
#             """
#             group = self.gl.groups.get(groupname, all=True)
#             return group.id
#
#         def get_user_projects(self, userid):
#             """
#             获取用户所拥有的项目
#             :param userid:
#             :return:
#             """
#             projects = self.gl.projects.owned(userid=userid, all=True)
#             result_list = []
#             for project in projects:
#                 result_list.append(project.http_url_to_repo)
#             return result_list
#
#     def get_group_projects(self, groupname):
#         """
#         获取组内项目！！！！！！！其他博客也有类似方法，实测不能拿到群组内项目，现经过小改动，亲测可满足要求
#         :param groupname:
#         :return:
#         """
#         group = self.gl.groups.get(groupname, all=True)
#         projects = group.projects.list(all=True)
#         return projects
#
#     def getContent(self, projectID):
#         """
#         通过项目id获取文件内容
#         :param projectID:
#         :return:
#         """
#         projects = self.gl.projects.get(projectID)
#         f = projects.files.get(file_path='指定项目中的文件路径', ref='master')
#         content = f.decode()
#         # print(content)
#         return content.decode('utf-8')
#
#     def get_all_group(self):
#         """
#         获取所有群组
#         :return:
#         """
#         return self.gl.groups.list(all=True)
#
#
#
# groups = GitlabAPI().get_all_group()
# print(groups)
#
# ## 得到所有project
# projects = GitlabAPI().gl.projects.list(all=True)
# print(projects)


import common_data
import gitlab

gitlab_host = 'https://gitlab.uuzu.com/'
gitlab_token = "tvAcuyt8xAjS3_9bYxTR"
gl = gitlab.Gitlab(gitlab_host, private_token=gitlab_token)


# group = gl.groups.get(group_id)
# projects = group.projects.list(all=True)
# print(len(projects))


def get_branch_info(project_id):
    # # 通过指定id 获取 project 对象
    project_info = gl.projects.get(project_id)
    # branch_info = gl.projects.get(project.id)
    # branches = project_info.branches.list(get_all=True)
    # branch_v4_6_0 = project_info.branches.get('v4.5.0')
    # print(branch_v4_6_0)
    # branch = project_info.branches.create({'branch_name': 'xxxxx', 'ref': 'v4.5.0'})
    tags = project_info.tags.list()
    print("before create ", tags)
    last_tag_name = tags[0].attributes["name"]
    if last_tag_name == 'testv4.5.0':
        print("the tag name %s is already exists" % last_tag_name)
    else:
        tag = project_info.tags.create({'tag_name': 'testv4.5.0', 'ref': 'v4.5.0'})
        print("the tag %s create " % tag)


# 0.新建分支
def create_branch(project_name, branch_name):
    project = gl.projects.get(common_data.project_name_dir[project_name])
    branches = project.branches.list(get_all=True)
    branches_name = []
    i = 0
    while i < len(branches):
        branches_name.append(branches[i].attributes["name"])
        i += 1
    print(branches_name)
    if branch_name not in branches_name:
        print(branch_name)
        print("not exits project ", branch_name)
        branch = project.branches.create({'branch': branch_name, 'ref': 'v4.6.0'})
        print("finish create branch ", branch)
    else:
        print("the branch %s already exits" % branch_name, project_name)


# 1.给group组的所有项目打tag，
def create_tags(project_name, tag_name):
    # # 通过指定name 获取 project 对象
    project = gl.projects.get(common_data.project_name_dir[project_name])

    tags = project.tags.list()
    if len(tags) != 0:
        last_tag_name = tags[0].attributes["name"]
        if last_tag_name == tag_name:
            print("the tag name %s is already exists" % last_tag_name)
        else:
            tag = project.tags.create({'tag_name': tag_name, 'ref': tag_name})
            print("the tag %s created " % tag)
    else:
        tag = project.tags.create({'tag_name': tag_name, 'ref': tag_name})
        print("the tag %s created " % tag.attributes["name"])


# 2.分支保护设置
def branch_protect(project_name, branch):
    project = gl.projects.get(common_data.project_name_dir[project_name])
    # print(project.attributes["name"])
    try:
        p_branches = project.protectedbranches.get(branch)
    except Exception as err:
        print("the branch is not protected", err)
        p_branch = project.protectedbranches.create({
            'name': branch,
            'merge_access_level': gitlab.const.AccessLevel.DEVELOPER,
            'push_access_level': gitlab.const.AccessLevel.MAINTAINER
        })
        print(branch, "protected done")
    else:
        print(project_name, " already protected", p_branches.attributes["name"])


# 3.增加新文件
def add_new_file(project_name):

    project = gl.projects.get(common_data.project_name_dir[project_name])
    # f = project.files.get(file_path='.gitlab-ci.yml', ref='CICD_test')
    # print(f)
    try:
        f = project.files.get(file_path='.gitlab-ci.yml', ref='v4.6.0')
    except Exception as err:
        print("the file in %s is not exits" % project_name, err)
        file_content = open('gitlab-ci.yml', 'r', encoding='UTF-8').read()
        nf = project.files.create(
            {'file_path': '.gitlab-ci.yml', 'branch': 'v4.6.0',
             'content': file_content, 'author_email': 'xxxxx@xxx.com',
             'author_name': 'xxxx',
             'commit_message': 'Add CICD config file'})
        print("add gitlab-ci.yml done", nf)
    else:
        print("the file is exits", f)

# get_branch_info(25506)

# common_data 所有项目的和对应projectID

for project_obj in common_data.project_name_dir:
    print(project_obj)