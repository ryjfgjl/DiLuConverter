
import os, sys
from common.handleconfig import HandleConfig


class Setting:

    def __init__(self):
        self.realpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
        self.configini = self.realpath + '\\config.ini'
        self.HandleConfig = HandleConfig()

    def db_type(self, dbtype):
        self.HandleConfig.handle_config('s', 'dbinfo', 'dbtype', dbtype)

    def switch_langage(self, language):
        self.HandleConfig.handle_config('s', 'general', 'language', language)
