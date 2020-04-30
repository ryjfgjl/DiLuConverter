# connect to mysql

import pymysql
import os
from common.handleconfig import HandleConfig

class ConnDB():

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.server = self.HandleConfig.handle_config("g", "global", "use_server")
        self.host = self.HandleConfig.handle_config('g', self.server, 'host')
        self.user = self.HandleConfig.handle_config('g', self.server, 'user')
        self.passwd = self.HandleConfig.handle_config('g', self.server, 'password')
        self.port = int(self.HandleConfig.handle_config('g', self.server, 'port'))

    def conndb(self, db=None, charset='utf8'):
        self.db = db
        conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port, charset=charset, database=db)

        return conn

        # execute sql
    def exec(self, conn, sql, kill=False, COMMAND=None):
        #conn = self.conndb()
        cur = conn.cursor()
        database = self.db
        if kill:
            killsql = "SELECT CONCAT('kill ',id) FROM information_schema.`PROCESSLIST` WHERE DB = '{}'".format(database)
            if COMMAND:
                killsql = "SELECT CONCAT('kill ',id) FROM information_schema.`PROCESSLIST` WHERE DB = '{}' OR COMMAND = 'Sleep'".format(database)

            cur.execute(killsql)
            killids = cur.fetchall()
            killids = list(killids)

            idx = 0
            for killid in killids:
                killids[idx] = (list(killid))[0]
                killidsql = killids[idx]
                cur.execute(killidsql)
                idx = idx + 1
        for s in sql.split(";"):
            if s != "":
                cur.execute(s)

        conn.commit()
        cur.close()
        return cur

    # exec cmd
    def cmd(self, db, op, file):
        if op == "mysql":
            cmd_statement = "{0} -u{1} -p{2} -h{3} -P{4} {5} --default-character-set=utf8 < \"{6}\"".format(op,self.user,self.passwd,self.host,self.port,db,file)
        print(cmd_statement)
        ret = os.system(cmd_statement)

        return ret