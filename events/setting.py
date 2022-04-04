
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

    def help(self):
        msg = """
            获取工具最新版本：请前往QQ群788719152群文件下载
            如有疑问：请前往QQ群788719152咨询或发送邮件至2577154121@qq.com
            在线文档：https://blog.csdn.net/qq_37955852/article/details/122488507?spm=1001.2014.3001.5502
            源代码：https://github.com/ryjfgjl/ExcelToDatabase
            
            点击OK，复制到剪切板
        """
        return msg