import web
import json
import time
from src.bean.cmd import Cmd
# from src.main import db_service



from src.service.db import dbservice

def file_callback(cmd, ts, ip):
    print '[FILE] callback to write to file'
    


class Controller(object):

    def GET(self, name):
        
        print name + 'in controller --------------'
        global  db_service
        db_service = dbservice.DBService()
        if not name: 
            raise web.seeother('/notFound')
        if name == 'getLast':
            return json.dumps(db_service.get())
        elif name == 'getAll':
            return json.dumps(db_service.getall())
        elif name == 'put':
            db_service.put()
        elif name == 'getReallyAll':
            return json.dumps(db_service.getReallyAll())
        else:
            raise web.seeother('/notfound/tt')
    
    
    def POST(self, name):
        if name == 'put':
            db_service = dbservice.DBService()
            
            i = web.input()
            cmd = i.get('cmd')
            print 'cmd:'+ cmd

            ip = web.ctx.ip
            ts = time.time()
            db_service.put(Cmd(cmd,ts,ip))
            
            return 'insert_suc'
#             return "not found anything xxxxxx"
    
        
