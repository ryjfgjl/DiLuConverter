##############################################################
# tool uses config.ini to save inputs and get saved configuration when program start
##############################################################
import os
import sys
import configparser


class HandleConfig:

    def __init__(self, configini=None):
        # when running in command line without gui, a config.ini is needed
        # when running with gui, config.ini is under the same directory with ExcelToDatabase program
        if configini != None:
            self.configini = configini
        else:
            realpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
            self.configini = realpath + r"/config.ini"

    def handle_config(self, option=None, section=None, key=None, value=None):
        conf = configparser.ConfigParser()
        conf.read(self.configini, encoding='utf8')
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

        with open(self.configini, 'w', encoding='utf8') as fw:
            conf.write(fw)

    def get_defaults(self):
        # general
        language = self.handle_config("g", "general", "language")
        source = self.handle_config("g", "general", "source")
        mode = self.handle_config("g", "general", 'mode')
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
        # advanced
        csv_encoding = self.handle_config("g", "advanced", "csv_encoding")
        na_values = self.handle_config("g", "advanced", "na_values")
        prefix = self.handle_config("g", "advanced", 'prefix')

        tname = self.handle_config("g", "advanced", 'tname')
        header = self.handle_config("g", "advanced", 'header')
        del_blank_lines = eval(self.handle_config("g", "advanced", 'del_blank_lines'))

        trim = eval(self.handle_config("g", "advanced", 'trim'))
        skip_blank_sheet = eval(self.handle_config("g", "advanced", 'skip_blank_sheet'))
        add_tname = eval(self.handle_config("g", "advanced", 'add_tname'))
        loop_subdir = eval(self.handle_config("g", "advanced", 'loop_subdir'))
        trf_cn = eval(self.handle_config("g", "advanced", 'trf_cn'))

        sql_b4 = self.handle_config("g", "advanced", 'sql_b4')
        sql_after = self.handle_config("g", "advanced", 'sql_after')

        default_values = {
            'language': language,
            'source': source,
            'mode': mode,

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

            'prefix': prefix,
            'tname': tname,
            'header': header,

            'del_blank_lines': del_blank_lines,
            'trim': trim,
            'skip_blank_sheet': skip_blank_sheet,

            'add_tname': add_tname,
            'loop_subdir': loop_subdir,
            'trf_cn': trf_cn,

            'sql_b4': sql_b4,
            'sql_after': sql_after,

        }
        return default_values

    def save_defaults(self, values):
        # general
        self.handle_config("s", "general", "language", values['language'])
        self.handle_config("s", "general", "source", values['source'])
        if values['mode1']:
            mode = 'O'
        else:
            mode = 'A'
        self.handle_config("s", "general", "mode", mode)
        # dbinfo
        self.handle_config("s", "dbinfo", "dbtype", values['dbtype'])
        self.handle_config("s", "dbinfo", "host", values['host'])
        self.handle_config("s", "dbinfo", "port", values['port'])
        self.handle_config("s", "dbinfo", "user", values['user'])
        self.handle_config("s", "dbinfo", "passwd", values['passwd'])
        self.handle_config("s", "dbinfo", "dbname", values['dbname'])
        # file
        self.handle_config("s", "file", "file_dir", values['file_dir'])
        self.handle_config("s", "file", "files", values['files'])
        # advanced
        self.handle_config("s", "advanced", "csv_encoding", values['csv_encoding'])
        self.handle_config("s", "advanced", "na_values", values['na_values'])

        self.handle_config("s", "advanced", "prefix", values['prefix'])
        self.handle_config("s", "advanced", "tname", values['tname'])
        self.handle_config("s", "advanced", "header", values['header'])

        self.handle_config("s", "advanced", "del_blank_lines", str(values['del_blank_lines']))
        self.handle_config("s", "advanced", "trim", str(values['trim']))
        self.handle_config("s", "advanced", "skip_blank_sheet", str(values['skip_blank_sheet']))

        self.handle_config("s", "advanced", "add_tname", str(values['add_tname']))
        self.handle_config("s", "advanced", "loop_subdir", str(values['loop_subdir']))
        self.handle_config("s", "advanced", "trf_cn", str(values['trf_cn']))

        self.handle_config("s", "advanced", "sql_b4", values['sql_b4'])
        self.handle_config("s", "advanced", "sql_after", values['sql_after'])

