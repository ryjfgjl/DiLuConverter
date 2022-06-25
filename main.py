"""
Tool Name: ExcelToDatabase
Version: V4.7
Bref: A tool which can batch import multiple excel files into mysql/oracle database automatically.
Feature: Batch Automation, One-Click, High Speed, Intelligent, Advanced Options, Schedule
Tested Environment: Windows 7+, MySQL 5.6+/Oracle 11g+, Excel 1997+(xls,xlsx,csv,xlsm)
Author: ryjfgjl
Help Email: 2577154121@qq.com
QQ Group: 788719152
"""
import PySimpleGUI as sg
import traceback
import sys

from common.handleconfig import HandleConfig
from gui.gui import Gui

Version = '4.7'

if len(sys.argv) <= 1:
    # normal start, run with a gui
    # cmd:python D:\Projects\ExcelToDatabase\main.py
    # exe:ExcelToDatabase.exe
    sg.ChangeLookAndFeel('dark')
    HandleConfig = HandleConfig()
    Gui = Gui()

    def exception_format():
        # format exception output
        return "".join(traceback.format_exception(
            sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2], limit=-1
        ))

    default_values = HandleConfig.get_defaults()
    window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(), location=(700, 50))

    while True:
        try:
            event, values = window.read()

            if values is not None:
                values['dbtype'] = default_values['dbtype']
                values['schedule'] = False
                values['source'] = default_values['source']

            if event == "start":
                # when click start button
                # program wil begin to import excels
                window['start'].update(disabled=True)
                from events.importer import Importer
                Importer = Importer(values)
                Importer.main(window)
                window['start'].update(disabled=False)
            elif event == 'MySQL' or event == 'Oracle' or event == 'SQL Server':
                # change database type
                from events.setting import Setting
                Setting = Setting()
                Setting.db_type(event)
                window['dbtype'].update(event)
                HandleConfig.save_defaults(values)
            elif event == 'English' or event == '中文':
                # change language
                from events.setting import Setting
                Setting = Setting()
                Setting.switch_langage(event)
                window.close()
                HandleConfig.save_defaults(values)
                window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(), location=(700, 50))
                window.Finalize()
            elif event == 'Directory' or event == 'Files' or event == '选择目录' or event == '选择文件':
                # change data source
                from events.setting import Setting
                Setting = Setting()
                Setting.data_source(event)
                window.close()
                HandleConfig.save_defaults(values)
                window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(), location=(700, 50))
                window.Finalize()
            elif event == "关于" or event == 'About':
                msg = """ExcelToDatabase V4.6\n\nHelp Email: 2577154121@qq.com\nQQ Group: 788719152
                \n\nCopyright @ ryjfgjl             
                        """
                sg.Popup(msg, title='Help')
            elif event == sg.WIN_CLOSED:
                break
        except:
            # throw exception
            window['start'].update(disabled=False)
            sg.PopupError(exception_format())
        finally:
            if event != sg.WIN_CLOSED:
                HandleConfig.save_defaults(values)
            default_values = HandleConfig.get_defaults()
else:
    # schedule
    # need add a config file as a parameter, tool reads all configuration from the config.ini
    # and run on background without gui
    # cmd:python D:\Projects\ExcelToDatabase\main.py D:\Projects\ExcelToDatabase\config.ini
    # or D:\Projects\ExcelToDatabase4.5\ExcelToDatabase.exe D:\Projects\ExcelToDatabase\config.ini
    configini = sys.argv[1]
    HandleConfig = HandleConfig(configini)
    values = HandleConfig.get_defaults()
    values['schedule'] = True
    from events.importer import Importer
    Importer = Importer(values)
    Importer.main()
