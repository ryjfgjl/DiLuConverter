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

# Version
Version = "4.1"

import PySimpleGUI as sg
import traceback
import sys
import pyperclip
# import configuration file
from common.handleconfig import HandleConfig
from gui.gui import Gui

sg.ChangeLookAndFeel('dark')
HandleConfig = HandleConfig()
Gui = Gui()

# format exception output
def exception_format():
    return "".join(traceback.format_exception(
        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    ))

# GO
default_values = HandleConfig.get_defaults()
window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(), location=(700, 100))
# keep running
while True:
    try:
        event, values = window.read()
        if values != None:
            values['dbtype'] = default_values['dbtype']
        # start
        if event == "开始" or event == '开始0' or event == "Start" or event == 'Start0':
            from events.importer import Importer
            Importer = Importer(values)
            Importer.main()
        # change database type
        elif event == 'MySQL' or event == 'Oracle':
            from events.setting import Setting
            Setting = Setting()
            Setting.db_type(event)
            window.close()
            HandleConfig.save_defaults(values)
            window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(), location=(700, 100))
            window.Finalize()
        # change language
        elif event == '中文' or event == 'English':
            from events.setting import Setting
            Setting = Setting()
            Setting.switch_langage(event)
            window.close()
            HandleConfig.save_defaults(values)
            window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(), location=(700, 100))
            window.Finalize()
        elif event == "获取帮助":
            from events.setting import Setting
            Setting = Setting()
            msg = Setting.help()
            sg.Popup(msg,title='Help')
            pyperclip.copy(msg)
        elif event == sg.WIN_CLOSED:
            break
    except:
        # throw error
        sg.PopupError(exception_format())
    finally:
        if event != sg.WIN_CLOSED:
            HandleConfig.save_defaults(values)
        default_values = HandleConfig.get_defaults()
