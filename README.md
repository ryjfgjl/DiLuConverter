# python-excelimporter
A python tool for batch importing excel/csv files into mysql database.

Usage:

1. You need to edit config.ini first. Please read the comment in config.ini. You must edit the server you will create database on and import excel to.

2. python E:\Python\Project\python-excelimporter\interface.py

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

The description is so simple. Please email me if you have any question.



copyright@ryjfgjl
email: 2577154121@qq.com

