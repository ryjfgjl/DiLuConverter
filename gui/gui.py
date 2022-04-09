##############################################################
# Program GUI
##############################################################

import PySimpleGUI as sg

# import configuration file
from common.handleconfig import HandleConfig

sg.ChangeLookAndFeel('dark')

class Gui():

    def __init__(self):
        self.HandleConfig = HandleConfig()

    def default_mode(self, default_values, _mode):
        if _mode == default_values['mode']:
            return True
        else:
            return False

    # generate chinese GUI
    def generate_layout(self):
        default_values = self.HandleConfig.get_defaults()
        if default_values['language'] == '中文':
            # menu
            menu_def = [
                ['&语言', ['&中文', '&English']],
                ['&数据库', ['&MySQL', '&Oracle']],
                ['&关于', ['&获取帮助']],
            ]
            # general
            layout_general = [
                [sg.Menu(menu_def)],
                [sg.Text('Excel文件', size=(12, 1), text_color='red')],
                    [sg.Text('所在文件夹:', size=(12, 1)), sg.Input('{}'.format(default_values['file_dir']), key='file_dir', size=(35, 1)),
                     sg.FolderBrowse(initial_folder='{}'.format(default_values['file_dir']), button_text=' 选择 ')],
                [sg.Text('{}连接'.format(default_values['dbtype']), size=(12, 1), text_color='red'),
                 ],

                [sg.Text('主机:', size=(5, 1)), sg.Input('{}'.format(default_values['host']), key='host', size=(15, 1)), sg.Text(' ' * 11),
                     sg.Text('端口:', size=(7, 1)), sg.Input('{}'.format(default_values['port']), key='port', size=(15, 1)), ],
                    [sg.Text('用户:', size=(5, 1)), sg.Input('{}'.format(default_values['user']), key='user', size=(15, 1)), sg.Text(' ' * 11),
                     sg.Text('密码:', size=(7, 1)), sg.Input('{}'.format(default_values['passwd']), key='passwd', size=(15, 1)), ],
                    [

                     sg.Text('数据库:', size=(5, 1)), sg.Input('{}'.format(default_values['dbname']), key='dbname', size=(21, 1)), sg.Text(' ' * 1),
                     sg.Text('模式:', text_color='red'),
                     sg.Text(' ' * 1),
                      sg.Radio('覆盖', group_id='mode', key='mode1', default=self.default_mode(default_values, 'mode1')),
                      sg.Radio('追加', group_id='mode', key='mode2', default=self.default_mode(default_values, 'mode2')),
                     ],

                [sg.Button('开始', size=(52, 1))]
            ]
            # advanced
            layout_advanced = [
                [sg.Text('CSV文件编码:', size=(12, 1)),
                    sg.Combo(['AUTO', 'UTF-8', 'ANSI', 'GBK'], default_value=default_values['csv_encoding'], key='csv_encoding', size=(10, 1))],
                [sg.Text('将这些值替换为null:', size=(15, 1)),sg.Input('{}'.format(default_values['na_values']), key='na_values', size=(40, 1)), ],
                [sg.Text('为创建的表名添加前缀:', size=(18, 1)), sg.Input(default_values['prefix'], key='prefix', size=(20, 1),), ],
                [sg.Text('将数据追加到已存在的表（追加模式有效）:', size=(34, 1)), sg.Input(default_values['tname'], key='tname', size=(20, 1), ), ],
                [sg.Text('指定列名所在行数:', size=(18, 1)), sg.Input(default_values['header'], key='header', size=(10, 1)), ],
                [sg.Checkbox('删除空行', key='del_blank_lines', size=(7, 1), default=default_values['del_blank_lines']),
                 sg.Checkbox('去除字符前后空格', key='trim', size=(14, 1), default=default_values['trim']),
                 sg.Checkbox('跳过空表', key='skip_blank_sheet', size=(6, 1), default=default_values['skip_blank_sheet']),
                 sg.Checkbox('遍历子目录', key='loop_subdir', size=(9, 1), default=False),
                 ],


                [sg.Button('开始', size=(52, 1))]
            ]

            tab_layouts = [sg.Tab('常规', layout_general), sg.Tab('高级', layout_advanced)]

            layout = [
                [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
            ]
        else:
            # English gui
            # menu
            menu_def = [
                ['&Language', ['&中文', '&English']],
                ['&Database', ['&MySQL', '&Oracle']],
            ]
            # general
            layout_general = [
                [sg.Menu(menu_def)],
                [sg.Text('Excel', size=(12, 1), text_color='red')],
                [sg.Text('Directory:', size=(8, 1)),
                 sg.Input('{}'.format(default_values['file_dir']), key='file_dir', size=(35, 1)),
                 sg.FolderBrowse(initial_folder='{}'.format(default_values['file_dir']), button_text=' Choose ')],
                [sg.Text('{} Connection'.format(default_values['dbtype']), size=(17, 1), text_color='red'),
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

                    sg.Text('Schema:', size=(6, 1)),
                    sg.Input('{}'.format(default_values['dbname']), key='dbname', size=(15, 1)), sg.Text(' ' * 1),
                    sg.Text('Mode:', text_color='red'),
                    #sg.Text(' ' * 1),
                    sg.Radio('Overwrite', group_id='mode', key='mode1', default=self.default_mode(default_values, 'mode1')),
                    sg.Radio('Append', group_id='mode', key='mode2', default=self.default_mode(default_values, 'mode2')),
                ],

                [sg.Button('Start', size=(52, 1))]
            ]
            # advanced
            layout_advanced = [
                [sg.Text('CSV Encoding:', size=(12, 1)),
                 sg.Combo(['AUTO', 'UTF-8', 'ANSI', 'GBK'], default_value=default_values['csv_encoding'],
                          key='csv_encoding', size=(10, 1))],
                [sg.Text('Replace to null:', size=(15, 1)),
                 sg.Input('{}'.format(default_values['na_values']), key='na_values', size=(40, 1)), ],
                [sg.Text('add table prefix:', size=(18, 1)),
                 sg.Input(default_values['prefix'], key='prefix', size=(20, 1), ), ],
                [sg.Text('append all data to one exists table:', size=(25, 1)),
                 sg.Input(default_values['tname'], key='tname', size=(25, 1), ), ],
                [sg.Text('The Column on row:', size=(18, 1)), sg.Input(default_values['header'], key='header', size=(10, 1)), ],
                [sg.Checkbox('Skip blank line', key='del_blank_lines', size=(10, 1), default=default_values['del_blank_lines']),
                 sg.Checkbox('Trim space', key='trim', size=(8, 1), default=default_values['trim']),
                 sg.Checkbox('Skip blank sheet', key='skip_blank_sheet', size=(12, 1),
                             default=default_values['skip_blank_sheet']),
                 sg.Checkbox('Sub Dir', key='loop_subdir', size=(7, 1),default=False),
                 ],

                [sg.Button('Start', size=(52, 1))]
            ]

            tab_layouts = [sg.Tab('General', layout_general), sg.Tab('Advanced', layout_advanced)]

            layout = [
                [sg.TabGroup([tab_layouts], selected_background_color='red', key='tabgroup')],
            ]
        return layout



