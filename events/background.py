"""
# run on background without window
"""

import os
from common.handleconfig import HandleConfig
from events.importer import Importer

class Background:

    def __init__(self):
        self.HandleConfig = HandleConfig()
        self.configini = None
        self.Importer = Importer()


    def main(self):
        self.HandleConfig.configini = self.configini
        values = self.HandleConfig.get_defaults()
        values['schedule'] = True
        values['mode1'] = False
        values['mode2'] = False
        values['mode3'] = False
        if values['mode'] == 'O':
            values['mode1'] = True
        elif values['mode'] == 'A':
            values['mode2'] = True
        else:
            values['mode3'] = True
        self.Importer.values = values
        ret = self.Importer.main()
        if type(ret) == str:
            print(ret)
        else:
            log_file = ret[0]
            num = ret[1]
            num_s = ret[2]

            if os.path.isfile(log_file):
                print(f'Import Complete with log!\nPlease see {log_file}')
            else:
                print('Import Complete!')

