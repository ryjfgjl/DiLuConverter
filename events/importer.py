##############################################################
# Importer
# From Excel, To MySQL ro To Oracle
##############################################################

import PySimpleGUI as sg
import os
import re
from common.handleconfig import HandleConfig
from events.from_excels import FromExcels
from events.to_mysql import ToMySQL
from events.to_oracle import ToOracle

class Importer:

    def __init__(self, values):
        self.values = values
        self.HandleConfig = HandleConfig()
        self.FromExcels = FromExcels(values)
        if values['dbtype'] == 'MySQL':
            self.ToDB = ToMySQL(values)
            self.ConnDB = self.ToDB.ConnDB
            self.conn_db = self.ToDB.conn_db
            self.sql_mode = self.ToDB.sql_mode
        else:
            self.ToDB = ToOracle(values)
            self.ConnDB = self.ToDB.ConnDB
            self.conn_db = self.ToDB.conn_db

    def main(self):

        # get all excel files
        excels_dict = self.FromExcels.get_excels()
        if not excels_dict:
            sg.Popup('No Excels!')
            return

        # record error log
        log_file = self.values['file_dir'] + "\\importlog.txt"
        if os.path.isfile(log_file):
            os.remove(log_file)

        # count of tables
        num = 0
        # count of succeed tables
        num_s = 0

        print("\n\nBegin Import...\n")
        # loop all excel files
        for excel, tablename in excels_dict.items():
            try:
                datasets = self.FromExcels.get_data(excel)
                excel_name = excel
                # loop all sheets in one excel
                for k, v in datasets.items():
                    created_table = None
                    try:
                        sheet_name = k
                        dataset = v
                        if self.values['mode2'] and self.values['tname']:
                            if len(datasets) > 1:
                                excel = excel_name + '.' + sheet_name
                        else:
                            # concat excel name and sheet name
                            if len(datasets) > 1:
                                tablename = tablename + '_' + re.sub(r"[^\w]+", "_", sheet_name, flags=re.IGNORECASE)
                                excel = excel_name + '.' + sheet_name
                            tablename = tablename.lower()
                            # cut off table name
                            if len(tablename.encode("utf8")) > 64:
                                if self.is_Chinese(tablename):
                                    tablename = tablename[:20]
                                else:
                                    tablename = tablename[:60]
                                with open(log_file, "a") as fw:
                                    fw.write("table name cut off: {0}, tablename: {1}\n".format(excel, tablename))

                        if len(dataset.columns) == 0 or (dataset.empty and self.values['skip_blank_sheet']):
                            raise EmptyError("Empty Table")
                        col_maxlen, dataset = self.FromExcels.parse_data(dataset)

                        # create table
                        created_sql = None
                        if self.values['mode1']:
                            created_table, created_sql = self.ToDB.create_table(col_maxlen, tablename)
                        self.ToDB.insert_data(dataset, tablename, created_sql)

                    except Exception as reason:
                        print('Failed: {}'.format(excel))
                        if created_table:
                            if self.values['dbtype'] == 'MySQL':
                                sql = 'drop table if exists `{0}`'.format(created_table)
                            else:
                                sql = 'drop table "{0}"'.format(created_table)
                            self.ConnDB.exec(self.conn_db, sql)
                        with open(log_file, 'a') as (fw):
                            fw.write('Failed Sheet: {0}, error: {1}\n'.format(excel, str(reason)))
                        continue

                    else:
                        print('Succeed: {}'.format(excel))
                        num_s += 1
                    finally:
                        num += 1
                        if self.values['dbtype'] == 'MySQL':
                            self.ConnDB.exec(self.conn_db, 'set SESSION sql_mode = "{}"'.format(self.sql_mode))

            except Exception as reason:
                print("Failed: {}".format(excel))
                with open(log_file, "a") as fw:
                    fw.write("Failed Excel: {0}, error: {1}\n".format(excel, str(reason)))
                num += 1
                continue

        print('\nTotal: {}, Succeed: {}\n'.format(num, num_s))
        self.conn_db.close()
        if os.path.isfile(log_file):
            layout = [
                [sg.Text('Import Complete with log！\n\nTotal: {}, Succeed: {}\n'.format(num, num_s))],
                [sg.OK('Finish'), sg.Text(' '*10), sg.Button('View Log', key='E')]
            ]
        else:
            layout = [
                [sg.Text('Import Complete！\n\nTotal: {}, Succeed: {}\n'.format(num, num_s))],
                [sg.OK('Finish')]
            ]
        window = sg.Window(layout=layout, title='Report')
        event, self.values = window.read()
        window.close()
        if event == 'E':
            os.popen(log_file)
        return

    def is_Chinese(self, word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

# empty table
class EmptyError(Exception):
    pass
