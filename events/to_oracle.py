##############################################################
# to_oracle
# create table, insert data
##############################################################

import numpy as np


class ToOracle:

    def __init__(self, values, ConnDB, dbconn, cur):
        self.values = values
        self.ConnDB = ConnDB
        self.dbconn = dbconn
        self.cur = cur

    # create table
    def create_table(self, col_maxlen, tablename):
        sql = "select 1 from all_tables where owner = '{}' and table_name = '{}'".format(self.values['user'].upper(),
                                                                                         tablename)
        cnt = self.ConnDB.exec(self.cur, sql)
        if len(cnt) > 0:
            sql = 'drop table "{}"'.format(tablename)
            self.ConnDB.exec(self.cur, sql)
        sql = "create table \"{0}\"(".format(tablename)
        for col, maxLen in col_maxlen.items():
            colType = "varchar(255)"
            if type(maxLen) == int:
                if maxLen * 6 > 4000:
                    colType = "CLOB"
                elif maxLen > 0:
                    colType = "varchar({})".format(maxLen * 6)

            sql = sql + "\"{0}\" {1} default null,".format(col, colType)

        sql = sql[:-1] + ")"
        self.ConnDB.exec(self.cur, sql)

        return tablename, sql

    # insert into
    def insert_data(self, dataset, tablename, created_sql=None, dir=None):
        if dataset.empty:
            return
        sql = "select column_name from ALL_TAB_COLUMNS " \
              "where OWNER = '{0}' and table_name = '{1}'".format(self.values['user'].upper(), tablename)
        columns = self.ConnDB.exec(self.cur, sql)
        exists_columns = []
        for column in columns:
            if column[0] in dataset.columns:
                exists_columns.append(column[0])
        dataset = dataset[exists_columns]

        if self.values['mode3']:
            sql = f"select cu.column_name from user_cons_columns cu, user_constraints au " \
                  f"where cu.constraint_name = au.constraint_name " \
                  "and au.constraint_type = 'P' and au.table_name = '{table_name}'"
            keys = self.ConnDB.exec(self.cur, sql)
            if not keys:
                raise NoPrimaryKeysError('There is no primary key on the table')

            sql = ''
            for index, row in dataset.iterrows():
                where = ' where 1=1'
                for key in keys:
                    key = key[0]
                    where += f' and "{key}" = "{row[key]}"'
                sql += f'delete from "{tablename}" {where};'
            self.ConnDB.exec(self.cur, sql)


        columns = dataset.columns
        dataset = np.array(dataset)
        datalist = dataset.tolist()

        cols = '","'.join(columns)
        l = len(columns)
        v = ''
        for i in range(l):
            v = v + ':{},'.format(i + 1)
        v = v[:-1]

        sql = 'insert into "%s"(%s) values(' % (tablename, '"' + cols + '"')
        sql = sql + '%s)' % v

        self.ConnDB.exec(self.cur, sql, datalist=datalist)

class NoPrimaryKeysError(Exception):
    # when skip empty table, raise this exception
    pass