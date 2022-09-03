##############################################################
# to_mysql
# create table, insert data
##############################################################

import pymysql
import re
import numpy as np


class ToMySQL:

    def __init__(self, values, ConnDB, dbconn, cur):
        self.values = values
        self.ConnDB = ConnDB
        self.dbconn = dbconn
        self.cur = cur
        self.sql_mode = self.ConnDB.exec(self.cur, 'SELECT @@SESSION.sql_mode')[0][0]

    def create_table(self, col_maxlen, tablename):
        sql = "drop table if exists {0};create table {0}(".format(tablename)
        for col, maxLen in col_maxlen.items():
            colType = "varchar(255)"
            if type(maxLen) == int:
                if maxLen > 255:
                    colType = "TEXT"
                if maxLen > 65535:
                    colType = "MEDIUMTEXT"
                if maxLen > 16777215:
                    colType = "LONGTEXT"

            sql = sql + "`{0}` {1} default null,".format(col, colType)

        sql = sql[:-1] + ")"

        try:
            self.ConnDB.exec(self.cur, sql)
        except:
            try:
                sql = re.sub(r"varchar\(\d+\)", "text", sql)
                self.ConnDB.exec(self.cur, sql)
            except:
                sql = sql + ' engine=myisam'
                self.ConnDB.exec(self.cur, sql)
        return tablename, sql

    def insert_data(self, dataset, tablename, created_sql, dir=None):
        if dataset.empty:
            return
        if not self.values['mode1']:
            sql = "select column_name, COLUMN_KEY from information_schema.`COLUMNS` " \
                  "where table_schema = '{0}' and table_name = '{1}'".format(self.values['dbname'], tablename)
            columns = self.ConnDB.exec(self.cur, sql)
            exists_columns = []
            for column in columns:
                if column[0] in dataset.columns:
                    exists_columns.append(column[0])
            if self.values['add_tname']:
                exists_columns.remove(self.values['add_tname'])
            if not exists_columns:
                raise NoMatchedColumnError('no matched columns')
            dataset = dataset[exists_columns]

        if self.values['mode3']:
            sql = "select column_name from information_schema.`COLUMNS` " \
                  "where table_schema = '{0}' and table_name = '{1}' and COLUMN_KEY = 'PRI'" \
                  "".format(self.values['dbname'], tablename)

            keys = self.ConnDB.exec(self.cur, sql)
            if not keys:
                raise NoPrimaryKeysError('There is no primary key on the table')

            sql = ''
            for index, row in dataset.iterrows():
                where = ' where 1=1'
                for key in keys:
                    key = key[0]
                    where += f" and `{key}` = '{row[key]}'"
                sql += f'delete from `{tablename}` {where};'
            self.ConnDB.exec(self.cur, sql)

        columns = dataset.columns
        dataset = np.array(dataset)
        datalist = dataset.tolist()

        cols = '`,`'.join(columns)
        l = len(columns)
        v = '%s,' * l
        v = v[:-1]

        sql = 'insert into `%s`(%s) values(' % (tablename, '`' + cols + '`')
        sql = sql + '%s)' % v
        try:
            self.ConnDB.exec(self.cur, sql, datalist=datalist)
        except pymysql.err.InternalError as reason:
            if self.values['mode1']:
                reason_num_0 = str(reason).split(',')[0].strip('(')
                # utf8mb4
                if reason_num_0 == '1366':
                    try:
                        sql_1 = 'truncate table `{1}`;'.format(tablename)
                        self.ConnDB.exec(self.cur, sql_1)
                        self.ConnDB.exec(self.cur, 'set SESSION sql_mode = ""')
                        self.ConnDB.exec(self.cur, sql, datalist=datalist)
                        self.ConnDB.exec(self.cur, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

                    except pymysql.err.InternalError as reason:
                        reason_num_1 = str(reason).split(',')[0].strip('(')
                        # 1118 error
                        if reason_num_1 == '1118':
                            sql_0 = re.sub('varchar\\(\\d+\\)', 'text', created_sql)
                            sql_1 = 'drop table if exists `{0}`.`{1}`;'.format(self.values['dbname'], tablename)
                            self.ConnDB.exec(self.cur, sql_1)
                            self.ConnDB.exec(self.cur, sql_0)

                            self.ConnDB.exec(self.cur, 'set SESSION sql_mode = ""')
                            self.ConnDB.exec(self.cur, sql, datalist=datalist)
                            self.ConnDB.exec(self.cur, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

                        else:
                            raise pymysql.err.InternalError(str(reason))

                elif reason_num_0 == '1118':
                    sql_1 = re.sub('varchar\\(\\d+\\)', 'text', created_sql)
                    sql_0 = 'drop table if exists `{0}`.`{1}`;'.format(self.values['dbname'], tablename) + sql_1
                    self.ConnDB.exec(self.cur, sql_0)
                    self.ConnDB.exec(self.cur, sql, datalist=datalist)
                else:
                    raise pymysql.err.InternalError(str(reason))
            else:
                raise pymysql.err.InternalError(str(reason))

class NoPrimaryKeysError(Exception):
    # when skip empty table, raise this exception
    pass
class NoMatchedColumnError(Exception):
    # when skip empty table, raise this exception
    pass