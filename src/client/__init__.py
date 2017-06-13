import requests

cmd = "cat /easdgasdg"
remote_ip = "localhost:8000"
import json

class OPTION:
    HELP=0
    FILE_SEND=1
    SEND=2
    GET=3
    GET_ALL=4
    KEEP_LOCAL=5
    ERROR_OPT=10

option = [
    {'opt':'-h', 'id':OPTION.HELP, 'help_info':'print help info'},
    {'opt':'-f', 'id':OPTION.FILE_SEND, 'help_info':'sync the content of file'},
    {'opt':'-s', 'id':OPTION.SEND, 'help_info':'sync the content'},
    {'opt':'-g', 'id':OPTION.GET, 'help_info':'get the last content'},
    {'opt':'-a', 'id':OPTION.GET_ALL, 'help_info':'get all sync data'},
    {'opt':'-k', 'id':OPTION.KEEP_LOCAL, 'help_info':'get all sync data then save to local file'}
    ]
class RequestMethods:
    GET = 'getLast'
    PUT='put'
    GET_ALL='getAll'
    GET_REALLY_ALL='getReallyAll'
    

def put(self, cmd):
    cmd_obj = {'cmd':cmd}
    res = requests.post("http://%s/%s"%(remote_ip,RequestMethods.PUT),params=cmd_obj)
    if res.status_code == 200:
        return True
    else:
        return False

def get():
    res = requests.get("http://%s/%s"%(remote_ip, RequestMethods.GET))
    return (res.status_code, res.content)

def getAll():
    res = requests.get("http://%s/%s" % (remote_ip, RequestMethods.GET_ALL))
    return (res.status_code, res.content)

def printHelp():
    pass

def printError():
    print '>> Error Command! Please use -h to see help <<'

def getOption(args):
    if len(args == 1):
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
        if len(args) == 2 :
            cmd = args[1]
        else:
            cmd = args[2]
        res = put(cmd)
        if res[0]== 200:
            print 'Send Successfully'
        else:
            print res[1]
    elif opt == OPTION.GET:
        res = get()
        if res[0] == 200:
            print res[1]
            
            
    elif opt == OPTION.GET_ALL:
        pass
    elif opt == OPTION.KEEP_LOCAL:
        pass
    elif opt == OPTION.ERROR_OPT:
        pass
        
import sys
if __name__ == '__main__':
    args = sys.argv
    opt = getOption(args)
    exec_cmd(opt,args)
    
        
    
