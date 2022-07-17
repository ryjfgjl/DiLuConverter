##############################################################
# Program GUI
# including English and Chinese
##############################################################

import PySimpleGUI as sg

sg.ChangeLookAndFeel('dark')


class Gui:

    def generate_layout(self, values):
        if values['language'] == 'English':
            # English gui
            # menu
            menu_def = [
                ['&Language', ['&中文', '&English']],
                ['&Database', ['&MySQL', '&Oracle', '&SQL Server', '&Hive']],
                ['&Data Source', ['&Directory', '&Files']],
                ['&Help', ['&About']],
            ]
            # general
            layout_general = [
                # menu
                [sg.Menu(menu_def)],
                # file
                [sg.Text('Excel', size=(12, 1), text_color='red')],
                [
                    sg.Input('{}'.format(values['file_dir']), key='file_dir', size=(42, 1),
                             visible=self.ret_bool('source', values['source'])),
                    sg.FolderBrowse(initial_folder='{}'.format(values['file_dir']), button_text='Choose Directory',
                                    visible=self.ret_bool('source', values['source'])),
                    sg.Input('{}'.format(values['files']), key='files', size=(45, 1),
                             visible=not self.ret_bool('source', values['source'])),
                    sg.FilesBrowse(button_text='Choose Files',
                                   visible=not self.ret_bool('source', values['source'])),
                ],
                # dbinfo
                [sg.Text('{}'.format(values['dbtype']),  text_color='red', key='dbtype'),
                 sg.Text('Connection', text_color='red'),
                 ],
                [sg.Text('Host:', size=(5, 1)), sg.Input('{}'.format(values['host']), key='host', size=(15, 1)),
                 sg.Text(' ' * 11),
                 sg.Text('Port:', size=(7, 1)),
                 sg.Input('{}'.format(values['port']), key='port', size=(15, 1)), ],
                [sg.Text('User:', size=(5, 1)), sg.Input('{}'.format(values['user']), key='user', size=(15, 1)),
                 sg.Text(' ' * 11),
                 sg.Text('Password:', size=(7, 1)),
                 sg.Input('{}'.format(values['passwd']), key='passwd', size=(15, 1)), ],
                [sg.Text('Database:', size=(7, 1)),
                 sg.Input('{}'.format(values['dbname']), key='dbname', size=(48, 1)), sg.Text(' ' * 1),
                ],
                # mode
                [sg.Text('Mode:', text_color='red'),
                     sg.Text(' ' * 10),
                    sg.Radio('Overwrite', group_id='mode', key='mode1',
                             default=self.ret_bool('mode', values['mode'])),
                 sg.Text(' ' * 10),
                    sg.Radio('Append', group_id='mode', key='mode2',
                             default=not self.ret_bool('mode', values['mode'])),],

                [sg.Button('Start', size=(52, 1), key='start')],
                [sg.MLine(key='output', size=(58, 10), auto_refresh=True)],
            ]
            # advanced
            layout_advanced = [
                [sg.Text('Encoding of CSV:', size=(12, 1)),
                 sg.Combo(['AUTO', 'UTF-8', 'ANSI', 'GBK'], default_value=values['csv_encoding'],
                          key='csv_encoding', size=(10, 1))],
                [sg.Text('Replace Values to Null:', size=(17, 1)),
                 sg.Input('{}'.format(values['na_values']), key='na_values', size=(26, 1)), ],

                [sg.Text('Add Table Prefix:', size=(13, 1)),
                 sg.Input(values['prefix'], key='prefix', size=(10, 1), ), ],
                [sg.Text('Append All Data to One Exists Table:', size=(27, 1)),
                 sg.Input(values['tname'], key='tname', size=(25, 1), ), ],
                [sg.Text('The Header on Row:', size=(15, 1)),
                 sg.Input(values['header'], key='header', size=(5, 1)), sg.Text('', size=(3, 1)),],

                [sg.Checkbox('Skip Blank Lines', key='del_blank_lines', size=(15, 1),
                             default=values['del_blank_lines']),
                 sg.Checkbox('Trim Spaces', key='trim', size=(10, 1), default=values['trim']),
                 sg.Checkbox('Skip Blank Sheets', key='skip_blank_sheet', size=(15, 1),
                             default=values['skip_blank_sheet']),
                 ],

                [sg.Checkbox('Add a Column, Values is The Table Name', key='add_tname', size=(35, 1),
                             default=values['add_tname']),
                 ],
                [sg.Checkbox('Recursion of Directories', key='loop_subdir', size=(25, 1), default=values['loop_subdir']),],
                [sg.Checkbox('Transform Chinese in Table/Column Name to The First Letter', key='trf_cn', size=(45, 1), default=values['trf_cn']),],

                [sg.Text('Run Sql Before Starting:', size=(17, 1)),
                 sg.Input('{}'.format(values['sql_b4']), key='sql_b4', size=(28, 1)),
                 sg.FileBrowse(initial_folder='{}'.format(values['sql_b4']), button_text=' Choose ')],
                [sg.Text('Run Sql After Comleting:', size=(17, 1)),
                 sg.Input('{}'.format(values['sql_after']), key='sql_after', size=(28, 1)),
                 sg.FileBrowse(initial_folder='{}'.format(values['sql_after']), button_text=' Choose ')],
            ]

            tab_layouts = [sg.Tab('General', layout_general), sg.Tab('Advanced', layout_advanced)]

            layout = [
                [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
            ]
        else:
            # menu
            menu_def = [
                ['&语言', ['&中文', '&English']],
                ['&数据库', ['&MySQL', '&Oracle', '&SQL Server', '&Hive']],
                ['&数据源', ['&目录', '&文件']],
                ['&帮助', ['&关于']],
            ]
            # general
            layout_general = [
                [sg.Menu(menu_def)],

                [sg.Text('Excel', size=(12, 1), text_color='red')],
                [
                 sg.Input('{}'.format(values['file_dir']), key='file_dir', size=(50, 1),
                          visible=self.ret_bool('source', values['source'])),
                 sg.FolderBrowse(initial_folder='{}'.format(values['file_dir']), button_text='选择目录',
                                 visible=self.ret_bool('source', values['source'])),
                 sg.Input('{}'.format(values['files']), key='files', size=(50, 1),
                          visible=not self.ret_bool('source', values['source'])),
                 sg.FilesBrowse(button_text='选择文件', visible=not self.ret_bool('source', values['source'])),
                 ],
                # dbinfo
                [sg.Text('{}'.format(values['dbtype']), text_color='red', key='dbtype'),
                 sg.Text('连接', text_color='red'),
                 ],
                [sg.Text('主机:', size=(5, 1)), sg.Input('{}'.format(values['host']), key='host', size=(15, 1)),
                 sg.Text(' ' * 11),
                 sg.Text('端口:', size=(7, 1)),
                 sg.Input('{}'.format(values['port']), key='port', size=(15, 1)), ],
                [sg.Text('用户:', size=(5, 1)), sg.Input('{}'.format(values['user']), key='user', size=(15, 1)),
                 sg.Text(' ' * 11),
                 sg.Text('密码:', size=(7, 1)),
                 sg.Input('{}'.format(values['passwd']), key='passwd', size=(15, 1)), ],
                [sg.Text('数据库:', size=(5, 1)),
                 sg.Input('{}'.format(values['dbname']), key='dbname', size=(50, 1)), sg.Text(' ' * 1),
                ],
                # mode
                [
                    sg.Text('模   式:', text_color='red'),
                    sg.Text(' ' * 6),
                    sg.Radio('覆   盖', group_id='mode', key='mode1', default=self.ret_bool('mode', values['mode'])),
                    sg.Text(' ' * 15),
                    sg.Radio('追   加', group_id='mode', key='mode2', default=not self.ret_bool('mode', values['mode'])),
                ],
                [sg.Button('开     始', size=(52, 1), key='start')],
                [sg.MLine(key='output', size=(58, 10), auto_refresh=True)],
            ]
            # advanced
            layout_advanced = [
                [sg.Text('CSV文件编码:', size=(12, 1)),
                 sg.Combo(['AUTO', 'UTF-8', 'ANSI', 'GBK'], default_value=values['csv_encoding'],
                          key='csv_encoding', size=(10, 1))],
                [sg.Text('将这些值替换为null:', size=(15, 1)),
                 sg.Input('{}'.format(values['na_values']), key='na_values', size=(30, 1)), ],

                [sg.Text('为创建的表名添加前缀:', size=(18, 1)),
                 sg.Input(values['prefix'], key='prefix', size=(10, 1), ), ],
                [sg.Text('将所有数据追加到表:', size=(16, 1)),
                 sg.Input(values['tname'], key='tname', size=(25, 1), ), ],
                [sg.Text('指定列名所在行数:', size=(15, 1)), sg.Input(values['header'], key='header', size=(5, 1)),
                 ],

                [sg.Checkbox('删除空行', key='del_blank_lines', size=(10, 1), default=values['del_blank_lines']),
                 sg.Checkbox('去除字符前后空格', key='trim', size=(15, 1), default=values['trim']),
                 sg.Checkbox('跳过空表', key='skip_blank_sheet', size=(6, 1), default=values['skip_blank_sheet']),
                 ],

                [sg.Checkbox('添加一列值为表名', key='add_tname', size=(15, 1), default=values['add_tname']),
                 sg.Checkbox('遍历子目录', key='loop_subdir', size=(9, 1), default=values['loop_subdir']),
                 ],
                [sg.Checkbox('转换表名和列名中文为拼音首字母', key='trf_cn', size=(33, 1), default=values['trf_cn']),],

                [sg.Text('导入开始前运行sql:', size=(15, 1)),
                 sg.Input('{}'.format(values['sql_b4']), key='sql_b4', size=(32, 1)),
                 sg.FileBrowse(initial_folder='{}'.format(values['sql_b4']), button_text=' 选择 ')],
                [sg.Text('导入结束后运行sql:', size=(15, 1)),
                 sg.Input('{}'.format(values['sql_after']), key='sql_after', size=(32, 1)),
                 sg.FileBrowse(initial_folder='{}'.format(values['sql_after']), button_text=' 选择 ')],

            ]

            tab_layouts = [sg.Tab('常规', layout_general), sg.Tab('高级', layout_advanced)]

            layout = [
                [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
            ]
        return layout

    def ret_bool(self, key, value):
        if key == 'source' and value == 'D':
            return True
        elif key == 'mode' and value == 'O':
            return True
        return False



