
import PySimpleGUI as sg
import os, sys
import pymysql
import re
from collections import defaultdict
import numpy as np
import pandas as pd
import chardet
from common.handleconfig import HandleConfig
from common.conndb import ConnDB

class ImportExcel:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    def main(self,values):
        # save the recent input
        self.HandleConfig.handle_config("s", "file", "file_dir", values['file_dir'])
        self.HandleConfig.handle_config("s", "file", "csv_encoding", values['csv_encoding'])
        self.HandleConfig.handle_config("s", "dbinfo", "host", values['host'])
        self.HandleConfig.handle_config("s", "dbinfo", "port", values['port'])
        self.HandleConfig.handle_config("s", "dbinfo", "user", values['user'])
        self.HandleConfig.handle_config("s", "dbinfo", "passwd", values['passwd'])
        self.HandleConfig.handle_config("s", "dbinfo", "dbname", values['dbname'])
        self.HandleConfig.handle_config("s", "file", "na_values", values['na_values'])

        self.db = values['dbname']
        self.conn = self.ConnDB.conndb(host=values['host'], port=int(values['port']), user=values['user'], passwd=values['passwd'], charset='utf8')
        self.file_dir = values['file_dir']
        na_values = values['na_values'].split(',')

        excelcsvs = self.get_excel()
        if not excelcsvs:
            sg.Popup('No Excel/CSV files!')
            return

        # write log
        log_file = self.file_dir + "\\log.txt"
        if os.path.isfile(log_file):
            os.remove(log_file)

        # create database
        if values['redb']:
            print("Bengin to Re-Create Database")
            sql = "drop database if exists `{0}`;create database `{0}`".format(self.db, self.db)
            self.ConnDB.exec(self.conn,sql)
            print('\n\n{}'.format(sql))
        self.conn_db = self.ConnDB.conndb(host=values['host'], port=int(values['port']), user=values['user'], passwd=values['passwd'], db=self.db, charset='utf8')
        self.sql_mode = self.ConnDB.exec(self.conn_db, 'SELECT @@SESSION.sql_mode').fetchall()[0][0]

        longexcelcsvs = defaultdict()
        long_num = 0
        num = 0
        num_s = 0

        print("\n\nBegin to import...\n")
        for excelcsv, origin_tablename in excelcsvs.items():
            self.excel_name = excelcsv
            try:
                isexcel = 0
                # get csv dataset
                if re.fullmatch(r"^.*?\.csv$", excelcsv, flags=re.IGNORECASE):
                    datasets = defaultdict()
                    csv = self.file_dir + "\\" + excelcsv
                    # Determining the encoding of a CSV file
                    # http://pandaproject.net/docs/determining-the-encoding-of-a-csv-file.html
                    if values['csv_encoding']:
                        csv_encoding = values['csv_encoding']
                    csv_encoding = 'utf8'
                    try:
                        dataset = pd.read_csv(csv, encoding=csv_encoding, dtype=str, na_values=na_values, keep_default_na=False, header=0, engine='c')
                    except UnicodeDecodeError:
                        try:
                            dataset = pd.read_csv(csv, encoding='ansi', dtype=str, na_values=na_values, keep_default_na=False, header=0, engine='c')
                        except UnicodeDecodeError:
                            try:
                                dataset = pd.read_csv(csv, encoding='utf-16', dtype=str, na_values=na_values, keep_default_na=False, header=0, engine='c')
                            except UnicodeDecodeError:
                                with open(csv, 'rb') as f:
                                    bytes = f.read()
                                    if len(bytes) > 100000:
                                        with open(csv, 'rb') as f:
                                            bytes = f.readline()
                                encode = chardet.detect(bytes)['encoding']
                                if encode == 'ascii':
                                    encode = 'ansi' #ansi is a super charset of ascii
                                dataset = pd.read_csv(csv, encoding=encode, dtype=str, na_values=na_values, keep_default_na=False, header=0, engine='c')
                    datasets['sheet1'] = dataset

                # get excel dataset(include sheets)
                if re.fullmatch(r"^.*?\.xlsx?$", excelcsv, flags=re.IGNORECASE):
                    isexcel = 1
                    excel = self.file_dir + "\\" + excelcsv
                    datasets = pd.read_excel(excel, dtype=str, na_values=na_values, keep_default_na=False, header=0, sheet_name=None)

                # one sheet/csv is one table
                for k, v in datasets.items():
                    created_table = None
                    try:
                        sheet_name = k
                        dataset = v
                        tablename = origin_tablename
                        self.excel_name = excelcsv
                        # rename table name if excel have more than one sheets
                        if isexcel == 1 and len(datasets) > 1:
                            tablename = origin_tablename + '_' + re.sub(r"[^\w]+", "_", sheet_name,flags=re.IGNORECASE)
                            self.excel_name = excelcsv + '.' + sheet_name
                        tablename = tablename.lower()
                        # cut off table name
                        if len(tablename.encode("utf8")) > 64:
                            if self.is_Chinese(tablename):
                                tablename = "{0}_".format(long_num) + tablename[:20]
                            else:
                                tablename = "{0}_".format(long_num) + tablename[:60]
                            long_num += 1
                            longexcelcsvs[excelcsv] = tablename
                            with open(log_file, "a", encoding="utf8") as fw:
                                fw.write("table name cut off: {0}, tablename: {1}\n".format(self.excel_name, tablename))

                        col_maxlen, dataset = self.read_data(dataset)

                        if dataset.empty:
                            raise EmptyError("Empty")
                            
                        created_table, created_sql = self.create_table(col_maxlen, tablename)

                        try:
                            self.insert_data(dataset, tablename)

                        except pymysql.err.InternalError as reason:

                            reason_num_0 = str(reason).split(',')[0].strip('(')

                            if reason_num_0 == '1366':
                                try:
                                    sql_1 = 'truncate table `{0}`.`{1}`;'.format(self.db, tablename)
                                    self.ConnDB.exec(self.conn, sql_1)
                                    self.ConnDB.exec(self.conn, 'set SESSION sql_mode = ""')
                                    self.insert_data(dataset, tablename)
                                    self.ConnDB.exec(self.conn, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))


                                except pymysql.err.InternalError as reason:
                                    reason_num_1 = str(reason).split(',')[0].strip('(')
                                    if reason_num_1 == '1118':
                                        sql = re.sub('varchar\\(\\d+\\)', 'text', created_sql)
                                        sql_1 = 'drop table if exists `{0}`.`{1}`;'.format(self.db, tablename)
                                        self.ConnDB.exec(self.conn, sql_1)
                                        self.ConnDB.exec(self.conn, sql)

                                        self.ConnDB.exec(self.conn, 'set SESSION sql_mode = ""')
                                        self.insert_data(dataset, tablename)
                                        self.ConnDB.exec(self.conn, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

                                    else:
                                        raise pymysql.err.InternalError(str(reason))

                            elif reason_num_0 == '1118':
                                    sql = re.sub('varchar\\(\\d+\\)', 'text', created_sql)
                                    sql_0 = 'drop table if exists `{0}`.`{1}`;'.format(self.db, tablename) + sql
                                    self.ConnDB.exec(self.conn, sql_0)
                                    self.insert_data(dataset, tablename)
                            else:
                                raise pymysql.err.InternalError(str(reason))


                    except Exception as reason:
                        print('Failed: {}'.format(self.excel_name))
                        with open(log_file, 'a') as (fw):
                            fw.write('sheet name: {0}, error: {1}\n'.format(self.excel_name, str(reason)))
                        if created_table:
                            sql = 'drop table if exists `{0}`.`{1}`'.format(self.db, created_table)
                            self.ConnDB.exec(self.conn, sql)
                        continue

                    else:
                        print('Imported: {}'.format(self.excel_name))
                        num_s += 1
                    finally:
                        num += 1
                        self.ConnDB.exec(self.conn, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

            except Exception as reason:
                print("Failed: {}".format(excelcsv))
                with open(log_file, "a") as fw:
                    fw.write("file name: {0}, error: {1}\n".format(self.excel_name, str(reason)))
                num += 1
                continue

        print('\nTotal: {}, Imported: {}\n'.format(num, num_s))
        self.conn.close()
        self.conn_db.close()

        if os.path.isfile(log_file):
            os.popen(log_file)
            sg.Popup("You have logs , see file '{}' \n\ncheck it first".format(log_file))
            if num_s == 0:
                sg.Popup("No imported tables!")
                return
        sg.Popup("Done!")
    
    def is_Chinese(self,word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
    
    def get_excel(self):
        # a function to get excel/csv files under the dictionary
        excels = os.listdir(self.file_dir)
        excelcsvs = defaultdict()
        for excel in excels:
            excel_dir = self.file_dir + "\\" + excel
            if os.path.isfile(excel_dir) and re.fullmatch(r"^.*?\.(xls|xlsx|csv)$", excel, flags=re.IGNORECASE):
                tablename = re.sub(r"\.(xls|xlsx|csv)$", '', excel.lower(), flags=re.IGNORECASE)
                # replace all character not \w to "_"
                tablename = re.sub(r"[^\w]+", "_", tablename,flags=re.IGNORECASE)
                excelcsvs[excel] = tablename
        return excelcsvs

    def read_data(self, dataset):
        dataset = dataset.fillna(value="")
        f = lambda x: str(x).strip()
        dataset = dataset.applymap(f)
        f = lambda x: len(x)
        df1 = dataset.applymap(f)
        f = lambda x: max(x)
        df3 = df1.apply(f, axis=1)
        df3 = pd.DataFrame(df3, columns=['c'])
        indexs = df3.loc[(df3['c'] == 0)].index
        dataset.drop(indexs, inplace=True)

        # deal with columns
        dataset.columns = [str(col) for col in dataset.columns]
        self.columns = dataset.columns
        low_col = [col.lower() for col in self.columns]
        s = len(low_col)
        recol = 1
        for col in low_col:
        	if 'unnamed: ' not in col:
        		recol = 0
        		break
	
        if recol:
            self.columns = dataset[0:1]
            self.columns = np.array(self.columns)
            self.columns = self.columns.tolist()[0]
            dataset.columns = self.columns
            dataset.drop(dataset[:1].index, inplace=True)
            low_col = [col.lower() for col in self.columns]

        self.columns = [str(col).strip() for col in self.columns]
        # fix blank col name
        f = lambda x: "unnamed" if x == "" else x
        self.columns = [f(col) for col in self.columns]
        
        # cut off col
        def f(x):
            if len(x.encode("utf8")) <= 63:
               x = x
            elif self.is_Chinese(x): 
               x = x[:20].strip()
            else:
               x = x[:62].strip() 
            return x
        self.columns = [f(col) for col in self.columns]
        
        # fix duplicate column name
        while 1:
            low_col = [col.lower() for col in self.columns]
            idx = 0
            odx = 0
            c = 0
            for i in self.columns:
                jdx = 0
                n = 1
                if idx == len(self.columns):
                    continue
                for j in low_col[idx + 1:]:
                    odx = idx + 1 + jdx
                    if j == i.lower():
                        self.columns[odx] = j + str(n)
                        n += 1
                        c += 1
                    jdx += 1

                idx += 1

            if c == 0:
                break

        dataset.columns = self.columns
        self.columns = np.array(self.columns)
        self.columns = self.columns.tolist()
        f = lambda x: max(x)
        df1.columns = self.columns
        df2 = df1.apply(f, axis=0)
        col_maxlen = df2.to_dict()
        f = lambda x: None if x == "" else x
        dataset = dataset.applymap(f)

        return col_maxlen, dataset


    def create_table(self, col_maxlen, tablename):
        sql = "create table {0}(".format(tablename)
        for col, maxLen in col_maxlen.items():
            colType = "varchar(255)"
            if maxLen > 255:
                colType = "TEXT"
            if maxLen > 65535:
                colType = "MEDIUMTEXT"
            if maxLen > 16777215:
                colType = "LONGTEXT"

            sql = sql + "`{0}` {1} default null,".format(col, colType)

        sql = sql[:-1] + ")"

        try:
            self.ConnDB.exec(self.conn_db,sql)
        except:
            sql = re.sub(r"varchar\(\d+\)", "text", sql)
            self.ConnDB.exec(self.conn_db,sql)

        return tablename, sql
    
    def insert_data(self, dataset, tablename):
        dataset = np.array(dataset)
        datalist = dataset.tolist()
        cols = '`,`'.join(self.columns)
        l = len(self.columns)
        v = '%s,' * l
        v = v[:-1]

        sql = 'insert into `%s`.`%s`(%s) values(' % (self.db, tablename, '`' + cols + '`')
        sql = sql + '%s)' % v
        self.ConnDB.exec(self.conn, sql, datalist=datalist)


class EmptyError(Exception):
    pass

if "__name__" == "__main__":
    ImportExcel = ImportExcel()
    ImportExcel.main()


