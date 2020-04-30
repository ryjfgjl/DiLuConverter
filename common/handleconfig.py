"""
handle with config.ini
"""

import easygui
import os
import sys

class HandleConfig:

    def __init__(self):
        pass

    # handle config.ini
    def handle_config(self, option=None, section=None, key=None, value=None):
        import configparser
        conf = configparser.ConfigParser()
        realpath = os.path.split(os.path.realpath(sys.argv[0]))[0]
        configini = realpath + r"\config.ini"

        try:
            conf.read(configini)
            if option == 'g':
                value = conf.get(section, key)
                return value
            elif option == 's':
                conf.set(section, key, value)
            elif option == "a":
                conf.add_section(section)
            elif option == "rs":
                conf.remove_section(section)
            elif option == "ro":
                conf.remove_option(section, key)

            with open(configini, 'w') as fw:
                conf.write(fw)
            return conf

        except:
            easygui.exceptionbox()
