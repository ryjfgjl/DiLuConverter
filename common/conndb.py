# connect to mysql

import pymysql
import os

class ConnDB():

    def conndb(self, host, port, user, passwd, db=None, charset='utf8'):
        conn = pymysql.connect(host=host, user=user, passwd=passwd, port=port, charset=charset, database=db)
        return conn

    # execute sql
    def exec(self, conn, sql, kill=True, datalist=[]):
        cur = conn.cursor()
        # kill db process first
        pid = conn.thread_id()
        #currentwork = self.HandleConfig.handle_config("g", "global", "currentwork")
        database = conn.db

        if database:
            database = database.decode('utf8')
            killsql = "SELECT CONCAT('kill ',id) FROM information_schema.`PROCESSLIST` WHERE DB = '{0}' and id <> {1}".format(database, pid)
            cur.execute(killsql)
            killids = cur.fetchall()
            killids = list(killids)

            idx = 0
            for killid in killids:
                killids[idx] = (list(killid))[0]
                killidsql = killids[idx]
                try:
                    cur.execute(killidsql)
                except:
                    continue
                idx = idx + 1
    
        if datalist:
            cur.executemany(sql, datalist)
        else:
            for s in sql.split(";"):
                if s != "":
                    cur.execute(s)

        conn.commit()
        cur.close()

        return cur
