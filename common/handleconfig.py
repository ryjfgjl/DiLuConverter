"""
 get or set something with config.ini
"""

import os
import sys
import configparser

class HandleConfig:

    # handle config.ini
    def handle_config(self, option=None, section=None, key=None, value=None):

        conf = configparser.ConfigParser()
        realpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
        configini = realpath + r"\config.ini"

        conf.read(configini)
        if option == 'g':
            value = conf.get(section, key)
            return value
        elif option == 's':
            conf.set(section, key, value)
        elif option == "a":
            conf.add_section(section)
        elif option == "rs":
            conf.remove_section(section)
        elif option == "ro":
            conf.remove_option(section, key)

        with open(configini, 'w') as fw:
            conf.write(fw)

    def get_defaults(self):
        # get default value: general
        language = self.handle_config("g", "general", "language")
        # get default value: dbinfo
        dbtype = self.handle_config("g", "dbinfo", "dbtype")
        host = self.handle_config("g", "dbinfo", "host")
        port = self.handle_config("g", "dbinfo", "port")
        user = self.handle_config("g", "dbinfo", "user")
        passwd = self.handle_config("g", "dbinfo", "passwd")
        dbname = self.handle_config("g", "dbinfo", "dbname")
        # get default value: file
        file_dir = self.handle_config("g", "file", "file_dir")
        csv_encoding = self.handle_config("g", "file", "csv_encoding")
        na_values = self.handle_config("g", "file", "na_values")
        # get default value: advanced
        mode = self.handle_config("g", "advanced", 'mode')
        prefix = self.handle_config("g", "advanced", 'prefix')
        tname = self.handle_config("g", "advanced", 'tname')
        header = self.handle_config("g", "advanced", 'header')
        del_blank_lines = eval(self.handle_config("g", "advanced", 'del_blank_lines'))
        trim = eval(self.handle_config("g", "advanced", 'trim'))
        skip_blank_sheet = eval(self.handle_config("g", "advanced", 'skip_blank_sheet'))
        loop_subdir = eval(self.handle_config("g", "advanced", 'loop_subdir'))

        default_values = {
            'language': language,
            'dbtype': dbtype,
            'host': host,
            'port': port,
            'user': user,
            'passwd': passwd,
            'dbname': dbname,
            'file_dir': file_dir,
            'csv_encoding': csv_encoding,
            'na_values': na_values,
            'mode': mode,
            'prefix': prefix,
            'tname': tname,
            'header': header,
            'del_blank_lines': del_blank_lines,
            'trim': trim,
            'skip_blank_sheet': skip_blank_sheet,
            'loop_subdir': loop_subdir,
        }
        return default_values

    def save_defaults(self, values):
        # save input
        self.handle_config("s", "file", "file_dir", values['file_dir'])
        self.handle_config("s", "file", "csv_encoding", values['csv_encoding'])
        self.handle_config("s", "dbinfo", "host", values['host'])
        self.handle_config("s", "dbinfo", "port", values['port'])
        self.handle_config("s", "dbinfo", "user", values['user'])
        self.handle_config("s", "dbinfo", "passwd", values['passwd'])
        self.handle_config("s", "dbinfo", "dbname", values['dbname'])
        if values['mode1']:
            self.handle_config("s", "advanced", "mode", 'mode1')
        else:
            self.handle_config("s", "advanced", "mode", 'mode2')
        self.handle_config("s", "advanced", "prefix", values['prefix'])
        self.handle_config("s", "advanced", "tname", values['tname'])
        self.handle_config("s", "advanced", "header", values['header'])
        self.handle_config("s", "advanced", "del_blank_lines", str(values['del_blank_lines']))
        self.handle_config("s", "advanced", "trim", str(values['trim']))
        self.handle_config("s", "advanced", "skip_blank_sheet", str(values['skip_blank_sheet']))
        self.handle_config("s", "advanced", "loop_subdir", str(values['loop_subdir']))

