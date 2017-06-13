import sqlite3
'''
db name: cmd.db

    table name: CMD
    column: 
           (id, cmd, timestamp, ip)
    trigger:
           keep the count of db is 1000
           
    table name: CurCmd
    column: 
           (cmd, timestamp, ip)
    trigger:
           keep the count of db is 1
'''
from src.bean.cmd import Cmd


class DBService:
    def __init__(self):
        print 'comming db service'
        self.conn = None
#         self.file_callback  = file_write_callback
        self.connect()
        
    def connect(self):
        self.conn = sqlite3.connect('service/db/cmd.db')
    
    def get(self):
        cursor = self.conn.execute("SELECT cmd,timestamp,ip from CurCmd")
        cmd = {}
#         if cursor
        res = cursor.fetchone()
        if res is None:
            cursor = self.conn.execute("SELECT cmd,timestamp,ip from CMD order by id desc limit 1")
            res = cursor.fetchone()
            if res is not None:
                cmd = {'cmd':res[0], 'ts':res[1], 'ip':res[2]}
        else:
            cmd = {'cmd':res[0], 'ts':res[1], 'ip':res[2]}
        
        
        self.conn.execute("DELETE from CurCmd")
        self.conn.commit()
        return cmd
    
    def getall(self):
        cursor = self.conn.execute("SELECT cmd,timestamp,ip,id from CMD order by id desc limit 100")
        cmd_list = []
        for row in cursor:
            cmd_list.append({'cmd':row[0], 'ts':row[1], 'ip':row[2]});
            
        cmd_list=list(reversed(cmd_list))  
        return cmd_list
    
    def getReallyAll(self):
        cursor = self.conn.execute("SELECT cmd,timestamp,ip from CMD order by id")
        cmd_list = []
        for row in cursor:
            cmd_list.append({'cmd':row[0], 'ts':row[1], 'ip':row[2]});
            
        cmd_list=list(reversed(cmd_list))  
        return cmd_list
    
    def put(self, o):
        self.conn.execute("INSERT INTO CMD (id,cmd,timestamp,ip) \
      VALUES (null,'%s',%s,'%s')"%(o.cmd,o.ts,o.ip));
        self.conn.commit()
        
        self.conn.execute("DELETE from CurCmd")
        self.conn.execute("INSERT INTO CurCmd (cmd,timestamp,ip) \
      VALUES ('%s',%s,'%s')"%(o.cmd,o.ts,o.ip));
        self.conn.commit()
        
#         self.file_callback(o.cmd,o.ts,o.ip)
        
    def _put(self, o):
        self.conn.execute("INSERT INTO CMD (id,cmd,timestamp,ip) \
      VALUES (3,'%s',%s,'%s')"%(o.cmd,o.ts,o.ip));
     
    def _get_cur_cmd(self):
        cursor = self.conn.execute("SELECT cmd,timestamp,ip from CurCmd")
        cmd = {}
        for row in cursor:
            cmd = {'cmd':row[0], 'ts':row[1], 'ip':row[2]}
        
        return cmd 
    
    
    def __del__(self):
        print 'leave db service'
        self.conn.close()



if __name__ == "__main__":
    conn = sqlite3.connect('cmd.db')
    cur = conn.execute("SELECT cmd,timestamp,ip from CMD")
    xx = cur.fetchone()
    print xx
#     conn.execute("DELETE from CMD")
#     conn.execute("DELETE from CurCmd")
#     conn.commit()
#     conn.close()
    
#     conn.execute("INSERT INTO CMD (id,cmd,timestamp,ip) \
#       VALUES (null,'123',1241,'asdgasdg');")
#     conn.commit()
#     for x in conn.execute("select count() from CMD;"):
#         print x[0]
#     conn.execute('drop table CMD')

#     conn.execute('''CREATE TABLE CurCmd
#             (cmd           TEXT    NOT NULL,
#             timestamp            INT     NOT NULL,
#             ip        CHAR(50) NOT NULL) ; ''')  
# 
#     conn.execute('''CREATE TABLE CMD
#             (id INTEGER PRIMARY KEY AUTOINCREMENT,
#             cmd           TEXT    NOT NULL,
#             timestamp            INTEGER     NOT NULL,
#             ip        CHAR(50) NOT NULL) ; ''')
        
#     db = DBService()
#     db.connect()
    
#     db.put(Cmd('cat12313 a12a',1231421,'1.0.0.2'))
#     
#     db.put(Cmd('cat12313 a12a',1231421,'1.0.0.13'))
    
#     print db._get_cur_cmd()
#     
#     db.get()
#     
#     print db._get_cur_cmd()
#     allcmd = db.getall()
#     print allcmd
