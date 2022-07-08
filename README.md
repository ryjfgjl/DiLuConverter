
![image](https://user-images.githubusercontent.com/39375647/174487675-d8d4a23b-df6d-43b0-ac5f-24742b4f4c0b.png)

# ExcelToDatabase: A tool which can batch import multiple excel files into mysql/oracle/sqlserver/hive database automatically.


## Features：
### Easy
  Only need 

### One-Click: 
  Do not need to do anything until all excel files are imported.

### High Speed: 
  Most quickly tools like this around the world.

### Inteligent: 
  When come across some durty data or some difference between Excel and Database, tool can deal with it and go on.

### Advanced Options: 
  Rich options could be custom choose to make more fuction come true.

### Schedule: 
  Can be scheduled.
  
### Free: 
  Most important thing.

## Usage
## Manual Start
1.Start Program

Way 1: Command: python D:\Projects\ExcelToDatabase\main.py

Way 2: Send an email to 2577154121@qq.com, you can get an exe program which can directly run on windows.

2.Input Information

Select directory with excel files; Input target database information; Choose import mode.

3.Click Start.

## Schedule
C:\Users\ryjfgjl>D:\Projects\ExcelToDatabase4.4\ExcelToDatabase.exe D:\Projects\ExcelToDatabase4.4\config.ini
You can run this command in DOS to start program.
So you can add a scheduled task in windows, D:\Projects\ExcelToDatabase4.4\ExcelToDatabase.exe is our program and D:\Projects\ExcelToDatabase4.4\config.ini is your configuration file.
Note: configuration file can be saved when you manual run ExcelToDatabase, and you can copy it to anywhere and rename it.
eg: D:\config_everyday.ini


## Tested Environments: 
Windows 7+, MySQL 5.6+/Oracle 11g+, Excel 1997+(xls,xlsx,xlsm,csv)

## Options Detail:

### General：
#### Excel：
Directory: The excel files under this directory would be imported

#### MySQL/Oracle/SQL Server Connection: 
options to connect to database
#### Mode:

Overwrite: drop table first(if exists); create table; insert data.

Append: just insert data into table(table needs exist in the database)

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
Trim spaces on data.
#### Skip Blank Sheets：
Ignore if no data.
#### Include Sub Directories
Find all excel files under the directory Include Sub Directories

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

