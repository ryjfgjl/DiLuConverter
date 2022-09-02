##############################################################
# to_hive
# create table, insert data
##############################################################

import pandas as pd

class ToHive:

    def __init__(self, values, ConnDB, dbconn, cur):
        self.values = values
        self.ConnDB = ConnDB
        self.dbconn = dbconn
        self.cur = cur

    # create table
    def create_table(self, col_maxlen, tablename):

        sql = "drop table if exists `{0}`;create table `{0}`(".format(tablename)
        for col, maxLen in col_maxlen.items():
            colType = "string"
            sql = sql + "`{0}` {1},".format(col, colType)
        sql = sql[:-1] + ") row format delimited fields terminated by ','"

        self.ConnDB.exec(self.cur, sql)

        return tablename, sql

    # insert into
    def insert_data(self, dataset, tablename, created_sql, dir=None):

        if dataset.empty:
            return

        df = pd.DataFrame(dataset)
        tmptxt = dir+'/'+tablename+'.txt'
        df.to_csv(tmptxt, index=False, header=None)
        sql = "load data inpath 'file:///{0}' into table {1}".format(tmptxt, tablename)
        self.ConnDB.exec(self.cur, sql)





