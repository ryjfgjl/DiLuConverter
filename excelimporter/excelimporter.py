print("Ready to import...")

import easygui
import os, sys
import pymysql
import re
from collections import defaultdict
import numpy as np
import pandas as pd
import chardet
from common.commonscripts import CommonScripts

class ImportExcel:

    def __init__(self):
        self.realpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
        # get configuration from 'config.ini'
        self.CommonScripts = CommonScripts()
        self.img = self.realpath + "\\" + self.CommonScripts.handle_config("g", "referencefile", "img")
        self.cleansql = self.realpath + "\\" + self.CommonScripts.handle_config("g", "referencefile", "cleanexcel")
        self.default_dir = self.CommonScripts.handle_config("g", "global", "default_excels_dictionary")
        self.use_server = self.CommonScripts.handle_config("g", "global", "use_server")

    def main(self):
        # enter a database you will import excel to
        self.db = easygui.enterbox(msg="Enter your database name:")
        if not self.db:
            return
        self.db = self.db.lower().strip()

        # choose excel file dictionary
        self.importexcelpath = easygui.diropenbox(msg="Choose your excels dictionary:", default=self.default_dir)
        if not self.importexcelpath:
            return

        excelcsvs = self.get_excel()
        if not excelcsvs:
            easygui.msgbox("No excels can import!")
            return

        # anything failed excel to import will be wrote in it
        log_file = self.importexcelpath + "\\log.txt"
        if os.path.isfile(log_file):
            os.remove(log_file)


        # create database
        try:
            sql = "create database `{0}`;".format(self.db)
            self.CommonScripts.exec(self.use_server, sql)
        except pymysql.err.ProgrammingError:
            conti = easygui.ynbox(msg="Database {0} exists, drop it first?".format(self.db))
            if conti:
                print("Dropping database...")
                sql = "drop database if exists `{0}`;create database `{0}`".format(self.db, self.db)
                self.CommonScripts.exec(self.use_server, sql, kill=True, COMMAND=True)
        print("Created database {}".format(self.db))

        longexcelcsvs = defaultdict()
        long_num = 0
        num = 0
        num_s = 0

        print("Begin to import...\n")
        for excelcsv, origin_tablename in excelcsvs.items():
            self.excel_name = excelcsv
            try:
                isexcel = 0
                # get csv dataset
                if re.fullmatch(r"^.*?\.csv$", excelcsv, flags=re.IGNORECASE):
                    datasets = defaultdict()
                    csv = self.importexcelpath + "\\" + excelcsv
                    with open(csv, 'rb') as f:
                        bytes = f.read()
                        if len(bytes) > 100000:
                            with open(csv, 'rb') as f:
                                bytes = f.readline()
                    encode = chardet.detect(bytes)['encoding']
                    if encode == 'ascii':
                        encode = 'ansi'  # ansi is a super charset of ascii
                     
                    dataset = pd.read_csv(csv, encoding=encode, dtype=str, na_filter=False, header=0, engine="c")
                    datasets['sheet1'] = dataset
                # get excel dataset(include sheets)
                if re.fullmatch(r"^.*?\.xlsx?$", excelcsv, flags=re.IGNORECASE):
                    isexcel = 1
                    excel = self.importexcelpath + "\\" + excelcsv
                    datasets = pd.read_excel(excel, dtype=str, na_filter=False, header=0, sheet_name=None)

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
                            tablename = origin_tablename + '_' + re.sub(r"[^\w]+", "_", sheet_name,
                                                                        flags=re.IGNORECASE)
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
                                fw.write("extra long excel: {0}, tablename: {1}\n".format(self.excel_name, tablename))

                        col_maxlen, dataset = self.read_data(dataset)

                        if dataset.empty:
                            raise EmptyError("Empty")
                        created_table, created_sql = self.create_table(col_maxlen, tablename)

                        try:
                            self.insert_data(dataset, tablename)
                        except pymysql.err.InternalError as reason:
                            reason_num_0 = str(reason).split(",")[0].strip("(")
                            if reason_num_0 == "1366":
                                try:
                                    sql_0 = "alter table `{1}`.{2} convert to character set utf8mb4 collate utf8mb4_bin".format(self.db, self.db, created_table)
                                    self.CommonScripts.exec(self.use_server, sql_0,self.db, kill=True,COMMAND=True)
                                    self.insert_data(dataset, tablename, charset="utf8mb4")
                                except pymysql.err.InternalError as reason:
                                    reason_num_1 = str(reason).split(",")[0].strip("(")
                                    if reason_num_1 == "1118":
                                        sql = re.sub(r"varchar\(\d+\)", "text", created_sql)
                                        sql_1 = "drop table if exists `{0}`.`{1}`;".format(self.db, tablename)
                                        self.CommonScripts.exec(self.use_server, sql_1,self.db, kill=True,COMMAND=True)
                                        self.CommonScripts.exec(self.use_server, sql,self.db, kill=True,COMMAND=True)
                                        
                                        sql_0 = "alter table `{1}`.{2} convert to character set utf8mb4 collate utf8mb4_bin".format(self.db, self.db, created_table)
                                        self.CommonScripts.exec(self.use_server, sql_0,self.db, kill=True,COMMAND=True)
                                        self.insert_data(dataset, tablename, charset="utf8mb4")
                                    else:
                                        raise pymysql.err.InternalError(str(reason))
                            elif reason_num_0 == "1118":
                                sql = re.sub(r"varchar\(\d+\)", "text", created_sql)
                                sql_0 = "drop table if exists `{0}`.`{1}`;".format(self.db, tablename) + sql
                                self.CommonScripts.exec(self.use_server, sql_0, self.db, kill=True, COMMAND=True)
                                self.insert_data(dataset, tablename)

                            else:
                                raise pymysql.err.InternalError(str(reason))


                    except Exception as reason:
                        print("Failed: {}".format(self.excel_name))

                        with open(log_file, "a", encoding="utf8") as fw:
                            fw.write("excel sheet name: {0}, error: {1}\n".format(self.excel_name, str(reason)))

                        if not created_table:
                            sql = "drop table if exists `{0}`.`{1}`".format(self.db, created_table)
                            self.CommonScripts.exec(self.use_server, sql, self.db, kill=True, COMMAND=True)

                        continue

                    else:
                        print("Imported: {}".format(self.excel_name))
                        num_s += 1

                    finally:
                        num += 1

            except Exception as reason:
                print("Failed: {}".format(excelcsv))
                with open(log_file, "a", encoding="utf8") as fw:
                    fw.write("excel file name: {0}, error: {1}\n".format(self.excel_name, str(reason)))
                num += 1
                continue

        print("\nTotal: {}, Imported: {}\n".format(num, num_s))
        conti = 1
        if os.path.isfile(log_file):
            os.popen(log_file)
            easygui.msgbox("You have logs , see file '{}' \n\ncheck it first".format(log_file))
            if num_s == 0:
                easygui.msgbox("No imported tables!")
                return

            conti = easygui.ccbox(msg="Clean database {} now?".format(self.db))
        if conti:
            self.clean_data()
    
    def is_Chinese(self,word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
    
    def get_excel(self):
        # a function to get excel/csv file under the dictionary
        excels = os.listdir(self.importexcelpath)
        excelcsvs = defaultdict()

        for excel in excels:
            excel_dir = self.importexcelpath + "\\" + excel
            if os.path.isfile(excel_dir) and re.fullmatch(r"^.*?\.(xls|xlsx|csv)$", excel, flags=re.IGNORECASE):
                tablename = re.sub(r"\.(xls|xlsx|csv)$", '', excel.lower(), flags=re.IGNORECASE)
                # replace all character not \w to "_"
                tablename = re.sub(r"[^\w]+", "_", tablename,flags=re.IGNORECASE)
                excelcsvs[excel] = tablename
        return excelcsvs

    def read_data(self, dataset):
        # str col
        dataset.columns = [str(col) for col in dataset.columns]
        self.columns = dataset.columns
        self.columns = [str(col).strip() for col in self.columns]

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
        while True:
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

        # deal with data
        f = lambda x: str(x).strip()
        dataset = dataset.applymap(f)
        f = lambda x: len(x.encode("utf8"))
        df1 = dataset.applymap(f)
        f = lambda x: max(x)
        df2 = df1.apply(f, axis=0)
        col_maxlen = df2.to_dict()

        f = lambda x: None if x == "" else x
        dataset = dataset.applymap(f)

        return col_maxlen, dataset

    def create_table(self, col_maxlen, tablename):
        sql = "create table `{0}`.`{1}`(".format(self.db, tablename)
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
            self.CommonScripts.exec(self.use_server, sql)

        except pymysql.InternalError:
            sql = re.sub(r"varchar\(\d+\)", "text", sql)
            self.CommonScripts.exec(self.use_server, sql)
        return tablename, sql
    
    def insert_data(self, dataset, tablename, charset="utf8"):
        # insert
        dataset = np.array(dataset)  # dataframe to ndarray
        datalist = dataset.tolist()  # ndarray to list
        # self.columns = [col.strip() for col in self.columns]
        cols = "`,`".join(self.columns)
        l = len(self.columns)
        v = "%s," * l
        v = v[:-1]
        sql = "insert into `%s`.`%s`(%s) values(" % (self.db, tablename, "`" + cols + "`")
        # sql = "insert into `" + self.db + "`.`" + tablename + "`(" + cols + "`)"
        sql = sql + "%s)" % v

        host = self.CommonScripts.handle_config('g', self.use_server, 'host')
        user = self.CommonScripts.handle_config('g', self.use_server, 'user')
        passwd = self.CommonScripts.handle_config('g', self.use_server, 'password')
        port = int(self.CommonScripts.handle_config('g', self.use_server, 'port'))
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, charset=charset)
        cur = conn.cursor()
        cur.executemany(sql, datalist)
        conn.commit()
        cur.close()
        conn.close()


    def clean_data(self):
        print('Begin to clean data...\n')
        file = self.cleansql
        ret = self.CommonScripts.cmd(self.use_server, self.db, "mysql", file)
        if ret == 0:
            easygui.msgbox(msg="Import Over", image=self.img)
        else:
            easygui.exceptionbox("Clean Data Failed")

class EmptyError(Exception):
    pass

if "__name__" == "__main__":
    ImportExcel = ImportExcel()
    ImportExcel.main()


