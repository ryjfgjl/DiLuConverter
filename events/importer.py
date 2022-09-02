##############################################################
# Importer
# From Excel, To MySQL/Oracle/SQL Server/Hive
##############################################################


import os
import re
import pypinyin as pn
from events.from_excels import FromExcels
from common.conndb import ConnDB
from events.to_mysql import ToMySQL
from events.to_oracle import ToOracle
from events.to_sqlserver import ToSqlserver
from events.to_hive import ToHive


class Importer:

    def __init__(self):
        self.values = {}
        self.window = None
        self.FromExcels = FromExcels()
        self.ConnDB = ConnDB()

    def main(self):
        try:
            if self.window:
                self.window['start'].update(disabled=True)
                self.window['start'].update('运    行    中')
            self.FromExcels.values = self.values
            self.ConnDB.values = self.values
            dbconn = self.ConnDB.conndb()
            cur = dbconn.cursor()
            if self.values['dbtype'] == 'MySQL':
                ToDB = ToMySQL(self.values, self.ConnDB, dbconn, cur)
            elif self.values['dbtype'] == 'Oracle':
                ToDB = ToOracle(self.values, self.ConnDB, dbconn, cur)
            elif self.values['dbtype'] == 'SQL Server':
                ToDB = ToSqlserver(self.values, self.ConnDB, dbconn, cur)
            elif self.values['dbtype'] == 'Hive':
                ToDB = ToHive(self.values, self.ConnDB, dbconn, cur)



            # get all excel files
            excels_dict = self.FromExcels.get_excels()

            if not excels_dict:
                if self.window:
                    # self.print('No Excels!', text_color='red')
                    self.window['start'].update(disabled=False)
                    self.window['start'].update('开     始')
                else:
                    self.print('No Excels')

                return 'No Excels!'

            # record error log

            if self.values['source'] == 'D':
                log_file = self.values['file_dir'] + "/importlog.txt"
            elif self.values['source'] == 'F':
                log_file = os.path.dirname(self.values['files'].split(';')[0]) + "/importlog.txt"

            if os.path.isfile(log_file):
                os.remove(log_file)

            # count of tables
            num = 0
            # count of succeed tables
            num_s = 0
            num_suffix = 1
            imported_tables = []

            self.print("\nBegin Import...\n")

            # run sql_b4
            if self.values['sql_b4']:
                with open(self.values['sql_b4'], 'r') as fr:
                    sql = fr.read()
                self.print("Running SQL in {}...\n".format(self.values['sql_b4']))
                self.ConnDB.exec(cur, sql)

            # loop all excel files
            for excel, tname in excels_dict.items():

                try:
                    datasets = self.FromExcels.get_data(excel)
                    excel_name = excel

                    # loop all sheets in one excel
                    for k, v in datasets.items():
                        created_table = None
                        try:
                            sheet_name = k
                            dataset = v
                            tablename = tname
                            if self.values['mode2'] and self.values['tname']:
                                if len(datasets) > 1:
                                    excel = excel_name + '.' + sheet_name
                            else:
                                # concat excel name and sheet name
                                if len(datasets) > 1:
                                    tablename = tablename + '_' + re.sub(r"[^\w]+", "_", sheet_name,
                                                                         flags=re.IGNORECASE)
                                    excel = excel_name + '.' + sheet_name
                                tablename = tablename.lower()
                                if self.values['trf_cn']:
                                    tablename = ''.join(
                                        [i[0] for i in pn.pinyin(tablename, style=pn.Style.FIRST_LETTER)])
                                # cut off table name
                                if len(tablename) > 62:
                                    tablename = tablename[:61]
                                    if tablename in imported_tables:
                                        tablename = tablename + '_{}'.format(num_suffix)
                                        num_suffix += 1
                                        self.print('Warnning: ', text_color='yellow', end='')
                                        self.print('{0}'.format(excel))
                                        with open(log_file, "a") as fw:
                                            fw.write("table name added suffix: {0}, tablename: {1}\n".format(excel,
                                                                                                             tablename))
                                    with open(log_file, "a") as fw:
                                        fw.write("table name cut off: {0}, tablename: {1}\n".format(excel, tablename))
                                    self.print('Warnning: ', text_color='yellow', end='')
                                    self.print('{0}'.format(excel))
                                else:
                                    if tablename in imported_tables:
                                        tablename = tablename + '_{}'.format(num_suffix)
                                        num_suffix += 1
                                        self.print('Warnning: ', text_color='yellow', end='')
                                        self.print('{0}'.format(excel))
                                        with open(log_file, "a") as fw:
                                            fw.write("table name added suffix: {0}, tablename: {1}\n".format(excel,
                                                                                                             tablename))
                            if len(dataset.columns) == 0 or (dataset.empty and self.values['skip_blank_sheet']):
                                raise EmptyError("Empty Table")

                            col_maxlen, dataset = self.FromExcels.parse_data(dataset)

                            # create table
                            created_sql = None

                            if self.values['mode1']:
                                created_table, created_sql = ToDB.create_table(col_maxlen, tablename)

                            ToDB.insert_data(dataset, tablename, created_sql, os.path.dirname(log_file))
                            if self.values['mode1']:
                                imported_tables.append(tablename)

                        except Exception as reason:
                            self.print('Failed: ', text_color='red', end='')
                            self.print('{0}'.format(excel))
                            if created_table:
                                if self.values['dbtype'] == 'MySQL' or self.values['dbtype'] == 'Hive':
                                    sql = 'drop table if exists `{0}`'.format(created_table)
                                else:
                                    sql = 'drop table "{0}"'.format(created_table)
                                self.ConnDB.exec(cur, sql)
                            with open(log_file, 'a') as (fw):
                                fw.write('Failed Sheet: {0}, error: {1}\n'.format(excel, str(reason)))
                            continue

                        else:
                            self.print('Succeed: {}'.format(excel))
                            num_s += 1
                        finally:
                            num += 1
                            if self.values['dbtype'] == 'MySQL':
                                self.sql_mode = ToDB.sql_mode
                                self.ConnDB.exec(cur, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

                except Exception as reason:
                    self.print('Failed: ', text_color='red', end='')
                    self.print('{0}'.format(excel))
                    with open(log_file, "a") as fw:
                        fw.write("Failed Excel: {0}, error: {1}\n".format(excel, str(reason)))
                    num += 1
                    continue
                finally:
                    dbconn.commit()

            self.print('\nTotal: {}, Succeed: {}\n'.format(num, num_s))

            # run sql_after
            if self.values['sql_after']:
                with open(self.values['sql_after'], 'r') as fr:
                    sql = fr.read()
                self.print("Running SQL in {}...\n".format(self.values['sql_after']))
                self.ConnDB.exec(cur, sql)
            dbconn.commit()
            cur.close()
            dbconn.close()
            if self.window:
                self.window['start'].update(disabled=False)
                self.window['start'].update('开     始')
            return [log_file, num, num_s, self.window]
        except Exception as reason:
            if self.window:
                self.window['start'].update(disabled=False)
                self.window['start'].update('开     始')
            try:
                dbconn.commit()
                cur.close()
                dbconn.close()
            except:
                pass
            return str(reason)

    def print(self, value, text_color=None, end='\n'):
        if self.window:
            return self.window['output'].print(value, text_color=text_color, end=end)
        else:
            return print(value, end=end)


class EmptyError(Exception):
    # when skip empty table, raise this exception
    pass
