# ExcelToMySQL
## 简介：一个实现自动化导入excel文件到mysql数据库的工具
## 工具截图：
![image](https://user-images.githubusercontent.com/39375647/132945877-aa80684a-5212-4e82-bab9-714f4d3b1bd1.png)

## 使用方法：
常规界面选择excel文件目录，填入目标数据库，选择导入模式，点击开始即可导入目录下所有excel文件。
## 工具特色：
高速自动化，一键式，无人值守，自动纠错，高级功能可选

## 主要Python包:
PySimpleGUI
numpy
pandas
pymysql
chardet

## 详细介绍:
如果电脑上有python环境，可以运行如下命令启动：

python E:\Python\Project\python-excelimporter\interface.py

也可以通过Cx-Freeze打包成exe文件：

cmd: cd E:\Python\Project\python-excelimporter

python E:\Python\Project\python-excelimporter\setup.py build.

如果没有python环境，可以联系2577154121@qq.com，获取exe文件可以直接运行。

## 选项介绍:

### 常规：
#### Excel文件：
所在文件夹：选择要导入的excel文件所在目录，该目录下所有的excel文件（包括xls、xlsx和csv格式）都将被导入

#### MySQL连接: 
填入要导入的目标数据库连接信息
   主机: 
   端口:  
   用户: 
   密码: 
   数据库:
#### 模式:

覆盖模式下，在导入一张表前，工具将先删除同名的表，在创建并导入数据。

追加模式下，工具将直接将数据导入到同名的表

### 高级：
#### CSV文件编码：
因为csv格式没有记录文件编码，所以我们不能确定其编码格式
如果选择自动，工具将自动猜测其编码格式，如果选择或者填写特定的编码格式，工具将先使用用户提供的编码解码，如果失败，再尝试用常见编码格式解码，如果失败再通过猜测其编码格式
如何确定csv文件的编码，可以参考下面文章
http://pandaproject.net/docs/determining-the-encoding-of-a-csv-file.html
   
#### 将这些值替换为null：
对于常见的excel错误单元格或者某特定的值，填入以逗号分隔，将被替换为null
#### 为创建的表名添加前缀：
可以为工具创建的表名指定前缀，以示区分
#### 删除空行：
如选择，工具将删除所有空行
#### 去除字符前后空格：
若选择，工具将去除字符前后空格
#### 跳过空表：
若选择，如果表格没有数据，工具将不会创建数据库表
  
### 其他：
  #### 表名的确定：
  使用文件名并小写，将非文字字符替换为_。如果一个excel文件包含多个sheet，将采用文件名+_+sheet名。如果表名超过64个字节，自动截断并再前面加上计数如0_表名
  #### 列名的确定：
  使用第一行作为列名，如果列名全为空，将用下一个非空行作为列名，如果存在列名为空，将用unnamed+计数作为列名，如果列名超过64个字节，自动截断。列名将去除前后空格并将%替换为_
  #### 列类型的确定：
  工具将计算每列最大长度，如果小于255，将使用varchar(255)，如果大于255，将使用text。
  #### 常见错误1366：
  如果excel文件包含表情等utf8mb4编码的字符，在utf8编码的表中，如果sql_mode为STRICT_TRANS_TABLES，会报1366错误。工具将暂时设置sql_mode=''，导入会设回默认值
  #### 常见错误1118：
  对于一行数据的总长度，mysql限制为65535，如果超长，将报1118错误。工具将全部列类型替换为text（text类型一列只占1个字节长度）
  
# 作者: ryjfgjl
# 如需帮助，请联系2577154121@qq.com

