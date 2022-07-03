##############################################################
# tool uses config.ini to save inputs and get saved configuration when program start
##############################################################
import os
import sys
import configparser


class HandleConfig:
    def __init__(self, configini=None):
        self.configini = configini

    def handle_config(self, option=None, section=None, key=None, value=None):
        conf = configparser.ConfigParser()
        if self.configini != None:
            configini = self.configini
        else:
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
        # general
        language = self.handle_config("g", "general", "language")
        source = self.handle_config("g", "general", "source")
        # dbinfo
        dbtype = self.handle_config("g", "dbinfo", "dbtype")
        host = self.handle_config("g", "dbinfo", "host")
        port = self.handle_config("g", "dbinfo", "port")
        user = self.handle_config("g", "dbinfo", "user")
        passwd = self.handle_config("g", "dbinfo", "passwd")
        dbname = self.handle_config("g", "dbinfo", "dbname")
        # file
        file_dir = self.handle_config("g", "file", "file_dir")
        files = self.handle_config("g", "file", "files")
        csv_encoding = self.handle_config("g", "file", "csv_encoding")
        na_values = self.handle_config("g", "file", "na_values")
        # get default value: advanced
        mode = self.handle_config("g", "advanced", 'mode')
        if mode == 'mode1':
            mode1 = True
            mode2 = False
        else:
            mode1 = False
            mode2 = True
        prefix = self.handle_config("g", "advanced", 'prefix')
        tname = self.handle_config("g", "advanced", 'tname')
        header = self.handle_config("g", "advanced", 'header')
        add_tname = eval(self.handle_config("g", "advanced", 'add_tname'))
        del_blank_lines = eval(self.handle_config("g", "advanced", 'del_blank_lines'))
        trim = eval(self.handle_config("g", "advanced", 'trim'))
        skip_blank_sheet = eval(self.handle_config("g", "advanced", 'skip_blank_sheet'))
        loop_subdir = eval(self.handle_config("g", "advanced", 'loop_subdir'))
        trf_cn = eval(self.handle_config("g", "advanced", 'trf_cn'))
        sql_b4 = self.handle_config("g", "advanced", 'sql_b4')
        sql_after = self.handle_config("g", "advanced", 'sql_after')

        default_values = {
            'language': language,
            'source': source,
            'dbtype': dbtype,
            'host': host,
            'port': port,
            'user': user,
            'passwd': passwd,
            'dbname': dbname,
            'file_dir': file_dir,
            'files': files,
            'csv_encoding': csv_encoding,
            'na_values': na_values,
            'mode1': mode1,
            'mode2': mode2,
            'prefix': prefix,
            'tname': tname,
            'header': header,
            'add_tname': add_tname,
            'del_blank_lines': del_blank_lines,
            'trim': trim,
            'skip_blank_sheet': skip_blank_sheet,
            'loop_subdir': loop_subdir,
            'trf_cn':trf_cn,
            'sql_b4': sql_b4,
            'sql_after': sql_after,

        }
        return default_values

    def save_defaults(self, values):
        # save input
        self.handle_config("s", "file", "file_dir", values['file_dir'])
        self.handle_config("s", "file", "files", values['files'])
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
        self.handle_config("s", "advanced", "add_tname", str(values['add_tname']))
        self.handle_config("s", "advanced", "del_blank_lines", str(values['del_blank_lines']))
        self.handle_config("s", "advanced", "trim", str(values['trim']))
        self.handle_config("s", "advanced", "skip_blank_sheet", str(values['skip_blank_sheet']))
        self.handle_config("s", "advanced", "loop_subdir", str(values['loop_subdir']))
        self.handle_config("s", "advanced", "trf_cn", str(values['trf_cn']))
        self.handle_config("s", "advanced", "sql_b4", values['sql_b4'])
        self.handle_config("s", "advanced", "sql_after", values['sql_after'])

