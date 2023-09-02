# ExcelToDatabase: batch import excel into database automatically
![image](https://github.com/ryjfgjl/ExcelToDatabase/assets/39375647/81c5c7ff-0a96-4467-a037-df44ae9859eb)
![image](https://github.com/ryjfgjl/ExcelToDatabase/assets/39375647/8e524554-d714-473f-992a-93f39e6087e6)




## What is it?
**ExcelToDatabase** is an automatical tool which can batch import multiple excel files into database(mysql/oracle/sqlserver/postgresql/access/hive/sqlite/dm). *Automation* is its main feature  beacuse the tool can import data into database automatically and no need you to provide a mapping. *Batch* is the another feature beacuse of automation, so you can import 10 or 10000 excels one time but not one by one. *Scheduler* make you can import excel to database at any time.

## Features
### Automation
  Based on the excel, the tool can create table and import data into the database automatically, or just append/merge the data based on the automatical mapping between the excel and databases.
  
### Batch
  Usually you only can import excel one by one using the other tool. But now, you can import all excels you want one time.

### Easy
  You only need to provide the location of excels and the connect information of database, the tool can work until all the excels are imported

### Fast: 
  The fastest, no others

### Intelligent: 
  When you manually import excel into database, whether if you feel sad when error occurs? DO NOT WORRY! The tool can deal with them!

### Advanced: 
  Rich options could be custom choose to make more fuction come true.

### Schedule: 
  You can make a schedule using it on windows/linux.
  
### Realtime
Sync data in excel into database in realtime.
### Security
DO NOT connect to internet. Work on offline to protect data

## Where to get it

  The packaged executable program(ExcelToDatabase.exe on windows) is available, 
  
  you can download it from [sourceforge](https://sourceforge.net/projects/exceltodatabase/).

<a href="https://sourceforge.net/projects/exceltodatabase/files/latest/download"><img alt="Download ExcelToDatabase" src="https://a.fsdn.com/con/app/sf-download-button" width=276 height=48 srcset="https://a.fsdn.com/con/app/sf-download-button?button_size=2x 2x"></a>


## Usage
**Start Program**
ExcelToDatabase.exe

**Choose and Input**
 
    Choose the directory or excel files; 
    Input target database information; 

**Click Start**

## Supported Environments: 
  * Windows
  * MySQL/Oracle/SQLServer/PostgreSQL/Access/Hive/SQLite/DM
  * Excel(xls,xlsx,xlsm,csv)

## Menu
### Configuration
Open/Save/Import Configuration

### Database
  you can choose one database according to your target database

### Data Source
  * Files: choose Files as your data source, in this case, you can select one or more excel files to import
  * Directory: choose Directory as your data source, in this case, excels under the directory will be imported
### Scheduler
  New/Edit/Import a schedule task.
  Programmer is crontab
  
## Options:

#### Excel：
  Choose directory or files as your data source

#### Database Connection: 
  Input connection information of your target database

### Excel Options：
  #### Recursion of Directories
      Recursive sub directories to find all excel files
  #### Only Import Excel Last Modified
    Only Import Excel Last Modified since last imported
  #### Speeding Read Large Excel
    only supported windows installed office and file format is xlsx/xls
    suggest only open for large excel file)
  #### Encoding of CSV：
    Tools can auto-detect encoding of csv files(default), 
    and you can choose or input other value
  #### Excel Password
    input excel password
  #### Sheet Index or Names
    sheet index as:1,sheet names as:Sheet1,Sheet2
  #### Ignore Sheets Start With
    if @,sheet name starts witj @ will be ignored
  #### The Header on Row
    eg: 1,default is 1,multiple header as: 1-3
  #### The Data Start From Row：
    eg: 2,default is header row+1
  #### Skip Footer Rows
    eg:1
  #### Trim Field Values
    trim()
  #### Skip Blank Lines：
    Skip Blank Rows
  #### Replace Space Character to Null
  #### Replace Values to Null：
    values populated(comma separated) will be replaced to null
  #### Remove Duplicate by Columns
  #### Fill Blank Cell using Last Cell
### Database Options
  #### Drop Table if Exists
    sql:drop table if exists
  #### Truncate Table
    sql:delete from
  #### Create Table if not Exists
    sql:create table if not exists
  #### Append All Data to One Table：
    import all data to the table populated
  #### Case to Append All Data to the Same Table
    Same Sheet Name、Same Excel Name、Similar Excel Name
  #### Use Sheet as Table Name
    defaule use excel file name as table name if not checked
  #### Replace symbol to _ in Indentifier
  
  #### Transform Chinese in Indentifier to The First Letter
    Transform chinese in table name and column name to the first letter of its pinyin
  #### Extract Table Name Using Regexp
  
  #### Add Table Prefix/Suffix：
    The value populated will be added to table name before/after
  #### Add a Key Column, Value is The Row Number：
    Add a Key Column, Value is The Row Number
  #### Excel Name(support regexp) Save to
  #### Allow Increase Column Length When not Enough
    sql:alter table modify column
  #### When excel has redundant column
    Nothing/Ignore redundant column/Add new column in table(sql:alter table add column)
  #### When excel data duplicate with table
    Nothing:sql:insert into
    Ignore:sql:insert ignore into
    Update: sql:delete then insert
  #### Replace Table Data by Columns
    delete table data by value of the columns
  #### Max Connections
    parallel insert
### Other Options
  #### Truncate Logs Before Start
  #### Popout Results when Completed
  #### ODBC Driver
  #### Run Sql Before Starting
    When starting import, run sql in the sql file choosed before
  #### Run Sql After Comleting
    When complete import, run sql in the sql file choosed after

## How the tool works?
  Some logic is described below when the tool work
  ## How to define table name：
    If only one sheet in excel >> excel name
    If multipule sheets in excel >> excel name + '_' + sheet name
    If table name is more than the limit of database >> cut off  
  ### How to define column name：
    Default is the first row, but if the first row is all blank, next row will be used
    If column name is blank, abcd will be set as column name
    If column name is repeated, number like '0' will be added as its suffix
  ### How to define column type：
    Varchar(255) is default. If max length of column more than 255, text/clob will be set.

# Getting Help
  * Email: ryjfgjl@qq.com






