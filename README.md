# python-excelimporter
A python tool for batch importing excel/csv files into mysql database.

Test Environment:
Win64
Python 3.7
MySQL 5.6.34
Excel: .xls/xlsx/csv

Python package:
PySimpleGUI
numpy
pandas
pymysql
chardet


Usage:

1. python E:\Python\Project\python-excelimporter\interface.py

2. MySQL Connection:
   Host: 
   Port: 
   User: 
   Password: 
   Database Name:
   Re-Create Database: if selected, tool will drop and create database, otherwise, tool will default the database is existing.
   
   Files:
   File Directionary: Choose your files directionary. The excel/csv files under this directionary will be imported.
   Replace Values: the value seperated by comma will be replaced to null
   CSV Encoding: We can get the encoding from the excel file, but we can not do this from csv file. So we can only detect the encoding from csv. 
		If you know the encoding of all the csv files and they are the same one encoding, you can choose/populate this field. The tool will prefer to use this encoding.
   


The problem solved by tool when we import excel into mysql database:

1. The length of Column Name more than 64 characters. ==> cut off
2. The Column Name inculde space on the first/end. ==> remove space
3. The repeatable column name. ==> add suffix
4. The length of column is too large(>255) ==> change the column from varchar(255) to text.
5. The row size is too large(>65535) ==> change all column from varchar(255) to text.
6. remove the space before/end the data.
7. change all "" character to null.
8. detect encoding from csv and get encoding from excel.
9. import all sheets from excel.(if more than one sheets in the excel, table name will be excel name+_+sheet name)
10. The length of Table Name more than 64 characters. ==> cut off
11. skip empty excel.
12. skip blank row.
13. support import utf8mb4 character
14. support chinese windows

Other:

you can use Cx-Freeze to build it to a exe.

cmd: cd E:\Python\Project\python-excelimporter
python E:\Python\Project\python-excelimporter\setup.py build.

If you have no python on your computer, you can also contact me to get .exe program which can run without python.

The description is so simple. Please email me if you have any question.


author: ryjfgjl
email: 2577154121@qq.com

