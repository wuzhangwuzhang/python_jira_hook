import gitlab
import requests
import response as response

#gl = gitlab.Gitlab(url='http://192.168.255.129', private_token='c5uU93yXCFDob4USp6aN')
gl = gitlab.Gitlab(url='https://gitlab.uuzu.com/', private_token='tvAcuyt8xAjS3_9bYxTR',http_username='zhwu@uuzu.com',http_password="Wz147258")

gl.auth()  # 安全认证
# result = []
# for each in gl.projects.list(all=True):
# 	# each是每个项目的信息，这里只保存名称和ID，如果想要其他信息，可以自行打印出来，按需获取
# 	result.append([each.name, each.id])
# print(result)

all_owned_projects = gl.projects.list(owned=True, get_all=True)

# 获取所有project
projects = gl.projects.list(all=True)
for project in projects:
	print (project.name,project.id,project.http_url_to_repo)

project = gl.projects.get(3325)    #项目的id '3325'

# ---------------------------------------------------------------- #
# 获取指定项目的所有merge request
# mrs = project.mergerequests.list(get_all=True)
# print(mrs)
# ---------------------------------------------------------------- #


# ---------------------------------------------------------------- #
# 获取 指定mr info
# mr = project.mergerequests.get(9243)
# print(mr)


# diffs = mr.diffs.list()
# print(f"diff:{diffs}")


PATH_PATTERNS = [
    'Client/Assets/Scripts',
]

mrs = project.mergerequests.list(state='opened', iterator=True)


seen_mr = {}

for mr in mrs:
    # https://docs.gitlab.com/ee/api/merge_requests.html#list-merge-request-diffs
    real_mr = project.mergerequests.get(mr.get_id())
    real_mr_id = real_mr.attributes['iid']
    real_mr_url = real_mr.attributes['web_url']

    for diff in real_mr.diffs.list(iterator=True):
        real_diff = real_mr.diffs.get(diff.id)

        for d in real_diff.attributes['diffs']:
            print(f"fileOldPath:{d['old_path']},fileNewPath:{d['new_path']},isNewFile:{d['new_file']},isReNamedFile:{d['renamed_file']},isDeleted:{d['deleted_file']}")#d['diff']
            #过滤特殊文件cs代码
            for p in PATH_PATTERNS:
                if p in d['old_path']:
                    print("MATCH: {p} in MR {mr_id}, status '{s}', title '{t}' - URL: {mr_url}".format(
                        p=p,
                        mr_id=real_mr_id,
                        t=real_mr.attributes['title'],
                        mr_url=real_mr_url))

                    if not real_mr_id in seen_mr:
                        seen_mr[real_mr_id] = real_mr

print("\n# MRs to update\n")

for id, real_mr in seen_mr.items():
    print("- [ ] !{mr_id} - {mr_url}+ Status: {s}, Title: {t}".format(
        mr_id=id,
        mr_url=real_mr.attributes['web_url'],
        s=real_mr.attributes['detailed_merge_status'],
        t=real_mr.attributes['title']))



#获取指定MR id的信息

real_mr = project.mergerequests.get(9245)
real_mr_id = real_mr.attributes['iid']
real_mr_url = real_mr.attributes['web_url']
for diff in real_mr.diffs.list(iterator=True):
    real_diff = real_mr.diffs.get(diff.id)
    for d in real_diff.attributes['diffs']:
        print(f"fileOldPath:{d['old_path']},fileNewPath:{d['new_path']},isNewFile:{d['new_file']},isReNamedFile:{d['renamed_file']},isDeleted:{d['deleted_file']}")  # d['diff']


