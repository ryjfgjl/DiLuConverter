# ExcelToDatabase
## Bref: A tool which can batch import excel files into mysql/oracle database.
## Pictures：
<img width="352" alt="屏幕截图 2022-04-22 212542" src="https://user-images.githubusercontent.com/39375647/164977010-ba7d2b56-25f8-42c9-94f2-6a560c5d1656.png"><img width="353" alt="屏幕截图 2022-04-22 212619" src="https://user-images.githubusercontent.com/39375647/164977024-272f292b-a0a1-4088-932f-6666e737c0b8.png">

## Features：
Batch Automation, One-Click, High Speed, Automatic Correct Error, Advanced Option

## Usage
1.Start Program

Way 1: Command: python D:\Projects\ExcelToDatabase\main.py

Way 2: Send an email to 2577154121@qq.com, you can get an exe program which can directly run on windows.

2.Input Information

Choose your database type(mysql or oracle);Select directory with excel files; Input target database information; Choose import mode.

3.Click Start.

## Tested Environments: 
Windows 7+, MySQL 5.6+/Oracle 11g+, Excel 1997+(xls,xlsx,csv)

## Options Detail:

### General：
#### Excel：
Directory: The excel files under this directory would be imported

#### MySQL/Oracle Connection: 
options to connect to database
#### mode:

Overwrite: drop table first(if exists); create table; insert data.

Append: just insert data into table(table needs exist in the database)

### Advanced：
#### CSV Encoding：
Tools can auto-detect encoding of csv files(default), and you can choose or input other value.
#### Replace to null：
values populated will be replaced to null
#### add table prefix：
add table prefix
#### append all data to one exists table：
#### The Column on row：
#### Skip blank line：
#### Trim space：
#### Skip blank sheet：
#### Sub Dir

### Others：
  #### How to define table name：
  file name + '_' + sheet name(if one excel has multipule sheets)
  #### How to define column name：
  Default is the first row
  #### How to define column type：
  Varchar(255) is default. If max length of column more than 255, text will be set.
  #### How to deal with mysql error 1366：
  Auto Correct
  #### How to deal with mysql error 1118：
  All column will be create as text
  
# Author: ryjfgjl
# Send email to 2577154121@qq.com for help.

