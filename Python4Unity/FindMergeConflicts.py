#!/usr/bin/env python
import os
import sys
import string
import codecs

assets = "E:/workspaceBak/workspace/Client/Asset" #os.path.dirname(os.path.realpath(__file__))  E:\workspaceBak\workspace\Client\Asset
result = []


# Find GUID
def checkConflict(path):
    path = path.replace('\\', '/')
    if not path.endswith(".meta"):
        return

    print(path)
    with codecs.open(path, 'r', encoding='utf8') as file:
        # 逐行读取文件内容
        content = file.read()
        print(content)
        if content.find(">>>>>>>") != -1 or content.find("=======") != -1 or content.find("<<<<<<<") != -1:
            print("line:{0}".format(content.replace("\n", "")))
            result.append(path)


if len(sys.argv) == 2:
    assets = sys.argv[1]

print("check path:",assets)
for root, dirs, files in os.walk(assets):
    for file in files:
        print(file)
        checkConflict(root + '/' + file)

# Output Result
if len(result) != 0:
    print(str(len(result)) + ' Conflict Founded!')  # 打开文件，如果文件不存在则创建新文件
    file = open("output.txt", "w")

    for line in result:
        try:
            file.writelines(line)
            file.writelines("\n")
            os.unlink(line)
            print("Conflict 文件删除成功", line)
        except PermissionError:
            print("Conflict 文件删除失败：另一个程序正在使用此文件，进程无法访问")
    # 关闭文件
    file.close()
else:
    print('Not Found Conflict!')
