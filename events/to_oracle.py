##############################################################
# to_oracle
# create table, insert data
##############################################################

import numpy as np
from common.handleconfig import HandleConfig
from common.conndb import ConnDB


class ToOracle:

    def __init__(self, values):
        self.values = values
        self.ConnDB = ConnDB(values)
        self.HandleConfig = HandleConfig()
        self.conn_db = self.ConnDB.conndb(host=values['host'], port=int(values['port']), user=values['user'],
                                          passwd=values['passwd'], db=values['dbname'], charset='utf8')

    # create table
    def create_table(self, col_maxlen, tablename):
        sql = "select 1 from all_tables where owner = '{}' and table_name = '{}'".format(self.values['user'].upper(),
                                                                                         tablename)
        cnt = self.ConnDB.exec(self.conn_db, sql)
        if len(cnt) > 0:
            sql = 'drop table "{}"'.format(tablename)
            self.ConnDB.exec(self.conn_db, sql)
        sql = "create table \"{0}\"(".format(tablename)
        for col, maxLen in col_maxlen.items():
            colType = "varchar(255)"
            if type(maxLen) == int:
                if maxLen * 6 > 4000:
                    colType = "CLOB"
                elif maxLen > 0:
                    colType = "varchar({})".format(maxLen * 6)

            sql = sql + "\"{0}\" {1} default null,".format(col, colType)
        if self.values['add_tname']:
            sql = sql + "`table_name` varchar(255) default '{0}',".format(tablename)
        sql = sql[:-1] + ")"

        self.ConnDB.exec(self.conn_db, sql)
        return tablename, sql

    # insert into
    def insert_data(self, dataset, tablename, created_sql=None, dir=None):
        if dataset.empty:
            return
        sql = "select column_name from ALL_TAB_COLUMNS " \
              "where OWNER = '{0}' and table_name = '{1}'".format(self.values['user'].upper(), tablename)
        columns = self.ConnDB.exec(self.conn_db, sql)
        exists_columns = []
        for column in columns:
            if column[0] in dataset.columns:
                exists_columns.append(column[0])
        dataset = dataset[exists_columns]
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

        self.ConnDB.exec(self.conn_db, sql, datalist=datalist)