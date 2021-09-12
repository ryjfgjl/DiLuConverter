#######################################################################################################################
# 工具名称：ExcelToMySQL
# 版本号：V3.0
# 工具简介：将excel文件导入到mysql数据库的自动化工具
# 工具特色：一键式，无人值守，批量导入
# 适用环境：Windows 7及以上，MySQL 5.6及以上，Excel 1997及以上（xls，xlsx和csv格式）
# 作者：ryjfgjl
# 更新日期：2021-09-01
# 更新内容：
# 1、代码注释及界面采用中文，更适合中国用户
# 2、优化主界面，增加高级选项配置功能，让更多高级功能可见可选可配置
#######################################################################################################################

##############################################################
# 主程序UI入口
##############################################################

# 程序版本号
Version = "3.0"

# 导入GUI及错误捕获包
import PySimpleGUI as sg
import traceback
import sys
# 导入自定义读写配置文件包
from common.handleconfig import HandleConfig

# 初始化UI界面风格
sg.ChangeLookAndFeel('dark')

HandleConfig = HandleConfig()

# 获取配置文件保存的数据库连接信息
host = HandleConfig.handle_config("g", "dbinfo", "host")
port = HandleConfig.handle_config("g", "dbinfo", "port")
user = HandleConfig.handle_config("g", "dbinfo", "user")
passwd = HandleConfig.handle_config("g", "dbinfo", "passwd")
dbname = HandleConfig.handle_config("g", "dbinfo", "dbname")
# 获取配置文件保存的文件信息
file_dir = HandleConfig.handle_config("g", "file", "file_dir")
csv_encoding = HandleConfig.handle_config("g", "file", "csv_encoding")
na_values = HandleConfig.handle_config("g", "file", "na_values")
mode = HandleConfig.handle_config("g", "advanced", 'mode')
prefix = HandleConfig.handle_config("g", "advanced", 'prefix')
del_blank_lines = eval(HandleConfig.handle_config("g", "advanced", 'del_blank_lines'))
trim = eval(HandleConfig.handle_config("g", "advanced", 'trim'))
skip_blank_sheet = eval(HandleConfig.handle_config("g", "advanced", 'skip_blank_sheet'))

def default_mode(_mode):
    if _mode == mode:
        return True
    else:
        return False

# 异常信息格式化函数
def exception_format():
    return "".join(traceback.format_exception(
        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    ))


# UI界面生成函数
def generate_layout():
    # 常规界面
    layout_general = [
        [sg.Text('Excel文件', size=(12, 1), text_color='red')],
            [sg.Text('所在文件夹:', size=(12, 1)), sg.Input('{}'.format(file_dir), key='file_dir', size=(35, 1)),
             sg.FolderBrowse(initial_folder='{}'.format(file_dir), button_text=' 选择 ')],
        [sg.Text('MySQL连接', size=(12, 1), text_color='red')],

        [sg.Text('主机:', size=(5, 1)), sg.Input('{}'.format(host), key='host', size=(15, 1)), sg.Text(' ' * 11),
             sg.Text('端口:', size=(7, 1)), sg.Input('{}'.format(port), key='port', size=(15, 1)), ],
            [sg.Text('用户:', size=(5, 1)), sg.Input('{}'.format(user), key='user', size=(15, 1)), sg.Text(' ' * 11),
             sg.Text('密码:', size=(7, 1)), sg.Input('{}'.format(passwd), key='passwd', size=(15, 1)), ],
            [sg.Text('数据库:', size=(5, 1)), sg.Input('{}'.format(dbname), key='dbname', size=(21, 1)), sg.Text(' ' * 1),
             sg.Text('模式:', text_color='red'),
             sg.Text(' ' * 1),
              sg.Radio('覆盖', group_id='mode', key='mode1', default=default_mode('mode1')),
              sg.Radio('追加', group_id='mode', key='mode2', default=default_mode('mode2')),
             ],

        [sg.Button('开始', size=(52, 1))]
    ]
    # 高级界面
    layout_advanced = [
        [sg.Text('CSV文件编码:', size=(12, 1)),
            sg.Combo(['自动', 'UTF-8', 'ANSI', 'GBK'], default_value=csv_encoding, key='csv_encoding', size=(10, 1))],
        [sg.Text('将这些值替换为null:', size=(15, 1)),sg.Input('{}'.format(na_values), key='na_values', size=(40, 1)), ],
        [sg.Text('为创建的表名添加前缀:', size=(17, 1)), sg.Input(prefix, key='prefix', size=(20, 1),), ],
        [sg.Checkbox('删除空行', key='del_blank_lines', size=(20, 1), default=del_blank_lines), ],
        [sg.Checkbox('去除字符前后控格', key='trim', size=(20, 1), default=trim), ],
        [sg.Checkbox('跳过空表', key='skip_blank_sheet', size=(20, 1), default=skip_blank_sheet), ],
        [sg.Button('开始', size=(52, 1))]
    ]

    tab_layouts = [sg.Tab('常规', layout_general), sg.Tab('高级', layout_advanced)]

    layout = [
        [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
    ]
    return layout


# 生成程序界面
window = sg.Window('ExcelToMySQL {0}'.format(Version), generate_layout(), location=(700, 100))

# 保持程序持续运行，直至点击 X 关闭程序
while True:
    try:
        event, values = window.read()
        # 点击开始，进入excel导入程序
        if event == "开始" or event == '开始0':
            from events.excelimporter import ImportExcel
            ImportExcel = ImportExcel()
            # 将用户选择传递进excel导入主程序
            ImportExcel.main(values)
        elif event == sg.WIN_CLOSED:
            break
    except:
        # 打印异常，而不退出
        sg.PopupError(exception_format())
