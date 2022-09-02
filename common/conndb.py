"""
connect to database
execute sql
"""

import pymysql
import cx_Oracle
import pymssql
from pyhive import hive


class ConnDB:

    def __init__(self):
        self.values = {}

    def conndb(self):
        # distribute a connection to database
        dbtype = self.values['dbtype']
        host = self.values['host']
        port = int(self.values['port'])
        user = self.values['user']
        passwd = self.values['passwd']
        db = self.values['dbname']
        charset = 'utf8'
        if dbtype == 'MySQL':
            dbconn = pymysql.connect(host=host, user=user, passwd=passwd, port=port, charset=charset, database=db)
        elif dbtype == 'Oracle':
            dbconn = cx_Oracle.connect(user, passwd, host + ':' + str(port) + '/' + db)
        elif dbtype == 'SQL Server':
            dbconn = pymssql.connect(host=host, user=user, password=passwd, port=port, charset=charset, database=db)
        elif dbtype == 'Hive':
            dbconn = hive.connect(host=host, username=user, password=passwd, port=port, database=db, auth="CUSTOM")
        return dbconn

    def exec(self, cur, sql, datalist=None):
        # execute sql
        if datalist:
            # insert data
            cur.executemany(sql, datalist)
        else:
            # other sql
            for s in sql.split(";"):
                if s != "":
                    cur.execute(s)
        try:
            results = cur.fetchall()
        except:
            results = None
        return results
