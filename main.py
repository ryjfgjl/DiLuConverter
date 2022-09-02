"""
Tool Name: ExcelToDatabase
Bref: A tool which can batch import multiple excel files into mysql/oracle/sql server/hive database automatically.
Feature: Batch Automation, One-Click, High Speed, Intelligent, Advanced Options, Schedule
Tested Environment: Windows/Linux, MySQL/Oracle/SQL Server/Hive, Excel(xls,xlsx,csv,xlsm)
Author: ryjfgjl
Help Email: 2577154121@qq.com
QQ Group: 788719152

Copyright (c) 2022 ryjfgjl
This program is a free software and it is under the MIT License.
"""
import sys

VERSION = '5.1'

if len(sys.argv) <= 1:
    # run with window
    # cmd:python main.py
    # windows:ExcelToDatabase.exe
    # linux:./ExcelToDatabase
    from events.window import Window

    Window = Window()
    Window.VERSION = VERSION
    Window.main()
else:
    # run on background without window
    # need add a config file as a parameter, tool reads all configuration from a config.ini
    # and run on background without gui
    # cmd:python main.py config.ini
    # windows: ExcelToDatabase.exe config.ini
    # linux: ./ExcelToDatabase config.ini
    configini = sys.argv[1]
    from events.background import Background

    Background = Background()
    Background.configini = configini
    Background.main()
