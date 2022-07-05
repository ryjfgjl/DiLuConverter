"""
Tool Name: ExcelToDatabase
Version: V5.0
Bref: A tool which can batch import multiple excel files into mysql/oracle/sql server/hive database automatically.
Feature: Batch Automation, One-Click, High Speed, Intelligent, Advanced Options, Schedule
Tested Environment: Windows/Linux, MySQL/Oracle/SQL Server/Hive, Excel(xls,xlsx,csv,xlsm)
Author: ryjfgjl
Help Email: 2577154121@qq.com
QQ Group: 788719152
"""
import PySimpleGUI as sg
import traceback
import sys

from common.handleconfig import HandleConfig
from gui.gui import Gui

Gui = Gui()

Version = '5.0'

if len(sys.argv) <= 1:
    # normal start, run with a gui
    # cmd:python main.py
    # windows:ExcelToDatabase.exe
    # linux:./ExcelToDatabase

    HandleConfig = HandleConfig()

    def exception_format():
        # format exception output
        return "".join(traceback.format_exception(
            sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2], limit=-1
        ))

    default_values = HandleConfig.get_defaults()

    def show_window(values):
        window = sg.Window('ExcelToDatabase {0}'.format(Version), Gui.generate_layout(values),
                       location=(700, 50), icon='excel.ico')
        window.Finalize()
        return window
    window = show_window(default_values)

    while True:
        # keep running with a gui event if any error occurs
        # until click x to close
        try:
            event, values = window.read()

            if values is not None:
                values['language'] = default_values['language']
                values['dbtype'] = default_values['dbtype']
                values['schedule'] = False
                values['source'] = default_values['source']
                if values['mode1']:
                    values['mode'] = 'O'
                else:
                    values['mode'] = 'A'

            if event == "start":
                # when click start button
                # program begins to import excels
                window['start'].update(disabled=True)
                from events.importer import Importer
                Importer = Importer(values)
                Importer.main(window)
                window['start'].update(disabled=False)
            elif event in ['MySQL', 'Oracle', 'SQL Server', 'Hive']:
                # change database type
                values['dbtype'] = event
                window['dbtype'].update(event)
            elif event in ['English', '中文']:
                # change language
                values['language'] = event
                window.close()
                window = show_window(values)
            elif event in ['Directory', 'Files', '选择目录', '选择文件']:
                # change data source
                if event in ['Directory', '选择目录']:
                    source = 'D'
                else:
                    source = 'F'
                values['source'] = source
                window.close()
                window = show_window(values)
            elif event in ['About', '关于']:
                msg = """ExcelToDatabase V{0}\n\nHelp Email: 2577154121@qq.com\nQQ Group: 788719152
                \n\nCopyright @ ryjfgjl             
                        """.format(Version)
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
    # command line without gui
    # need add a config file as a parameter, tool reads all configuration from a config.ini
    # and run on background without gui
    # cmd:python main.py config.ini
    # windows: ExcelToDatabase.exe config.ini
    # linux: ./ExcelToDatabase config.ini
    configini = sys.argv[1]
    HandleConfig = HandleConfig(configini)
    values = HandleConfig.get_defaults()
    values['schedule'] = True
    values['mode1'] = False
    values['mode2'] = False
    if values['mode'] == 'O':
        values['mode1'] = True
    else:
        values['mode2'] = True
    from events.importer import Importer
    Importer = Importer(values)
    Importer.main()
