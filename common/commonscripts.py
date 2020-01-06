"""
common scripts used usually
"""

import easygui
import pymysql
import os

class CommonScripts:

    def __init__(self):
        pass

    # handle config.ini
    def handle_config(self, option=None, section=None, key=None, value=None):
        import configparser
        conf = configparser.ConfigParser()
        configini = "config.ini"

        try:
            conf.read(configini)
            if option == 'g':
                value = conf.get(section, key)
                return value
            elif option == 's':
                conf.set(section, key, value)
            elif option == "a":
                conf.add_section(section)
            elif option == "rs":
                conf.remove_section(section)
            elif option == "ro":
                conf.remove_option(section, key)

            with open(configini, 'w') as fw:
                conf.write(fw)
            return conf

        except:
            easygui.exceptionbox()

    #execute sql
    def exec(self,server,sql, database=None, kill=False, COMMAND=None):
        host = self.handle_config('g', server, 'host')
        user = self.handle_config('g', server, 'user')
        passwd = self.handle_config('g', server, 'password')
        port = int(self.handle_config('g', server, 'port'))

        conn = pymysql.connect(host=host,user=user,passwd=passwd,port=port,charset='utf8')

        cur = conn.cursor()
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
        conn.close()
        return cur

    # exec cmd
    def cmd(self, server, db, op, file=None, fromserver=None, fromdb=None):
        host = self.handle_config('g', server, 'host')
        user = self.handle_config('g', server, 'user')
        password = self.handle_config('g', server, 'password')
        port = int(self.handle_config('g', server, 'port'))

        if fromserver:
            fromhost = self.handle_config('g', fromserver, 'host')
            fromuser = self.handle_config('g', fromserver, 'user')
            frompassword = self.handle_config('g', fromserver, 'password')

        msg = '{0} {1}.{2} {3}'.format(op, host, db, file)
        if op == "mysql":
            cmd_statement = "{0} -u{1} -p{2} -h{3} -P{4} {5} < \"{6}\"".format(op, user, password, host, port, db, file)

        print(cmd_statement)
        ret = os.system(cmd_statement)

        return ret
