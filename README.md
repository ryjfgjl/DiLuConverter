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

### Fast
  It takes 1 minute and 46 seconds to import all 100 excel sheets with 10,000 rows x 20 columns x 1MB each. It only takes 3 minutes and 24 seconds to import a large excel with 1 million rows x 50 columns x 300MB. It only takes 3 minutes and 24 seconds to import a giant excel with 10 million rows x 30 columns x 4GB. csv only takes 5 minutes and 35 seconds, and importing a giant excel with 10 sheets totaling 10 million rows x 50 columns x 2GB only takes 31 minutes and 25 seconds (ordinary notebook test)

### Smart
  Do you often encounter errors when importing manually? do not worry! Tools can easily avoid or automatically correct them.

### Timing
  You can use the built-in scheduled task function or combine it with other scheduled task programs to achieve scheduled import.

### Real-time
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

For example: ExcelToDatabase.exe "Test connection 1" "Test configuration 1"

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
  #### Read Engine
    Default engine: supports all options
    Fast engine: faster, but some functions are limited, including: Excel needs to be installed on the computer. It is only effective when the file format is xls/xlsx. It does not support specifying the label of the imported column. This option will lock the excel file and occupy more space. Computer resources, it is recommended to only enable it when the file is large
  #### Recurse Subdirectories
    Traverse all excel files in the selected directory and its subdirectories. This is only valid when the data source selects a folder.
  #### Skip files that have not been updated since the last import
    Record the modification time of each successfully imported excel. The next time you import, only the excel with updated modification time or the newly added excel will be imported.
(Invalid after the data source folder is changed)
  #### Select the Sheet's
    Name: For example: Sheet1,Sheet2
    Index: 1,2
    Multiple sheets are separated by commas. If not filled in, all will be imported by default.
  #### Select the Header's
    Name: name,age,birthday
    Index: 1,2,3
    Label: A:C
    If left blank, all columns will be imported by default. CSV/TXT does not support labels.
  #### Field Name Row
    Specify which row to use as the column name. The first row starts from 1. If left blank, it defaults to 1.
    Supports multi-level headers, example: 1-3
    You can fill in 0, which means the data starts from the first row, and the column names are A, B, and C. . . name,
  #### First Data Row
    The number of data starting rows. If not filled in, the default is the number of rows in the header + 1
  #### Import Rows
    Specify the number of rows to import, default is all rows
  #### Skip Footer Rows
    The number of lines to skip at the end of the file. If left blank, the default value is 0.
Note: This option and the number of rows to be imported are mutually exclusive.
  #### Encoding
    The default is automatic identification, which means the tool automatically detects. If the encoding of all CSV/TXT files can be determined,
Can be specified (optional and input) for efficiency. AI recognition has a certain probability of failure.
If it fails and reports encoding format related issues, please save it as a utf8 encoding format file or save it as xlsx and re-import it.
  #### Delimiter
    Specify the column delimiter of the csv file, the default is comma,
  #### Lineterminator
    Specify the line separator of the csv file, the default is \n
  #### Chunck Size
    Import large csv/txt files in batches to avoid insufficient memory, such as 100000
  #### Password of Excel
    Enter the password to encrypt excel
  #### Field Mapping
    Specify field matching rules:
By Name: Match database table fields based on excel header names
By Index: Match database table fields according to excel header order
Custom: Match database tables and fields based on custom files. The template is located in "Field Matching Custom Template.xlsx" in the files directory under the tool directory.

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






