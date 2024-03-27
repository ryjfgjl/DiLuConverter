# Import excel into database automatically-ExcelToDatabase
<img width="959" alt="首页" src="https://github.com/ryjfgjl/ExcelToDatabase/assets/39375647/b7f15080-d4ed-42c4-b9e7-047bcf0c4ed9">


## What is it?
**ExcelToDatabase** is a productivity tool that can automatically import excel into a database. Support excel files in xls/xlsx/xlsm/xlsb/csv/txt format and import into 8 common databases mysql/oracle/sql server/postgresql/access/hive/sqlite/dm. ***Automation*** is its main feature, because it can automatically generate table information based on excel to establish contact with the database, and finally import the data into the database table. ***Batch*** is another feature of it, because it can be automated, so you can import thousands of tables at one time instead of importing them one by one. ***Scheduled*** import and export, real-time refresh, to achieve seamless connection between Excel data and database table data.

## Features
### Automatic
  The tool can automatically generate table names, column names, column types and lengths based on excel, and finally create tables and import data, or automatically match and append or update data based on the generated table information and database tables.
  
### Batch
  Usually you can only use other tools to manually import excel into the database one by one, but now, you can import thousands of tables at once.

### Simple
  Just provide the excel file location and target database connection information, and the tool will start working until all excel is imported.

### Fast
  It takes 3s to import all 10 excel sheets with 10,000 rows x 20 columns x 1MB each. 
  It only takes 3m24s to import a large excel with 1 million rows x 50 columns x 300MB.
  It only takes 5m35s to import a giant csv with 10 million rows x 30 columns x 4GB. 
  and importing a giant excel with 10 sheets totaling 10 million rows x 50 columns x 2GB only takes 31m25s 
  (normal notebook test)

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

## Getting Help
  Email: ryjfgjl.zhang@gmail.com

  Email1: ryjfgjl@qq.com
  
  WeChat: ryjfgjl

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
    Fast engine: faster, but some functions are limited, including: Excel needs to be installed on the computer. 
    It is only effective when the file format is xls/xlsx. It 
    does not support specifying the label of the imported column. 
    This option will lock the excel file and occupy more space. Computer resources, 
    it is recommended to only enable it when the file is large
  #### Recurse Subdirectories
    Traverse all excel files in the selected directory and its subdirectories. 
    This is only valid when the data source selects a folder.
  #### Skip files that have not been updated since the last import
    Record the modification time of each successfully imported excel. The next time you import, 
    only the excel with updated modification time or the newly added excel will be imported.
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
    The default is automatic identification, which means the tool automatically detects. 
    If the encoding of all CSV/TXT files can be determined,
    Can be specified (optional and input) for efficiency. AI recognition has a certain probability of failure.
    If it fails and reports encoding format related issues, 
    please save it as a utf8 encoding format file or save it as xlsx and re-import it.
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
    Custom: Match database tables and fields based on custom files. 
    The template is located in "Field Matching Custom Template.xlsx" in the files directory under the tool directory.

### Data Clean Options
  #### Replace the values of these cells with null
    For common excel error cells or a specific value, enter them separated by commas.
    These cell values will be replaced with null. For example: #NA,null,0, if not filled in, it will not be replaced by default.
  #### Replace these characters with the empty string
    Multiple values are separated by commas, for example: ---, ,(, if not filled in, it will not be replaced by default
  #### Trim Cell Values
    Remove the leading and trailing spaces from the cell value, that is, execute the trim function
  #### Skip Blank Lines
    Delete rows with all blank cells
  #### Deduplicate data by these columns
    Multiple columns are separated by commas, for example: col1, col2. Fill in * to remove duplicates in the entire row. 
    If not filled in, no duplicates will be deleted by default.
  #### Fill the blank cells of these columns with the values from the previous row
    Use the data from the previous row to complete the blank cells of the filled columns. Multiple columns are separated by commas,
    for example: col1,col2
  #### Fill blank cells with field default value
    Fill blank cells with field default value
  #### Fill blank cells of numeric type fields with 0
    Fill blank cells of numeric type fields with 0
  #### Use empty string as null
    Use empty string as null
  #### When excel data and table records are duplicated
    When a primary key or unique index exists in a database table and data duplication occurs:
    Ignore excel data based on unique key of database table: Append mode applies
    Update excel table records based on unique key of database table: update mode applies
    Replace database table records based on specified column: Manually specify fields, 
    no need to set unique keys in the database table, and separate multiple columns with commas.
  ### Database Options
  #### Table Naming Rule
    Auto: when there is only one sheet, use the Excel file name as the table name; 
    when there are multiple sheets, use the Excel file name + Sheet name as the table name
    Use Excel file name + Sheet name: Use Excel file name + Sheet name as table name
    Only Use Excel Name: Use only Excel file name as table name
    Only Use Sheet Name: Use only Sheet name as table name
  #### Regularly Extract Table Name
    Use regular expressions to extract the table name from the excel file name. 
    If not filled in, the default is the original excel file name.
  #### Replace the symbols in the table name with _
    Replace all symbols in the table name (colons, quotes, etc.) with underscores_,
    If there are special symbols in the excel name, check this option to avoid import failure.
  #### Add prefix to table name
    Add prefix to table name
  #### Add suffix to table name
    Add suffix to table name
  #### Table Name Case
    Origin: stay as is
    Upper: Use uppercase characters
    Lower: Use lowercase characters
  #### When the generated table names are repeated, regard as
    Different Table
    Same Table
  #### Replace the symbols in the field name with _
    Replace the symbols (colon quotes, etc.) in the field name with underscore_,
    If there are special symbols in the field, check this option to avoid import failure.
  #### Field Name Case
    Origin: stay as is
    Upper: Use uppercase characters
    Lower: Use lowercase characters
  #### Add an auto-increment field when creating a table
    Add a column to the database table when creating the table. 
    This column will store the automatically growing number and serve as the primary key of the table.
  #### Save import time to field
    Save the import time to the filled in column
  #### Save the excel file name (supports regular extraction) to the field
    Save the excel file name to the filled-in column. 
    You can apply a regular expression to the excel file name to extract it and then use it as a column value.
  #### Field Data Type
    All Use Character Types: use varchar/nvarchar as data types
    Automatically Recognize Date and Numeric Types: only valid for xls/xlsx/xlsm/xlsb
  #### When there are extra columns in excel
    Nothing: do nothing
    Ignore Extra Column: only import matching column data
    Add a New Field in the Table: Add a new column to the database table and perform the alter table add column operation.
  #### Automatically extend the field length when it is not long enoug
    Automatically extend the field length when it is not long enoug
  #### Insert Way
    Fast: fast
    Load: fast, suitable for large files and the database is mysql/hive, where hive needs to fill in the server login information in other options
    Bcp: fast, suitable for large files and sql server, the computer needs to have the bcp tool installed (CMD command line input: bcp)
    Sqlldr: fast, suitable for large files and Oracle, requires the computer to have installed the sqlldr tool adapted to the database (CMD command line input: sqlldr)
    Parallel: Fast, 5 connections are enabled for parallel writing by default, suitable for large files
    General: Slower, good for small to medium files, and able to print and skip written lines with errors
  #### Commit Way
    Once Commit: One-time submission after data writing is completed. Failure can be rolled back.
    Batch Commit: Submit every 1000 rows
    Auto Commit: auto-submit

### Other Options
  #### Truncate Logs Before Start
  #### Run Sql Before Starting
    When starting import, run sql in the sql file choosed before
  #### Run Sql After Comleting
    When complete import, run sql in the sql file choosed after
  #### Run Query After Comleting Export to


