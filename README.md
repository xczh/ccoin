Coding Coins
===================

an automatic acquisition of coding coins tool.

####**If you find some bugs, please send pull request.**

----------
### Basic Usage
```
usage: python ccoin.py [-h] [-u USER] [-p PWD] [-P PUSH_PROJECT] [-B PUSH_BRANCH] [-D PUSH_PATH] [-v]

an automatic acquisition of coding coins tool.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Your coding.net Email or Personality Suffix
  -p PWD, --pwd PWD     Your coding.net Password
  -P PUSH_PROJECT, --push-project PUSH_PROJECT
                        push to which project
  -B PUSH_BRANCH, --push-branch PUSH_BRANCH
                        push to which branch
  -D PUSH_PATH, --push-path PUSH_PATH
                        push to project's dir name
  -v, --version         show program's version number and exit

```
For example, you can use this command to get coins manually:
```
python ccoin.py -u YOUR_NAME -p YOUR_PASS -P PUSH_PROJECT -B PUSH_BRANCH -D PUSH_PATH
```
Also, all these params can be modified through conf.py:
```
USER = 'default_user'
PWD = 'default_pwd'
PUSH_PROJECT = 'dust'
PUSH_BRANCH = 'master'
PUSH_PATH = 'coding_coin'
```
If you provide the command line, the configure in conf.py will be ignore.

### About Automation
You can add the follow command to crontab on your VPS:
```
# m h  dom mon dow   command
3 0 * * * python /path/to/ccoin.py 1>ccoin.log 2>ccoin.err &
```
Don't forget to redirect STDOUT and STDERR!