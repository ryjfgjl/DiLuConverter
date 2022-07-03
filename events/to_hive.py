##############################################################
# to_hive
# create table, insert data
##############################################################

import numpy as np
import pandas as pd
from common.handleconfig import HandleConfig
from common.conndb import ConnDB

class ToHive:

    def __init__(self, values):
        self.values = values
        self.ConnDB = ConnDB(values)
        self.HandleConfig = HandleConfig()
        self.conn_db = self.ConnDB.conndb(host=values['host'], port=int(values['port']), user=values['user'],
                                          passwd=values['passwd'], db=values['dbname'])

    # create table
    def create_table(self, col_maxlen, tablename):

        sql = "drop table if exists `{0}`;create table `{0}`(".format(tablename)
        for col, maxLen in col_maxlen.items():
            colType = "string"
            sql = sql + "`{0}` {1},".format(col, colType)
        sql = sql[:-1] + ")"

        self.ConnDB.exec(self.conn_db, sql)

        return tablename, sql
    
    # insert into
    def insert_data(self, dataset, tablename, created_sql, dir=None):

        if dataset.empty:
            return
        sql = "show columns in {}".format(tablename)
        columns = self.ConnDB.exec(self.conn_db, sql)
        exists_columns = []
        for column in columns:
            if column[0] in dataset.columns:
                exists_columns.append(column[0])
        #dataset = dataset[exists_columns]

        df = pd.DataFrame(dataset)
        tmptxt = dir+'/'+tablename+'.txt'
        df.to_csv(tmptxt)
        sql = "load data inpath 'file:///{0}' into table {1}".format(tmptxt,tablename)
        self.ConnDB.exec(self.conn_db, sql)





