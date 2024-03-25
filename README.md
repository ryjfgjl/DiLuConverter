# ExcelToDatabase: Automatically import excel into database
<img width="960" alt="首页" src="https://github.com/ryjfgjl/ExcelToDatabase/assets/39375647/65225342-90d3-4fd8-8afc-a86b1c2712de">




## What is it?
**ExcelToDatabase** is an automated tool that can batch import excel (xls/xlsx/xlsm/xlsb/csv/txt) into the database (mysql/oracle/sql server/postgresql/access/hive/sqlite/dm). ***Automation*** is its main feature, because it can automatically generate table information based on excel to establish contact with the database, and finally import the data into the database table. ***Batch*** is another feature of it, because it can be automated, so you can import thousands of tables at one time instead of importing them one by one. ***Scheduled*** import and export, real-time refresh, to achieve seamless connection between Excel data and database table data.

## Features
### Automatic
  The tool can automatically generate table names, column names, column types and lengths based on excel, and finally create tables and import data, or automatically match and append or update data based on the generated table information and database tables.
  
### Batch
  Usually you can only use other tools to manually import excel into the database one by one, but now, you can import thousands of tables at once.

### Simple
  Just provide the excel file location and target database connection information, and the tool will start working until all excel is imported.

### Fast: 
  It takes 1 minute and 46 seconds to import all 100 excel sheets with 10,000 rows x 20 columns x 1MB each. It only takes 3 minutes and 24 seconds to import a large excel with 1 million rows x 50 columns x 300MB. It only takes 3 minutes and 24 seconds to import a giant excel with 10 million rows x 30 columns x 4GB. csv only takes 5 minutes and 35 seconds, and importing a giant excel with 10 sheets totaling 10 million rows x 50 columns x 2GB only takes 31 minutes and 25 seconds (ordinary notebook test)

### Smart: 
  Do you often encounter errors when importing manually? do not worry! Tools can easily avoid or automatically correct them.

### Timing: 
  You can use the built-in scheduled task function or combine it with other scheduled task programs to achieve scheduled import.

### Real-time: 
  Using scheduled tasks, when excel data is updated, it can be updated synchronously to the database in real-time.
  
### Security
  The software is green and requires no installation, and can work under any network conditions.


## Supported Environment: 
  * Windows
  * MySQL/Oracle/SQLServer/PostgreSQL/Access/Hive/SQLite/DM
  * Excel(xls,xlsx,xlsm,,xlsb,csv,txt)

## Where to get it

  The packaged executable program(ExcelToDatabase.exe on windows) is available, 
  
  you can download it from [sourceforge](https://sourceforge.net/projects/exceltodatabase/).

<a href="https://sourceforge.net/projects/exceltodatabase/files/latest/download"><img alt="Download ExcelToDatabase" src="https://a.fsdn.com/con/app/sf-download-button" width=276 height=48 srcset="https://a.fsdn.com/con/app/sf-download-button?button_size=2x 2x"></a>
    
## Usage

1. Click ExcelToDatabase.exe to start the program
2. Create a new database connection
3. Create a new configuration after the database connection is successful.
4. Select the Excel to be imported, the target table and the import mode (required)
5. Adjust advanced options as needed (optional)
6. Click Start

## API
The tool provides API capabilities that can be called by other applications for background import without a graphical interface.
For example: ExcelToDatabase.exe Test connection 1 Test configuration 1
Command: ExcelToDatabase.exe
Parameter 1: Test connection 1--connection name
Parameter 2: Test configuration 1--configuration name
  
## Left Options Introduction:

### Excel：
  Select the excel directory or file that needs to be imported.

  Select files: Select one or more excel files, the selected files will be imported
  
  Select directory: Select a folder, and all excel files under this folder will be imported.

### Target table: 
  Auto Generate: The tool automatically generates the table name through the excel file name and sheet name.

  Input or Select: select or enter a table name

### Mode：
  Append: Add records to the target table
  
  Update: Delete the same records in the target table and re-import the data from Excel
  
  Overwrite: Delete all records in the target table and re-import the data from Excel
  
  Rebuild: Delete the target table and re-import the data from Excel
  
## Right Options Introduction:
### Excel options:
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






