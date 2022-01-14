##############################################################
# excel到mysql程序
# 包括获取excel文件，读取excel数据，建表，插入
##############################################################

import PySimpleGUI as sg
import os
import pymysql
import re
from collections import defaultdict
import numpy as np
import pandas as pd
import chardet
from common.handleconfig import HandleConfig
from common.conndb import ConnDB

# excel导入类
class ImportExcel:
    # 初始化配置文件和数据库连接
    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.ConnDB = ConnDB()

    # 主程序
    def main(self, values):
        # 保存界面输入到配置文件作为下次打开时的默认值
        self.HandleConfig.handle_config("s", "file", "file_dir", values['file_dir'])
        self.HandleConfig.handle_config("s", "file", "csv_encoding", values['csv_encoding'])
        self.HandleConfig.handle_config("s", "dbinfo", "host", values['host'])
        self.HandleConfig.handle_config("s", "dbinfo", "port", values['port'])
        self.HandleConfig.handle_config("s", "dbinfo", "user", values['user'])
        self.HandleConfig.handle_config("s", "dbinfo", "passwd", values['passwd'])
        self.HandleConfig.handle_config("s", "dbinfo", "dbname", values['dbname'])
        if values['mode1']:
            self.HandleConfig.handle_config("s", "advanced", "mode", 'mode1')
        else:
            self.HandleConfig.handle_config("s", "advanced", "mode", 'mode2')
        self.HandleConfig.handle_config("s", "advanced", "prefix", values['prefix'])
        self.HandleConfig.handle_config("s", "advanced", "tname", values['tname'])
        self.HandleConfig.handle_config("s", "advanced", "header", values['header'])

        self.HandleConfig.handle_config("s", "advanced", "del_blank_lines", str(values['del_blank_lines']))
        self.HandleConfig.handle_config("s", "advanced", "trim", str(values['trim']))
        self.HandleConfig.handle_config("s", "advanced", "skip_blank_sheet", str(values['skip_blank_sheet']))

        self.file_dir = values['file_dir']
        na_values = values['na_values'].split(',')
        # 获取目录下excel文件
        excelcsvs = self.get_excel(values)
        if not excelcsvs:
            sg.Popup('文件夹下没有可导入的excel文件!')
            return

        # 记录错误日志
        log_file = self.file_dir + "\\exceltoimport_log.txt"
        if os.path.isfile(log_file):
            os.remove(log_file)
        # 连接数据库
        self.db = values['dbname']
        self.conn_db = self.ConnDB.conndb(host=values['host'], port=int(values['port']), user=values['user'],
                                          passwd=values['passwd'], db=self.db, charset='utf8')
        self.sql_mode = self.ConnDB.exec(self.conn_db, 'SELECT @@SESSION.sql_mode').fetchall()[0][0]

        # 表名超长前缀计数
        longexcelcsvs = defaultdict()
        long_num = 0
        # 表个数
        num = 0
        # 导入成功表个数
        num_s = 0

        print("\n\n开始导入...\n")
        for excelcsv, origin_tablename in excelcsvs.items():
            self.excel_name = excelcsv
            try:
                isexcel = 0
                if not values['header']:
                    header = 0
                else:
                    header = int(values['header'])
                # 解析csv格式文件
                if re.fullmatch(r"^.*?\.csv$", excelcsv, flags=re.IGNORECASE):
                    datasets = defaultdict()
                    csv = self.file_dir + "\\" + excelcsv
                    # 如何确定csv文件的编码，请参考下面文章
                    # 因为csv没有记录文件编码，所以我们不能确定其编码格式
                    # 这里采用的策略是优先使用用户提供的编码，再尝试用常见编码格式解码，最后通过探测字节流猜测其编码格式
                    # http://pandaproject.net/docs/determining-the-encoding-of-a-csv-file.html
                    csv_encoding = 'utf8'
                    if values['csv_encoding'] != '自动':
                        csv_encoding = values['csv_encoding']

                    try:
                        dataset = pd.read_csv(csv, encoding=csv_encoding, dtype=str, na_values=na_values,
                                              keep_default_na=False, header=header, engine='c')
                    except UnicodeDecodeError:
                        try:
                            dataset = pd.read_csv(csv, encoding='utf8', dtype=str, na_values=na_values,
                                                  keep_default_na=False, header=header, engine='c')
                        except UnicodeDecodeError:
                            try:
                                dataset = pd.read_csv(csv, encoding='ansi', dtype=str, na_values=na_values,
                                                      keep_default_na=False, header=header, engine='c')
                            except UnicodeDecodeError:
                                try:
                                    dataset = pd.read_csv(csv, encoding='utf-16', dtype=str, na_values=na_values,
                                                          keep_default_na=False, header=header, engine='c')
                                except UnicodeDecodeError:
                                    with open(csv, 'rb') as f:
                                        bytes = f.read()
                                        if len(bytes) > 100000:
                                            with open(csv, 'rb') as f:
                                                bytes = f.readline()
                                    encode = chardet.detect(bytes)['encoding']
                                    if encode == 'ascii':
                                        encode = 'ansi'  # ansi is a super charset of ascii
                                    dataset = pd.read_csv(csv, encoding=encode, dtype=str, na_values=na_values,
                                                          keep_default_na=False, header=header, engine='c')
                    datasets['sheet1'] = dataset

                # 获取excel格式数据（包含每个sheet）
                if re.fullmatch(r"^.*?\.xlsx?$", excelcsv, flags=re.IGNORECASE):
                    isexcel = 1
                    excel = self.file_dir + "\\" + excelcsv
                    datasets = pd.read_excel(excel, dtype=str, na_values=na_values, keep_default_na=False, header=header,
                                             sheet_name=None)

                # 每个sheet为一张表
                for k, v in datasets.items():
                    created_table = None
                    try:
                        sheet_name = k
                        dataset = v
                        tablename = origin_tablename
                        self.excel_name = excelcsv
                        # 同个excel文件有多个sheet，表名采用excel+sheet命名
                        if isexcel == 1 and len(datasets) > 1:
                            tablename = origin_tablename + '_' + re.sub(r"[^\w]+", "_", sheet_name, flags=re.IGNORECASE)
                            self.excel_name = excelcsv + '.' + sheet_name
                        tablename = tablename.lower()
                        # 表名长度超过64需截断，并在表名前加上数字标记
                        if len(tablename.encode("utf8")) > 64:
                            if self.is_Chinese(tablename):
                                tablename = "{0}_".format(long_num) + tablename[:20]
                            else:
                                tablename = "{0}_".format(long_num) + tablename[:60]
                            long_num += 1
                            longexcelcsvs[excelcsv] = tablename
                            with open(log_file, "a") as fw:
                                fw.write("表名超长被截断: {0}, tablename: {1}\n".format(self.excel_name, tablename))

                        # 解析数据
                        if len(dataset.columns) == 0:
                            raise EmptyError("空表")
                        col_maxlen, dataset = self.read_data(dataset, values)
                        # 跳过空表
                        if dataset.empty and values['skip_blank_sheet']:
                            raise EmptyError("空表")

                        # 创建表
                        if values['mode1']:
                            created_table, created_sql = self.create_table(col_maxlen, tablename)
                        try:
                            # 插入数据
                            self.insert_data(dataset, tablename)
                        except pymysql.err.InternalError as reason:
                            if values['mode1']:
                                # 获取mysql错误代码
                                reason_num_0 = str(reason).split(',')[0].strip('(')
                                # utf8mb4
                                if reason_num_0 == '1366':
                                    try:
                                        sql_1 = 'truncate table `{1}`;'.format(tablename)
                                        self.ConnDB.exec(self.conn_db, sql_1)
                                        self.ConnDB.exec(self.conn_db, 'set SESSION sql_mode = ""')
                                        self.insert_data(dataset, tablename)
                                        self.ConnDB.exec(self.conn_db, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

                                    except pymysql.err.InternalError as reason:
                                        reason_num_1 = str(reason).split(',')[0].strip('(')
                                        # 数据行长度超长
                                        if reason_num_1 == '1118':
                                            sql = re.sub('varchar\\(\\d+\\)', 'text', created_sql)
                                            sql_1 = 'drop table if exists `{0}`.`{1}`;'.format(self.db, tablename)
                                            self.ConnDB.exec(self.conn_db, sql_1)
                                            self.ConnDB.exec(self.conn_db, sql)

                                            self.ConnDB.exec(self.conn_db, 'set SESSION sql_mode = ""')
                                            self.insert_data(dataset, tablename)
                                            self.ConnDB.exec(self.conn_db, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

                                        else:
                                            raise pymysql.err.InternalError(str(reason))

                                elif reason_num_0 == '1118':
                                    sql = re.sub('varchar\\(\\d+\\)', 'text', created_sql)
                                    sql_0 = 'drop table if exists `{0}`.`{1}`;'.format(self.db, tablename) + sql
                                    self.ConnDB.exec(self.conn_db, sql_0)
                                    self.insert_data(dataset, tablename)
                                else:
                                    raise pymysql.err.InternalError(str(reason))
                            else:
                                raise pymysql.err.InternalError(str(reason))

                    except Exception as reason:
                        print('失败: {}'.format(self.excel_name))
                        with open(log_file, 'a') as (fw):
                            fw.write('失败的sheet: {0}, error: {1}\n'.format(self.excel_name, str(reason)))
                        if created_table:
                            sql = 'drop table if exists `{1}`'.format(created_table)
                            self.ConnDB.exec(self.conn_db, sql)
                        continue

                    else:
                        print('成功: {}'.format(self.excel_name))
                        num_s += 1
                    finally:
                        num += 1
                        self.ConnDB.exec(self.conn_db, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

            except Exception as reason:
                print("失败: {}".format(excelcsv))
                with open(log_file, "a") as fw:
                    fw.write("文件名: {0}, error: {1}\n".format(self.excel_name, str(reason)))
                num += 1
                continue

        print('\n总数: {}, 导入成功: {}\n'.format(num, num_s))
        self.conn_db.close()
        if os.path.isfile(log_file):
            layout = [
                [sg.Text('导入完成，但是有日志！\n\n总数: {}, 导入成功: {}\n'.format(num, num_s))],
                [sg.OK('完成'), sg.Text(' '*10), sg.Button('查看日志', key='E')]
            ]
        else:
            layout = [
                [sg.Text('导入完成！\n\n总数: {}, 导入成功: {}\n'.format(num, num_s))],
                [sg.OK('完成')]
            ]
        window = sg.Window(layout=layout, title='结果')
        event, values = window.read()
        window.close()
        if event == 'E':
            os.popen(log_file)
        return

    def is_Chinese(self, word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False
    # 获取目录下所有excel文件函数
    def get_excel(self, values):
        excels = os.listdir(self.file_dir)
        excelcsvs = defaultdict()
        for excel in excels:
            excel_dir = self.file_dir + "\\" + excel
            if os.path.isfile(excel_dir) and re.fullmatch(r"^.*?\.(xls|xlsx|csv)$", excel, flags=re.IGNORECASE):
                if values['mode2'] and values['tname']:
                    tablename = values['tname']
                else:
                    tablename = values['prefix'].lower() + re.sub(r"\.(xls|xlsx|csv)$", '', excel.lower(), flags=re.IGNORECASE)
                    # 替换非文字字符为"_"
                    tablename = re.sub(r"[^\w]+", "_", tablename, flags=re.IGNORECASE)

                excelcsvs[excel] = tablename
        return excelcsvs
    # 解析数据函数
    def read_data(self, dataset, values):
        dataset = dataset.fillna(value="")
        if values['trim']:
            f = lambda x: str(x).strip()
            # 去除数据前后空格
            dataset = dataset.applymap(f)
        f = lambda x: len(x)
        # 获取数据长度
        df1 = dataset.applymap(f)
        f = lambda x: max(x)
        # 获取行最大长度
        df3 = df1.apply(f, axis=1)
        df3 = pd.DataFrame(df3, columns=['c'])
        indexs = df3.loc[(df3['c'] == 0)].index
        # 删除空行
        if values['del_blank_lines']:
            dataset.drop(indexs, inplace=True)

        # 处理列名
        dataset.columns = [str(col) for col in dataset.columns]
        self.columns = dataset.columns
        low_col = [col.lower() for col in self.columns]
        # s = len(low_col)
        # 如果列名为空行，用下一行作为列名
        recol = 1
        for col in low_col:
            if 'unnamed: ' not in col:
                recol = 0
                break

        if recol and values['del_blank_lines'] and values['header'] != '0':
            self.columns = dataset[0:1]
            self.columns = np.array(self.columns)
            self.columns = self.columns.tolist()[0]
            dataset.columns = self.columns
            dataset.drop(dataset[:1].index, inplace=True)
            #low_col = [col.lower() for col in self.columns]

        # 将列名的%,\n替换为_
        self.columns = [str(col).strip().replace('%', '_').replace('\n', '_') for col in self.columns]
        # 处理列名为空
        f = lambda x: "unnamed" if x == "" else x
        self.columns = [f(col) for col in self.columns]

        # 如果列名长度超过64，截断
        def f(x):
            if len(x.encode("utf8")) <= 63:
                x = x
            elif self.is_Chinese(x):
                x = x[:20].strip()
            else:
                x = x[:62].strip()
            return x

        self.columns = [f(col) for col in self.columns]

        # 处理重复列名
        while 1:
            low_col = [col.lower() for col in self.columns]
            idx = 0
            # odx = 0
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
        # 计算列最大长度
        df1.columns = self.columns
        df2 = df1.apply(f, axis=0)
        col_maxlen = df2.to_dict()
        # 替换空字符串为null
        f = lambda x: None if x == "" else x
        dataset = dataset.applymap(f)
        return col_maxlen, dataset
    # 创建表函数
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
            self.ConnDB.exec(self.conn_db, sql)
        except:
            sql = re.sub(r"varchar\(\d+\)", "text", sql)
            self.ConnDB.exec(self.conn_db, sql)
        return tablename, sql
    # 插入数据函数
    def insert_data(self, dataset, tablename):
        if dataset.empty:
            return
        dataset = np.array(dataset)
        datalist = dataset.tolist()
        cols = '`,`'.join(self.columns)
        l = len(self.columns)
        v = '%s,' * l
        v = v[:-1]

        sql = 'insert into `%s`(%s) values(' % (tablename, '`' + cols + '`')
        sql = sql + '%s)' % v
        self.ConnDB.exec(self.conn_db, sql, datalist=datalist)

# 空表错误类
class EmptyError(Exception):
    pass


if "__name__" == "__main__":
    ImportExcel = ImportExcel()
    ImportExcel.main()
