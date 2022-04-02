#######################################################################################################################
# Tool Name: ExcelToDatabase
# Version: V4.0
# Bref: A tool which can batch import excel files into mysql/oracle database.
# Feature: Automation, One-Click, High Speed, Automatic Correct Error
# Tested Environment: Windows 7+, MySQL 5.6+/Oracle 11g+, Excel 1997+(xls,xlsx,csv)
# Author: ryjfgjl
# Help Email: 2577154121@qq.com
# Source: QQ群788719152
#######################################################################################################################

##############################################################
# Program GUI
##############################################################

# Version
Version = "4.0"

import PySimpleGUI as sg
import traceback
import sys
# import configuration file
from common.handleconfig import HandleConfig


sg.ChangeLookAndFeel('dark')
HandleConfig = HandleConfig()

# get default value: dbinfo
dbtype = HandleConfig.handle_config("g", "dbinfo", "dbtype")
host = HandleConfig.handle_config("g", "dbinfo", "host")
port = HandleConfig.handle_config("g", "dbinfo", "port")
user = HandleConfig.handle_config("g", "dbinfo", "user")
passwd = HandleConfig.handle_config("g", "dbinfo", "passwd")
dbname = HandleConfig.handle_config("g", "dbinfo", "dbname")
# get default value: file
file_dir = HandleConfig.handle_config("g", "file", "file_dir")
csv_encoding = HandleConfig.handle_config("g", "file", "csv_encoding")
na_values = HandleConfig.handle_config("g", "file", "na_values")
# get default value: advanced
mode = HandleConfig.handle_config("g", "advanced", 'mode')
prefix = HandleConfig.handle_config("g", "advanced", 'prefix')
tname = HandleConfig.handle_config("g", "advanced", 'tname')
header = HandleConfig.handle_config("g", "advanced", 'header')
del_blank_lines = eval(HandleConfig.handle_config("g", "advanced", 'del_blank_lines'))
trim = eval(HandleConfig.handle_config("g", "advanced", 'trim'))
skip_blank_sheet = eval(HandleConfig.handle_config("g", "advanced", 'skip_blank_sheet'))


def default_mode(_mode):
    if _mode == mode:
        return True
    else:
        return False

# format exception output
def exception_format():
    return "".join(traceback.format_exception(
        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    ))


# generate GUI
def generate_layout(dbtype):
    # menu
    menu_def = [
        ['&显示语言', ['&中文', '&English']],
        ['&数据库类型', ['&MySQL', '&Oracle']],
    ]
    # general
    layout_general = [
        [sg.Menu(menu_def)],
        [sg.Text('Excel文件', size=(12, 1), text_color='red')],
            [sg.Text('所在文件夹:', size=(12, 1)), sg.Input('{}'.format(file_dir), key='file_dir', size=(35, 1)),
             sg.FolderBrowse(initial_folder='{}'.format(file_dir), button_text=' 选择 ')],
        [sg.Text('{}连接'.format(dbtype), size=(12, 1), text_color='red'),
         ],

        [sg.Text('主机:', size=(5, 1)), sg.Input('{}'.format(host), key='host', size=(15, 1)), sg.Text(' ' * 11),
             sg.Text('端口:', size=(7, 1)), sg.Input('{}'.format(port), key='port', size=(15, 1)), ],
            [sg.Text('用户:', size=(5, 1)), sg.Input('{}'.format(user), key='user', size=(15, 1)), sg.Text(' ' * 11),
             sg.Text('密码:', size=(7, 1)), sg.Input('{}'.format(passwd), key='passwd', size=(15, 1)), ],
            [

             sg.Text('数据库:', size=(5, 1)), sg.Input('{}'.format(dbname), key='dbname', size=(21, 1)), sg.Text(' ' * 1),
             sg.Text('模式:', text_color='red'),
             sg.Text(' ' * 1),
              sg.Radio('覆盖', group_id='mode', key='mode1', default=default_mode('mode1')),
              sg.Radio('追加', group_id='mode', key='mode2', default=default_mode('mode2')),
             ],

        [sg.Button('开始', size=(52, 1))]
    ]
    # advanced
    layout_advanced = [
        [sg.Text('CSV文件编码:', size=(12, 1)),
            sg.Combo(['AUTO', 'UTF-8', 'ANSI', 'GBK'], default_value=csv_encoding, key='csv_encoding', size=(10, 1))],
        [sg.Text('将这些值替换为null:', size=(15, 1)),sg.Input('{}'.format(na_values), key='na_values', size=(40, 1)), ],
        [sg.Text('为创建的表名添加前缀:', size=(18, 1)), sg.Input(prefix, key='prefix', size=(20, 1),), ],
        [sg.Text('将数据追加到已存在的表（追加模式有效）:', size=(34, 1)), sg.Input(tname, key='tname', size=(20, 1), ), ],
        [sg.Text('指定列名所在行数:', size=(18, 1)), sg.Input(header, key='header', size=(10, 1)), ],
        [sg.Checkbox('删除空行', key='del_blank_lines', size=(10, 1), default=del_blank_lines),
         sg.Checkbox('去除字符前后空格', key='trim', size=(20, 1), default=trim),
         sg.Checkbox('跳过空表', key='skip_blank_sheet', size=(10, 1), default=skip_blank_sheet), ],


        [sg.Button('开始', size=(52, 1))]
    ]

    tab_layouts = [sg.Tab('常规', layout_general), sg.Tab('高级', layout_advanced)]

    layout = [
        [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
    ]
    return layout


# GO
window = sg.Window('ExcelToDatabase {0}'.format(Version), generate_layout(dbtype), location=(700, 100))

# keep running
while True:
    try:
        event, values = window.read()
        # start
        if event == "开始" or event == '开始0':
            if dbtype == 'MySQL':
                from events.excelimporter import ImportExcel
                ImportExcel = ImportExcel()
                ImportExcel.main(values)
            elif dbtype == 'Oracle':
                from events.to_oracle import ToOracle
                ToOracle = ToOracle()
                ToOracle.main(values)
        # change database type
        elif event == 'MySQL' or event == 'Oracle':
            from events.setting import Setting
            Setting = Setting()
            Setting.db_type(event)
            window.close()
            window = sg.Window('ExcelToDatabase {0}'.format(Version), generate_layout(event), location=(700, 100))
            window.Finalize()
            dbtype = HandleConfig.handle_config("g", "dbinfo", "dbtype")

        elif event == sg.WIN_CLOSED:
            break
    except:
        # throw error
        sg.PopupError(exception_format())
