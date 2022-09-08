"""
run with a window
"""

import PySimpleGUI as sg
import os
from common.handleconfig import HandleConfig
from gui.gui import Gui
from events.importer import Importer
from setting.setting import Setting


class Window:

    def __init__(self):
        self.Gui = Gui()
        self.HandleConfig = HandleConfig()
        self.Importer = Importer()
        self.Setting = Setting()
        self.VERSION = None

    def main(self):
        default_values = self.HandleConfig.get_defaults()
        window = self.show_window(default_values)

        while True:
            # keep running with a gui event if any error occurs
            # until click x to close
            event, values = window.read()
            if values:
                values['language'] = default_values['language']
                values['dbtype'] = default_values['dbtype']
                values['schedule'] = False
                values['source'] = default_values['source']
                if values['mode1']:
                    values['mode'] = 'O'
                elif values['mode2']:
                    values['mode'] = 'A'
                else:
                    values['mode'] = 'M'

            try:
                if event == "start":
                    # start to import

                    self.Importer.values = values
                    self.Importer.window = window

                    window.perform_long_operation(self.Importer.main, '-IMPORT COMPLETED-')

                elif event == '-IMPORT COMPLETED-':
                    if type(values['-IMPORT COMPLETED-']) == str:
                        sg.PopupError(values['-IMPORT COMPLETED-'])
                        continue
                    log_file = values['-IMPORT COMPLETED-'][0]
                    num = values['-IMPORT COMPLETED-'][1]
                    num_s = values['-IMPORT COMPLETED-'][2]

                    if os.path.isfile(log_file):
                        layout = [
                            [sg.Text('Import Complete with log!\n\nTotal: {}, Succeed: {}\n'.format(num, num_s))],
                            [sg.OK('Finish'), sg.Text(' ' * 10), sg.Button('View Log', key='E')]
                        ]
                        complete_window = sg.Window(layout=layout, title='Report')
                        complete_event, complete_values = complete_window.read()
                        complete_window.close()
                        if complete_event == 'E':
                            os.popen(log_file)
                    else:
                        layout = [
                            [sg.Text('Import Complete!\n\nTotal: {}, Succeed: {}\n'.format(num, num_s))],
                            [sg.OK('Finish'), sg.Text(' ' * 10)]
                        ]
                        complete_window = sg.Window(layout=layout, title='Report')
                        complete_window.read()
                        complete_window.close()
                elif event == sg.WIN_CLOSED:
                    break

                else:
                    self.Setting.event = event
                    self.Setting.values = values
                    self.Setting.window = window
                    self.Setting.show_window = self.show_window
                    window = self.Setting.main()

            except Exception as reason:
                # throw exception
                sg.PopupError(reason)
            finally:
                if event != sg.WIN_CLOSED:
                    self.HandleConfig.configini = f"config.ini"
                    self.HandleConfig.save_defaults(values)
                    if values['current_config']:
                        self.HandleConfig.configini = f"saved_configuration/{values['current_config']}.ini"
                        if event != 'load_config':
                            self.HandleConfig.save_defaults(values)
                default_values = self.HandleConfig.get_defaults()
                if event == 'load_config':
                    window.close()
                    window = self.show_window(default_values)


    def show_window(self, values):
        window = sg.Window('ExcelToDatabase {0}'.format(self.VERSION), self.Gui.generate_layout(values)
                           , icon='ExcelToDatabase.ico')
        return window
