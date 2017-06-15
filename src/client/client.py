#!/usr/bin/env python

import requests

cmd = "cat /easdgasdg"
remote_ip = "192.168.122.20:8000"
import json
import platform
import subprocess


class OPTION:
    HELP = 0
    FILE_SEND = 1
    SEND = 2
    GET = 3
    GET_ALL = 4
    KEEP_LOCAL = 5
    ERROR_OPT = 10

class OS_TYPE:
    LINUX=0
    MAC=1
    WINDOWS=2

option = [
    {'opt': '-h', 'id': OPTION.HELP, 'help_info': 'print help info'},
    {'opt': '-f', 'id': OPTION.FILE_SEND, 'help_info': 'sync the content of file'},
    {'opt': '-s', 'id': OPTION.SEND, 'help_info': 'sync the content'},
    {'opt': '-g', 'id': OPTION.GET, 'help_info': 'get the last content'},
    {'opt': '-a', 'id': OPTION.GET_ALL, 'help_info': 'get all sync data'},
    {'opt': '-k', 'id': OPTION.KEEP_LOCAL, 'help_info': 'get all sync data then save to local file'}
]


class RequestMethods:
    GET = 'getLast'
    PUT = 'put'
    GET_ALL = 'getAll'
    GET_REALLY_ALL = 'getReallyAll'


def mac_copy(value):
    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(value.encode('utf-8'))

def win_copy(value):
    pass

def put(cmd):
    cmd_obj = {'cmd': cmd}
    res = requests.post("http://%s/%s" % (remote_ip, RequestMethods.PUT), params=cmd_obj)
    return (res.status_code, res.content)


def get():
    res = requests.get("http://%s/%s" % (remote_ip, RequestMethods.GET))
    return (res.status_code, res.content)




def getAll():
    res = requests.get("http://%s/%s" % (remote_ip, RequestMethods.GET_ALL))
    return (res.status_code, res.content)


def get_os_type():
    system_name = platform.system()
    if system_name == 'Linux':
        return OS_TYPE.LINUX
    elif system_name == 'Darwin':
        return OS_TYPE.MAC
    elif system_name == 'Windows':
        return OS_TYPE.WINDOWS

def opt_get():
    res = get()
    if res[0] == 200:
        cmd = json.loads(res[1]).get('cmd')
        print cmd
        if get_os_type() == OS_TYPE.MAC:
            mac_copy(cmd)

def opt_send(cmd):
    res = put(cmd)
    if res[0] == 200:
        print 'Send Successfully'
    else:
        print res[1]


def printHelp():
    print 'Usage: '
    for item in option:

        print item['opt'] + '    ' + item['help_info']

def opt_getall():
    def space_get(i):
        all_space_count = 6
        num_len = len(str(i))
        return (all_space_count - num_len) * ' '


    res = getAll()
    if res[0] == 200:
        cmds = json.loads(res[1])
        for i in range(len(cmds)):
            print str(i+1) + space_get(i+1) + cmds[i].get('cmd')
        print ' '
        num = input("Please input the num which need to copy:")
        while type(num) != type(1):
            num = input("Please input the correctly num which need to copy:")
        copy_content(cmds[num - 1].get('cmd'))

def copy_content(cmd):
    ostype = get_os_type()
    if ostype == OS_TYPE.MAC:
        mac_copy(cmd)
    elif ostype == OS_TYPE.WINDOWS:
        win_copy(cmd)


def printError():
    print '>> Error Command! Please use -h to see help <<'


def getOption(args):
    if len(args) == 1:
        return OPTION.GET
    if len(args) == 2:
        if args[1] == '-h' or args[1] == '--help':
            return OPTION.HELP
        elif args[1] == '-g':
            return OPTION.GET
        elif args[1] == '-a':
            return OPTION.GET_ALL
        else:
            return OPTION.SEND
    elif len(args) == 3:
        if args[1] == '-s':
            return OPTION.SEND
        elif args[1] == '-f':
            return OPTION.FILE_SEND
        elif args[1] == '-k':
            return OPTION.KEEP_LOCAL
        else:
            return OPTION.ERROR_OPT
    else:
        return OPTION.ERROR_OPT


def exec_cmd(opt, args):
    if opt == OPTION.HELP:
        printHelp()
    elif opt == OPTION.FILE_SEND:
        print 'not implement'
    elif opt == OPTION.SEND:
        cmd = None
        if len(args) == 2:
            cmd = args[1]
        else:
            cmd = args[2]
        opt_send(cmd)
    elif opt == OPTION.GET:
        opt_get()
    elif opt == OPTION.GET_ALL:
        opt_getall()
    elif opt == OPTION.KEEP_LOCAL:
        pass
    elif opt == OPTION.ERROR_OPT:
        pass






import sys

if __name__ == '__main__':
    args = sys.argv
    opt = getOption(args)
    exec_cmd(opt, args)



