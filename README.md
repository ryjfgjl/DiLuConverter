# ExcelToDatabase: batch import excel into database automatically
![image](https://user-images.githubusercontent.com/39375647/177957033-eff740df-22f4-4ce5-af93-dde3c95187c7.png)

## What is it?
**ExcelToDatabase** is an automatical tool which can batch import multiple excel files into database(mysql/oracle/sqlserver/hive). Automation is its main feature  beacuse the tool can import data into database automatically and no need you to provide a mapping. Batch is the another feature beacuse of automation, so you can import 10 or 10000 excels one time but not one by one.

## Features
### Automation
  Based on the excel, the tool can create table and import data into the database automatically, or just append/merge the data based on the automatical mapping between the excel and databases.
  
### Batch
  Usually you only can import excel one by one using the other tool. But now, you can import all excels you want one time.

### Easy
  You only need to provide the location of excels and the connect information of database, the tool can work until all the excels are imported

### Quick: 
  Batch importting make it faster than manual tool like navicate over the count of your excels times. If you have 10 excels, it is faster 10x

### Intelligent: 
  When you manually import excel into database using tool like navicate, whether if you feel sad when error occurs? Baddly, other error occurs when you just fix one. DO NOT WORRY! The tool can deal with them!

### Advanced: 
  Rich options could be custom choose to make more fuction come true.

### Schedule: 
  You can make a schedule using it on windows/linux.

## Where to get it
  The source code is here.

  The packaged executable program(ExcelToDatabase.exe on windows or ExcelToDatabase on linux) is available, you can download it from https://sourceforge.net/projects/exceltodatabase/.

<a href="https://sourceforge.net/projects/exceltodatabase/files/latest/download"><img alt="Download ExcelToDatabase" src="https://a.fsdn.com/con/app/sf-download-button" width=276 height=48 srcset="https://a.fsdn.com/con/app/sf-download-button?button_size=2x 2x"></a>


## Usage
**Start Program**
* If you hive python environment, you can use command to start:

    `python main.py`

* If you get a packaged executable program:

  On Windows: ExcelToDatabase.exe
  
  On Linux: ./ExcelToDatabase


**Choose and Input**
 
    Choose the directory with excel files; 
    Input target database information; 
    Choose import mode`

**Click Start**

## Supported Environments: 
  * Windows/Linux
  * MySQL/Oracle/SQLServer/Hive
  * Excel(xls,xlsx,xlsm,csv)

## Menu
### Language
  English and Chinese you can choose to display

### Database
  MySQL/Oracle/SQLServer/Hive, you can choose one database according to your target database

### Data Source
  * Directory: choose Directory as your data source, in this case, excels under the directory will be imported
  * Files: choose Files as your data source, in this case, you can select one or more excel files to import

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

* Merge: based on the primary keys on the table, delete then insert.

### Advanced：
  #### Encoding of CSV：
    Tools can auto-detect encoding of csv files(default), 
    and you can choose or input other value
  #### Replace Values to Null：
    values populated(comma separated) will be replaced to null
  #### Add Table Prefix：
    The value populated will be added to table name before
  #### Append All Data to One Exists Table：
    Under Append mode, import all data to the table populated
  #### The Header on Row：
    Set which row as Column name
  #### Skip Blank Lines：
    Skip Blank Rows
  #### Trim Spaces：
    Trim spaces around the data
  #### Skip Blank Sheets：
    Ignore sheet if there is no data in it
  #### Add a Column, Values is The Table Name：
    For imported table, add a column which value is its table name
  #### Recursion of Directories
    Recursive directories to find all excel files
  #### Transform Chinese in Table/Column Name to The First Letter
    Transform chinese in table name and column name to the first letter of its pinyin
  #### Run Sql Before Starting
    When starting import, run sql in the sql file choosed before
  #### Run Sql After Comleting
    When complete import, run sql in the sql file choosed after
  #### Save Current Configuration
    Save Current Configuration
  #### Load Saved Configuration
    Load Saved Configuration

## How the tool works?
  Some logic is described below when the tool work
  ## How to define table name：
    If only one sheet in excel >> excel name
    If multipule sheets in excel >> excel name + '_' + sheet name
    Symbol like ',' will be replaced to '_'
    If table name is more than the limit of database >> cut off  
  ### How to define column name：
    Default is the first row, but if the first row is all blank, next row will be used
    Symbol like ',' will be replaced to '_'
    If column name is blank, 'unnamed' will be set as column name
    If column name is repeated, number like '0' will be added as its suffix
  ### How to define column type：
    Varchar(255) is default. If max length of column more than 255, text/clob will be set.
    
## Correct Error
  ### mysql error 1118：
    utf8mb4 is contained in the data, but the utf8 is the character set of database, 
    mysql error 1118 occured >> import but utf8mb4 character is ignored
  ### mysql error 1366：
    The length of all column is too long or the row size is too large, 
    mysql error 1366 occured >> text will be set as column type
 
## How To Schedule
  The tool can directly run in command line without gui, so you can schedule it on the Windows or Linux. A configuration file(config.ini) is needed to add.
  
  * Python environment:

    Windows: python main.py D:/config.ini
    
    Linux:  python main.py /home/ryjfgjl/config.ini
    
  * Packaged Program:
 
    Windows: ExcelToDatabase.exe D:/config.ini
    
    Linux: ./ExcelToDatabase /home/ryjfgjl/config.ini

# Getting Help
  * Email: 2577154121@qq.com






