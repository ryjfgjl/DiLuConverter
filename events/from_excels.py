##############################################################
# from excel
# get excels, parse data
##############################################################

import os
import re
from collections import defaultdict
import numpy as np
import pandas as pd
import chardet
from common.handleconfig import HandleConfig

class FromExcels:

    def __init__(self, values):
        self.values = values
        self.HandleConfig = HandleConfig()

    # get all excels upder directionary
    def get_excels(self):
        excels_dict = defaultdict()
        if self.values['loop_subdir']:
            excels = []
            for root, dirs, files in os.walk(self.values['file_dir']):
                root = root.replace(self.values['file_dir'], '')[1:]
                if len(root) > 1:
                    root = root + '\\'
                for file in files:
                    file = root + file
                    excels.append(file)
            for excel in excels:
                excel_dir = self.values['file_dir'] + "\\" + excel
                if os.path.isfile(excel_dir) and re.fullmatch(r"^.*?\.(xls|xlsx|csv)$", excel, flags=re.IGNORECASE):
                    if self.values['mode2'] and self.values['tname']:
                        tablename = self.values['tname']
                    else:
                        tablename = self.values['prefix'].lower() + re.sub(r"\.(xls|xlsx|csv)$", '', excel.lower(),
                                                                           flags=re.IGNORECASE)
                        # 替换非文字字符为"_"
                        tablename = re.sub(r"[^\w]+", "_", tablename, flags=re.IGNORECASE)

                    excels_dict[excel] = tablename
        else:
            excels = os.listdir(self.values['file_dir'])
            for excel in excels:
                excel_dir = self.values['file_dir'] + "\\" + excel
                if os.path.isfile(excel_dir) and re.fullmatch(r"^.*?\.(xls|xlsx|csv)$", excel, flags=re.IGNORECASE):
                    if self.values['mode2'] and self.values['tname']:
                        tablename = self.values['tname']
                    else:
                        tablename = self.values['prefix'].lower() + re.sub(r"\.(xls|xlsx|csv)$", '', excel.lower(), flags=re.IGNORECASE)
                        # 替换非文字字符为"_"
                        tablename = re.sub(r"[^\w]+", "_", tablename, flags=re.IGNORECASE)

                    excels_dict[excel] = tablename
        return excels_dict

    # get sheets in excel
    def get_data(self, excel):
        na_values = self.values['na_values'].split(',')
        if not self.values['header']:
            header = 0
        else:
            header = int(self.values['header'])
        # csv
        if re.fullmatch(r"^.*?\.csv$", excel, flags=re.IGNORECASE):
            datasets = defaultdict()
            csv = self.values['file_dir'] + "\\" + excel
            # how to deal with csv encoding
            # http://pandaproject.net/docs/determining-the-encoding-of-a-csv-file.html
            csv_encoding = 'utf8'
            if self.values['csv_encoding'] != 'AUTO':
                csv_encoding = self.values['csv_encoding']

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

        # excel
        if re.fullmatch(r"^.*?\.xlsx?$", excel, flags=re.IGNORECASE):
            excel = self.values['file_dir'] + "\\" + excel
            datasets = pd.read_excel(excel, dtype=str, na_values=na_values, keep_default_na=False, header=header,
                                     sheet_name=None)
        return datasets

    # parse data in sheet
    def parse_data(self, dataset):
        dataset = dataset.fillna(value="")
        # trim space
        if self.values['trim']:
            f = lambda x: str(x).strip()
            dataset = dataset.applymap(f)
        f = lambda x: len(x)
        # get length of data
        df1 = dataset.applymap(f)
        f = lambda x: max(x)
        # max length
        df3 = df1.apply(f, axis=1)
        df3 = pd.DataFrame(df3, columns=['c'])
        indexs = df3.loc[(df3['c'] == 0)].index
        # delete blank lines
        if self.values['del_blank_lines']:
            dataset.drop(indexs, inplace=True)

        # deal with column name
        dataset.columns = [str(col) for col in dataset.columns]
        columns = dataset.columns
        low_col = [col.lower() for col in columns]
        # s = len(low_col)
        # if the column names are all blank, use next row
        recol = 1
        for col in low_col:
            if 'unnamed: ' not in col:
                recol = 0
                break

        if recol and self.values['del_blank_lines'] and self.values['header'] != '0':
            columns = dataset[0:1]
            columns = np.array(columns)
            columns = columns.tolist()[0]
            dataset.columns = columns
            dataset.drop(dataset[:1].index, inplace=True)
            # low_col = [col.lower() for col in columns]

        # replace %,\n to _ in column
        columns = [str(col).strip().replace('%', '_').replace('\n', '_') for col in columns]
        # deal with blank column name
        f = lambda x: "unnamed" if x == "" else x
        columns = [f(col) for col in columns]

        # cut off column name
        def f(x):
            if len(x.encode("utf8")) <= 63:
                x = x
            elif self.is_Chinese(x):
                x = x[:20].strip()
            else:
                x = x[:62].strip()
            return x

        columns = [f(col) for col in columns]

        # deal with repeated column name
        while 1:
            low_col = [col.lower() for col in columns]
            idx = 0
            # odx = 0
            c = 0
            for i in columns:
                jdx = 0
                n = 1
                if idx == len(columns):
                    continue
                for j in low_col[idx + 1:]:
                    odx = idx + 1 + jdx
                    if j == i.lower():
                        columns[odx] = j + str(n)
                        n += 1
                        c += 1
                    jdx += 1

                idx += 1

            if c == 0:
                break

        dataset.columns = columns
        columns = np.array(columns)
        columns = columns.tolist()
        f = lambda x: max(x)
        # max length
        df1.columns = columns
        df2 = df1.apply(f, axis=0)
        col_maxlen = df2.to_dict()
        # replace '' to null
        f = lambda x: None if x == "" else x
        dataset = dataset.applymap(f)

        return col_maxlen, dataset

    def is_Chinese(self, word):
        for ch in word:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

