import argparse
import os
import shutil
import subprocess
import sys

__author__ = 'Werner Beroux <werner@beroux.com>'


def printStatus(msg):
    print('')
    print('\033[1m-----> {} ... \033[0m'.format(msg))
    sys.stdout.flush()


def onPreReceive(oldrev, newrev, refname):
    # The value in `oldrev` will be 0000000000000000000000000000000000000000 if the reference name `refname` is being proposed to be created.
    # The value in `newrev` will be 0000000000000000000000000000000000000000 if the reference name `refname` is being proposed to be deleted.
    # The values of both will be nonzero if the reference name `refname` is being proposed to be updated,
    # i.e., it currently points to git object `oldrev` and if you allow the change, it will point to new object `newsha` instead.

    # Only run this script for the master branch. You can remove this
    # if block if you wish to run it for others as well.
    if refname != 'refs/heads/master':
        sys.exit(0)

    build_and_deploy(newrev)


def build_and_deploy(sha1):
    # We build in a directory named after the project.
    # It may affect some Docker containers names for example.
    project_name = os.path.basename(os.getcwd())
    if project_name.endswith('.git'):
        project_name = project_name[:-4]

    # Since the repo is bare, we need to put the actual files someplace,
    # so we use the temp dir we chose earlier
    printStatus('Checking out commit {}'.format(sha1))
    tmp_dir = os.path.join('/tmp', project_name)
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    subprocess.check_call(['git', 'checkout', '-f', sha1], env={'GIT_WORK_TREE': tmp_dir})
    subprocess.check_call(['git', 'reset', '--hard'], env={'GIT_WORK_TREE': tmp_dir})
    subprocess.check_call(['git', 'clean', '-fdx'], env={'GIT_WORK_TREE': tmp_dir})

    printStatus('Running build')
    subprocess.check_call('./build', cwd=tmp_dir)

    printStatus('Running deploy')
    subprocess.check_call('./deploy', cwd=tmp_dir)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('oldrev', help='old object name stored in the ref')
    parser.add_argument('newrev', help='new object name stored in the ref')
    parser.add_argument('refname', help='full name of the ref')

    for line in sys.stdin:
        try:
            args = parser.parse_args(line.strip().split(' '))
            onPreReceive(args.oldrev, args.newrev, args.refname)
        except IOError as ex:
            # May happen for type=file arguments if the user gives a non-existing file path.
            sys.stderr.write(str(ex) + '\n')
            sys.exit(1)
        except subprocess.CalledProcessError as ex:
            sys.stderr.write(str(ex) + '\n')
            sys.exit(ex.returncode)