##############################################################
# Program GUI
# including English and Chinese
##############################################################

import PySimpleGUI as sg
from common.handleconfig import HandleConfig

sg.ChangeLookAndFeel('dark')


class Gui:
    def __init__(self):
        self.HandleConfig = HandleConfig()

    def ret_bool(self, source):
        if source == 'D':
            return True
        else:
            return False

    def generate_layout(self):
        default_values = self.HandleConfig.get_defaults()
        if default_values['language'] == 'English':
            # English gui
            # menu
            menu_def = [
                ['&Language', ['&中文', '&English']],
                ['&Database', ['&MySQL', '&Oracle', '&SQL Server']],
                ['&Data Source', ['&Directory', '&Files']],
                ['&Help', ['&About']],
            ]
            # general
            layout_general = [
                [sg.Menu(menu_def)],
                [sg.Text('Excel', size=(12, 1), text_color='red')],
                [
                    sg.Input('{}'.format(default_values['file_dir']), key='file_dir', size=(42, 1),
                             visible=self.ret_bool(default_values['source'])),
                    sg.FolderBrowse(initial_folder='{}'.format(default_values['file_dir']), button_text='Choose Directory',
                                    visible=self.ret_bool(default_values['source'])),
                    sg.Input('{}'.format(default_values['files']), key='files', size=(45, 1),
                             visible=not self.ret_bool(default_values['source'])),
                    sg.FilesBrowse(button_text='Choose Files',
                                   visible=not self.ret_bool(default_values['source'])),
                ],
                [sg.Text('{}'.format(default_values['dbtype']),  text_color='red', key='dbtype'),
                 sg.Text('Connection', text_color='red'),
                 ],

                [sg.Text('Host:', size=(5, 1)), sg.Input('{}'.format(default_values['host']), key='host', size=(15, 1)),
                 sg.Text(' ' * 11),
                 sg.Text('Port:', size=(7, 1)),
                 sg.Input('{}'.format(default_values['port']), key='port', size=(15, 1)), ],
                [sg.Text('User:', size=(5, 1)), sg.Input('{}'.format(default_values['user']), key='user', size=(15, 1)),
                 sg.Text(' ' * 11),
                 sg.Text('Password:', size=(7, 1)),
                 sg.Input('{}'.format(default_values['passwd']), key='passwd', size=(15, 1)), ],
                [

                    sg.Text('Database:', size=(7, 1)),
                    sg.Input('{}'.format(default_values['dbname']), key='dbname', size=(48, 1)), sg.Text(' ' * 1),

                ],
                [sg.Text('Mode:', text_color='red'),
                     sg.Text(' ' * 10),
                    sg.Radio('Overwrite', group_id='mode', key='mode1',
                             default=default_values['mode1']),
                 sg.Text(' ' * 10),
                    sg.Radio('Append', group_id='mode', key='mode2',
                             default=default_values['mode2']),],

                [sg.Button('Start', size=(52, 1), key='start')],
                [sg.MLine(key='output', size=(58, 10), auto_refresh=True)],
            ]
            # advanced
            layout_advanced = [
                [sg.Text('CSV Encoding:', size=(12, 1)),
                 sg.Combo(['AUTO', 'UTF-8', 'ANSI', 'GBK'], default_value=default_values['csv_encoding'],
                          key='csv_encoding', size=(10, 1))],
                [sg.Text('Replace To NULL:', size=(15, 1)),
                 sg.Input('{}'.format(default_values['na_values']), key='na_values', size=(40, 1)), ],
                [sg.Text('Append all data to one exists table:', size=(25, 1)),
                 sg.Input(default_values['tname'], key='tname', size=(25, 1), ), ],
                [sg.Text('Add Table Prefix:', size=(13, 1)),
                 sg.Input(default_values['prefix'], key='prefix', size=(10, 1), ),
                 sg.Checkbox('Add a column is table name', key='add_tname', size=(22, 1), default=default_values['add_tname']),],

                [sg.Text('The column on row:', size=(15, 1)),
                 sg.Input(default_values['header'], key='header', size=(10, 1)),
                 sg.Text('', size=(3, 1)),
                 sg.Checkbox('Include Sub Directories', key='loop_subdir', size=(18, 1), default=default_values['loop_subdir']),],
                [sg.Checkbox('Skip Blank Rows', key='del_blank_lines', size=(15, 1),
                             default=default_values['del_blank_lines']),
                 sg.Checkbox('Trim Spaces', key='trim', size=(12, 1), default=default_values['trim']),
                 sg.Checkbox('Skip Blank Sheets', key='skip_blank_sheet', size=(12, 1),
                             default=default_values['skip_blank_sheet']),

                 ],
                [sg.Text('Run sql before starting:', size=(17, 1)),
                 sg.Input('{}'.format(default_values['sql_b4']), key='sql_b4', size=(32, 1)),
                 sg.FileBrowse(initial_folder='{}'.format(default_values['sql_b4']), button_text=' 选择 ')],
                [sg.Text('Run sql after comleting:', size=(17, 1)),
                 sg.Input('{}'.format(default_values['sql_after']), key='sql_after', size=(32, 1)),
                 sg.FileBrowse(initial_folder='{}'.format(default_values['sql_after']), button_text=' 选择 ')],
            ]

            tab_layouts = [sg.Tab('General', layout_general), sg.Tab('Advanced', layout_advanced)]

            layout = [
                [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
            ]
        else:
            # menu
            menu_def = [
                ['&语言', ['&中文', '&English']],
                ['&数据库', ['&MySQL', '&Oracle', '&SQL Server']],
                ['&数据源', ['&选择目录', '&选择文件']],
                ['&帮助', ['&关于']],
            ]
            # general
            layout_general = [
                [sg.Menu(menu_def)],
                [sg.Text('Excel 文件', size=(12, 1), text_color='red')],
                [
                 sg.Input('{}'.format(default_values['file_dir']), key='file_dir', size=(50, 1), visible=self.ret_bool(default_values['source'])),
                 sg.FolderBrowse(initial_folder='{}'.format(default_values['file_dir']), button_text='选择目录', visible=self.ret_bool(default_values['source'])),
                 sg.Input('{}'.format(default_values['files']), key='files', size=(50, 1), visible=not self.ret_bool(default_values['source'])),
                 sg.FilesBrowse(button_text='选择文件', visible=not self.ret_bool(default_values['source'])),
                 ],
                [sg.Text('{}'.format(default_values['dbtype']), text_color='red', key='dbtype'),
                 sg.Text('连接', text_color='red'),
                 ],

                [sg.Text('主机:', size=(5, 1)), sg.Input('{}'.format(default_values['host']), key='host', size=(15, 1)),
                 sg.Text(' ' * 11),
                 sg.Text('端口:', size=(7, 1)),
                 sg.Input('{}'.format(default_values['port']), key='port', size=(15, 1)), ],
                [sg.Text('用户:', size=(5, 1)), sg.Input('{}'.format(default_values['user']), key='user', size=(15, 1)),
                 sg.Text(' ' * 11),
                 sg.Text('密码:', size=(7, 1)),
                 sg.Input('{}'.format(default_values['passwd']), key='passwd', size=(15, 1)), ],
                [

                    sg.Text('数据库:', size=(5, 1)),
                    sg.Input('{}'.format(default_values['dbname']), key='dbname', size=(50, 1)), sg.Text(' ' * 1),

                ],
                [
                    sg.Text('模   式:', text_color='red'),
                    sg.Text(' ' * 6),
                    sg.Radio('覆   盖', group_id='mode', key='mode1', default=default_values['mode1']),
                    sg.Text(' ' * 15),
                    sg.Radio('追   加', group_id='mode', key='mode2', default=default_values['mode2']),
                ],
                [sg.Button('开     始', size=(52, 1), key='start')],
                [sg.MLine(key='output', size=(58, 10), auto_refresh=True)],
            ]
            # advanced
            layout_advanced = [
                [sg.Text('CSV文件编码:', size=(12, 1)),
                 sg.Combo(['AUTO', 'UTF-8', 'ANSI', 'GBK'], default_value=default_values['csv_encoding'],
                          key='csv_encoding', size=(10, 1))],
                [sg.Text('将这些值替换为null:', size=(15, 1)),
                 sg.Input('{}'.format(default_values['na_values']), key='na_values', size=(40, 1)), ],
                [sg.Text('为创建的表名添加前缀:', size=(18, 1)),
                 sg.Input(default_values['prefix'], key='prefix', size=(20, 1), ), ],
                [sg.Text('将数据追加到已存在的表（追加模式有效）:', size=(34, 1)),
                 sg.Input(default_values['tname'], key='tname', size=(20, 1), ), ],
                [sg.Text('指定列名所在行数:', size=(18, 1)), sg.Input(default_values['header'], key='header', size=(10, 1)),
                 sg.Checkbox('添加一列值为表名', key='add_tname', size=(15, 1), default=default_values['add_tname']),
                 ],
                [sg.Checkbox('删除空行', key='del_blank_lines', size=(7, 1), default=default_values['del_blank_lines']),
                 sg.Checkbox('去除字符前后空格', key='trim', size=(14, 1), default=default_values['trim']),
                 sg.Checkbox('跳过空表', key='skip_blank_sheet', size=(6, 1), default=default_values['skip_blank_sheet']),
                 sg.Checkbox('遍历子目录', key='loop_subdir', size=(9, 1), default=default_values['loop_subdir']),
                 ],
                [sg.Text('导入开始前运行sql:', size=(15, 1)),
                 sg.Input('{}'.format(default_values['sql_b4']), key='sql_b4', size=(32, 1)),
                 sg.FileBrowse(initial_folder='{}'.format(default_values['sql_b4']), button_text=' 选择 ')],
                [sg.Text('导入结束后运行sql:', size=(15, 1)),
                 sg.Input('{}'.format(default_values['sql_after']), key='sql_after', size=(32, 1)),
                 sg.FileBrowse(initial_folder='{}'.format(default_values['sql_after']), button_text=' 选择 ')],

            ]

            tab_layouts = [sg.Tab('常规', layout_general), sg.Tab('高级', layout_advanced)]

            layout = [
                [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
            ]
        return layout



