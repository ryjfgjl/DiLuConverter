
![image](https://user-images.githubusercontent.com/39375647/174487675-d8d4a23b-df6d-43b0-ac5f-24742b4f4c0b.png)

# ExcelToDatabase: batch import multiple excel files into database

## What is it?
**ExcelToDatabase** is an automatical tool which can batch import multiple excel files into database(mysql/oracle/sqlserver/hive).It frees your hands when you have many excels need to import into database, or you do not want to deal with all kinds of problem when manually import excel any more

## Features
### Easily
  Only need you provide the location of excels and the connect information of database, the tool can work until all the excels are imported

### Quickly: 
  Batch importting make it faster than manual tool like navicate over the count of your excels times. If you have 10 excels, it is faster 10x

### Intelligent: 
  When you manually import excel into database using tool like navicate, whether if you feel sad when error occurs? Baddly, other error occurs when you just fix one. DO NOT WORRY! The tool can deal with them!

### Advanced: 
  Rich options could be custom choose to make more fuction come true.

### Schedule: 
  You can make a schedule using it on windows/linux.

## Where to get it
The source code is here.

The packaged executable program(.exe on windows or a file on linux) are available, you can send an email 2577154121@qq.com to get it.

## Usage
**Start Program**
If you hive python environment, you can use command to start:

`python D:\Projects\ExcelToDatabase\main.py`

If you get a packaged executable program:

On Windows: ExcelToDatabase.exe

On Linux: ./ExcelToDatabase

**Choose and Input**

Choose the directory with excel files; Input target database information; Choose import mode

**Click Start**

## Supported Environments: 
Windows/Linux, MySQL/Oracle/SQLServer/Hive, Excel(xls,xlsx,xlsm,csv)

## Menu
### Language
English and Chinese you can choose to display

### Database
MySQL/Oracle/SQLServer/Hive, you can choose one database according to your target database

### Data Source
Directory: choose Directory as your data source, in this case, excels under the directory will be imported
Files: choose Files as your data source, in this case, you can select one or more excel files to import

## Options:
In general, you only need to provide information in the section of "General". But if you want to do more, you may need "Advanced" section

### General：
#### Excel：
Choose directory or files as your data source

#### MySQL/Oracle/SQL Server/Hive Connection: 
Input connection information of your target database
#### Mode:

* Overwrite: drop table first(if exists); create table; insert data.

* Append: just insert data into table(table needs exist in the database), according to table name + column name to match, only import data in matched column to the matched table, unmatched column will be ignored 

### Advanced：
#### CSV Encoding：
Tools can auto-detect encoding of csv files(default), and you can choose or input other value.
#### Replace To NULL：
values populated will be replaced to null.
#### Add Table Prefix：
The value populated will be added to table name before.
#### Append all data to one exists table：
Under Append mode, import all data to the table populated.
#### The Column on row：
Set which row as Column name.
#### Skip Blank Rows：
Skip Blank Rows
#### Trim Spaces：
Trim spaces around the data.
#### Skip Blank Sheets：
Ignore sheet if there is no data in it.
#### Add a column is table name：
For imported table, add a column which value is its table name
#### Include Sub Directories
Recursive directories to find all excel files
#### Transform Chinese to First Letter
Transform chinese in table name and column name to the first letter of its pinyin
#### Run sql before starting
When starting import, run sql in the sql file choosed before
#### Run sql after completing
When complete import, run sql in the sql file choosed after


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

## Schedule
C:\Users\ryjfgjl>D:\Projects\ExcelToDatabase4.4\ExcelToDatabase.exe D:\Projects\ExcelToDatabase4.4\config.ini
You can run this command in DOS to start program.
So you can add a scheduled task in windows, D:\Projects\ExcelToDatabase4.4\ExcelToDatabase.exe is our program and D:\Projects\ExcelToDatabase4.4\config.ini is your configuration file.
Note: configuration file can be saved when you manual run ExcelToDatabase, and you can copy it to anywhere and rename it.
eg: D:\config_everyday.ini

