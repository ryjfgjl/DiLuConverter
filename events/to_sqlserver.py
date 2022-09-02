##############################################################
# to_sqlserver
# create table, insert data
##############################################################

import numpy as np


class ToSqlserver:

    def __init__(self, values, ConnDB, dbconn, cur):
        self.values = values
        self.ConnDB = ConnDB
        self.dbconn = dbconn
        self.cur = cur

    # create table
    def create_table(self, col_maxlen, tablename):
        sql = "select 1 from sysobjects where xtype = 'U' and name = '{}'".format(tablename)
        cnt = self.ConnDB.exec(self.cur, sql)
        if len(cnt) > 0:
            sql = 'drop table "{}"'.format(tablename)
            self.ConnDB.exec(self.cur, sql)
        sql = "create table \"{0}\"(".format(tablename)
        for col, maxLen in col_maxlen.items():
            colType = "varchar(255)"
            if type(maxLen) == int:
                if maxLen * 6 > 4000:
                    colType = "text"
                elif maxLen > 0:
                    colType = "varchar({})".format(maxLen * 6)

            sql = sql + "\"{0}\" {1} default null,".format(col, colType)
        if self.values['add_tname']:
            sql = sql + "table_name varchar(255) default '{0}',".format(tablename)
        sql = sql[:-1] + ")"

        self.ConnDB.exec(self.cur, sql)
        return tablename, sql

    # insert into
    def insert_data(self, dataset, tablename, created_sql=None, dir=None):
        if dataset.empty:
            return
        sql = "SELECT name FROM syscolumns WHERE id=object_id('{0}')".format(tablename)
        columns = self.ConnDB.exec(self.cur, sql)
        exists_columns = []
        for column in columns:
            if column[0] in dataset.columns:
                exists_columns.append(column[0])
        dataset = dataset[exists_columns]

        if self.values['mode3']:
            sql = f"SELECT c.name Cname FROM sys.objects t INNER JOIN sys.objects p " \
                  f" ON t.object_id=p.parent_object_id AND t.type='U' AND p.type='PK'" \
                  f" INNER JOIN sys.syscolumns c ON c.id=t.object_id " \
                  f" INNER JOIN sysindexes i ON i.name=p.name" \
                  f" INNER JOIN sysindexkeys k ON k.id=c.id AND k.colid=c.colid AND k.indid=i.indid" \
                  f" where t.name = '{tablename}'"
            keys = self.ConnDB.exec(self.cur, sql)
            if not keys:
                raise NoPrimaryKeysError('There is no primary key on the table')

            sql = ''
            for index, row in dataset.iterrows():
                where = ' where 1=1'
                for key in keys:
                    key = key[0]
                    where += f' and "{key}" = \'{row[key]}\''
                sql += f'delete from "{tablename}" {where};'
            self.ConnDB.exec(self.cur, sql)

        columns = dataset.columns
        dataset = np.array(dataset)
        # datalist = dataset.tolist()
        datalist = [tuple(i) for i in dataset.tolist()]

        cols = '","'.join(columns)
        l = len(columns)
        v = ''
        for i in range(l):
            v = v + '%s,'
        v = v[:-1]

        sql = 'insert into "%s"(%s) values(' % (tablename, '"' + cols + '"')
        sql = sql + '%s)' % v

        self.ConnDB.exec(self.cur, sql, datalist=datalist)

class NoPrimaryKeysError(Exception):
    # when skip empty table, raise this exception
    pass