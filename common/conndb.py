"""
connect to database
execute sql
"""

import pymysql
import cx_Oracle
import pymssql
from pyhive import hive


class ConnDB:

    def __init__(self, values):
        self.values = values
        self.dbtype = self.values["dbtype"]

    def conndb(self, charset='utf8'):
        # distribute a connection to database
        host = self.values['host']
        port = int(self.values['port'])
        user = self.values['user']
        passwd = self.values['passwd']
        db = self.values['dbname']
        if self.dbtype == 'MySQL':
            conn = pymysql.connect(host=host, user=user, passwd=passwd, port=port, charset=charset, database=db)
        elif self.dbtype == 'Oracle':
            conn = cx_Oracle.connect(user, passwd, host+':'+str(port)+'/'+db)
        elif self.dbtype == 'SQL Server':
            conn = pymssql.connect(host=host, user=user, password=passwd, port=port, charset=charset, database=db)
        elif self.dbtype == 'Hive':
            conn = hive.connect(host=host, username=user, password=passwd, port=port, database=db, auth="CUSTOM")
        return conn

    def exec(self, conn, sql, datalist=None):
        # execute sql
        cur = conn.cursor()

        if datalist:
            # insert data
            data = [tuple(i) for i in datalist]
            cur.executemany(sql, data)
        else:
            # other sql
            for s in sql.split(";"):
                if s != "":
                    cur.execute(s)
        try:
            results = cur.fetchall()
        except:
            results = None
        cur.close()
        conn.commit()
        return results
