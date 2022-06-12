#######################################################################################################################
# Tool Name: ExcelToDatabase
# Version: V4.5
# Bref: A tool which can batch import excel files into mysql/oracle database.
# Feature: Automation, One-Click, High Speed, Automatic Correct Error
# Tested Environment: Windows 7+, MySQL 5.6+/Oracle 11g+/SQL Server, Excel 1997+(xls,xlsx,csv,xlsm)
# Author: ryjfgjl
# Help Email: 2577154121@qq.com
#######################################################################################################################

# Version
Version = "4.5"

import PySimpleGUI as sg
import traceback
import sys
import pyperclip
# import configuration file
from common.handleconfig import HandleConfig
from gui.gui import Gui


if len(sys.argv) >= 2:
    configini = sys.argv[1]
    HandleConfig = HandleConfig(configini)
    values = HandleConfig.get_defaults()
    values['schedule'] = True
    # start
    from events.importer import Importer
    Importer = Importer(values)
    Importer.main()

else:
    sg.ChangeLookAndFeel('dark')
    HandleConfig = HandleConfig()
    Gui = Gui()

    # format exception output
    def exception_format():
        return "".join(traceback.format_exception(
            sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2],limit=1
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
                values['schedule'] = False
            # start
            if event == "Start" or event == "开     始":
                from events.importer import Importer
                Importer = Importer(values)
                Importer.main()
            # change database type
            elif event == 'MySQL' or event == 'Oracle' or event == 'SQL Server':
                from events.setting import Setting
                Setting = Setting()
                Setting.db_type(event)
                window.close()
                HandleConfig.save_defaults(values)
                window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(), location=(700, 100))
                window.Finalize()
            # change language
            elif event == 'English' or event == '中文':
                from events.setting import Setting
                Setting = Setting()
                Setting.switch_langage(event)
                window.close()
                HandleConfig.save_defaults(values)
                window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(), location=(700, 100))
                window.Finalize()
            elif event == "联系方式":
                from events.setting import Setting
                Setting = Setting()
                msg = Setting.help()
                sg.Popup(msg, title='Help')
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
