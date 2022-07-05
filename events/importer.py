##############################################################
# Importer
# From Excel, To MySQL/Oracle/SQL Server/Hive
##############################################################

import PySimpleGUI as sg
import pypinyin as pn
import os
import re
from events.from_excels import FromExcels
from events.to_mysql import ToMySQL
from events.to_oracle import ToOracle
from events.to_sqlserver import ToSqlserver
from events.to_hive import ToHive


class Importer:

    def __init__(self, values):
        self.values = values
        self.FromExcels = FromExcels(values)

        if values['dbtype'] == 'MySQL':
            self.ToDB = ToMySQL(values)
        elif values['dbtype'] == 'Oracle':
            self.ToDB = ToOracle(values)
        elif values['dbtype'] == 'SQL Server':
            self.ToDB = ToSqlserver(values)
        elif values['dbtype'] == 'Hive':
            self.ToDB = ToHive(values)
        self.ConnDB = self.ToDB.ConnDB
        self.conn_db = self.ToDB.conn_db

    def main(self, window=None):
        self.window = window

        # get all excel files
        excels_dict = self.FromExcels.get_excels()
        if not excels_dict:
            if window:
                sg.Popup('No Excels!')
            else:
                self.print('No Excels')
            return

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
            self.ConnDB.exec(self.conn_db, sql)

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
                                tablename = tablename + '_' + re.sub(r"[^\w]+", "_", sheet_name, flags=re.IGNORECASE)
                                excel = excel_name + '.' + sheet_name
                            tablename = tablename.lower()
                            if self.values['trf_cn']:
                                tablename = ''.join([i[0] for i in pn.pinyin(tablename, style=pn.Style.FIRST_LETTER)])
                            # cut off table name
                            if len(tablename) > 62:
                                tablename = tablename[:61]
                                if tablename in imported_tables:
                                    tablename = tablename + '_{}'.format(num_suffix)
                                    num_suffix += 1
                                    self.print('Warnning: ', text_color='yellow', end='')
                                    self.print('{0})'.format(excel))
                                    with open(log_file, "a") as fw:
                                        fw.write("table name added suffix: {0}, tablename: {1}\n".format(excel, tablename))
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
                                        fw.write("table name added suffix: {0}, tablename: {1}\n".format(excel, tablename))
                        if len(dataset.columns) == 0 or (dataset.empty and self.values['skip_blank_sheet']):
                            raise EmptyError("Empty Table")

                        col_maxlen, dataset = self.FromExcels.parse_data(dataset)

                        # create table
                        created_sql = None
                        if self.values['mode1']:
                            created_table, created_sql = self.ToDB.create_table(col_maxlen, tablename)

                        self.ToDB.insert_data(dataset, tablename, created_sql, os.path.dirname(log_file))
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
                            self.ConnDB.exec(self.conn_db, sql)
                        with open(log_file, 'a') as (fw):
                            fw.write('Failed Sheet: {0}, error: {1}\n'.format(excel, str(reason)))
                        continue

                    else:
                        self.print('Succeed: {}'.format(excel))
                        num_s += 1
                    finally:
                        num += 1
                        if self.values['dbtype'] == 'MySQL':
                            self.sql_mode = self.ToDB.sql_mode
                            self.ConnDB.exec(self.conn_db, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

            except Exception as reason:
                self.print('Failed: ', text_color='red', end='')
                self.print('{0})'.format(excel))
                with open(log_file, "a") as fw:
                    fw.write("Failed Excel: {0}, error: {1}\n".format(excel, str(reason)))
                num += 1
                continue

        self.print('\nTotal: {}, Succeed: {}\n'.format(num, num_s))

        # run sql_after
        if self.values['sql_after']:
            with open(self.values['sql_after'], 'r') as fr:
                sql = fr.read()
            self.print("Running SQL in {}...\n".format(self.values['sql_after']))
            self.ConnDB.exec(self.conn_db, sql)
        self.conn_db.close()

        if os.path.isfile(log_file):
            if window:
                layout = [
                    [sg.Text('Import Complete with log!\n\nTotal: {}, Succeed: {}\n'.format(num, num_s))],
                    [sg.OK('Finish'), sg.Text(' '*10), sg.Button('View Log', key='E')]
                ]
                window = sg.Window(layout=layout, title='Report')
                event, self.values = window.read()
                window.close()
                if event == 'E':
                    os.popen(log_file)
            else:
                self.print("Import Complete with log: {}".format(log_file))
        else:
            if window:
                layout = [
                    [sg.Text('Import Complete!\n\nTotal: {}, Succeed: {}\n'.format(num, num_s))],
                    [sg.OK('Finish'), sg.Text(' '*10)]
                ]
                window = sg.Window(layout=layout, title='Report')
                event, self.values = window.read()
                window.close()
            else:
                self.print("Import Complete!".format(log_file))

    def print(self, value, text_color=None, end='\n'):
        if self.window:
            return self.window['output'].print(value, text_color=text_color, end=end)
        else:
            return print(value, end=end)


class EmptyError(Exception):
    # when skip empty table, raise this exception
    pass
