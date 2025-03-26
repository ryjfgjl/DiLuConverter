#                                                                           DiLu Converter
This is the official documentation for [DiLu Converter](https://www.diluauto.com/en/).

![dilu-converter](https://github.com/user-attachments/assets/17c14a26-7c18-4897-a2d8-3f95b9a034c3)



## What is it?
**DiLu Converter** is a powerful Excel import and export tool that supports more than 10 databases such as MySQL, Oracle, SQL Server, PostgreSQL and so on.
The supported file formats include xls, xlsx, xlsm, xlsb, csv, txt, xml, json, and dbf. Its native user interface brings users a comfortable experience of simplified Excel import and export, making Excel import and export easier than ever before.
Whether you want one-click, batch, and personalized import and export, or want to use scheduled tasks to achieve unattended full automation, DiLu Converter can bring you unprecedented productivity improvement.

## Features
### Safe
  The software has passed sourceforge and google virus detection and it works offline on a single machine to ensure data security.
  
### Fast
  The fastest import and export software.

### Powerful
  Supports importing Excel files of any shape into many popular databases

### Credible
  Verified by thousands of users, with numerous positive reviews. Applied to the production environment of large-scale enterprises, as stable as an old horse

### Automatic
  It allows you to import and export in one step, in batch , in scheduled and in realtime.

### Easy to use
  Both beginners and experts can benefit greatly from this.


## Supported Environment: 
  * Windows/MacOS/Linux
  * MySQL/Oracle/SQLServer/PostgreSQL/IBM DB2/Access/Hive/SQLite/DM/DuckDB
  * Excel(xls,xlsx,xlsm,xlsb,csv,txt,xml)

## Where to get it

  [DiLu Converter Official Website)](https://www.diluauto.com/en/)

## Getting Help

  Email1: 2577154121@qq.com

  Email2: ryjfgjl.zhang@gmail.com

    
## Usage

1. Click DiLuConverter.exe to start the program
2. Create a new database connection
3. Create a new configuration after the database connection is successful.
4. Select the Excel to be imported, the target table and the import mode (required)
5. Adjust advanced options as needed (optional)
6. Click Start

## API
The tool provides API capabilities that can be called by other applications for background import without a graphical interface.

For example: DiLuConverter.exe import/export/sync/job "Test connection 1" "Test configuration 1"

Command: DiLuConverter.exe

Parameter 1: import/export/sync/job--execute type

Parameter 2: Test connection 1--connection name

Parameter 3: Test configuration 1--configuration name

## Tutorial
1: [New Database Connection Guide](https://github.com/ryjfgjl/ExcelToDatabase/wiki/Database-Connection-Guide)

2: [One-click Importing Excel Data into a Database](https://dev.to/ryjfgjl/one-click-importing-excel-data-into-a-database-2j02)

3: [Importing Multiple Excel Files into a Database in Batch](https://dev.to/ryjfgjl/batch-import-of-multiple-excel-files-into-the-database-45ac)

4: [Merging Data from Multiple Excel Files](https://dev.to/ryjfgjl/merging-data-from-multiple-excel-files-4g2h)

5: [Scheduled Import of Excel into Database](https://dev.to/ryjfgjl/scheduled-import-of-excel-into-database-4pcd)

6: [Real-time Synchronization and Refresh of Excel Data to Database](https://dev.to/ryjfgjl/synchronize-and-refresh-excel-data-to-the-database-in-real-time-2fe2)


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


