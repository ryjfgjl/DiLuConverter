"""
A python tool for batch importing excel/csv files into mysql database.
Author: ryjfgjl
Date: 2020-01-05

"""

Version = "2.0"

# import GUI model
import PySimpleGUI as sg
import traceback
import sys
from common.handleconfig import HandleConfig
sg.ChangeLookAndFeel('dark')
HandleConfig = HandleConfig()

# database connection
host = HandleConfig.handle_config("g", "dbinfo", "host")
port = HandleConfig.handle_config("g", "dbinfo", "port")
user = HandleConfig.handle_config("g", "dbinfo", "user")
passwd = HandleConfig.handle_config("g", "dbinfo", "passwd")
dbname = HandleConfig.handle_config("g", "dbinfo", "dbname")
# file information
file_dir = HandleConfig.handle_config("g", "file", "file_dir")
csv_encoding = HandleConfig.handle_config("g", "file", "csv_encoding")
na_values = HandleConfig.handle_config("g", "file", "na_values")

def exception_format():
    """
    Convert exception info into a string suitable for display.
    """
    return "".join(traceback.format_exception(
        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]
    ))


def generate_layout():
    # display
    layout = [
        [sg.Frame(layout=[
        [sg.Text('Host:',size=(5,1)),sg.Input('{}'.format(host), key='host', size=(15,1)),sg.Text(' '*11),sg.Text('Port:',size=(7,1)),sg.Input('{}'.format(port), key='port', size=(15,1)),],
        [sg.Text('User:',size=(5,1)),sg.Input('{}'.format(user), key='user', size=(15,1)),sg.Text(' '*11),sg.Text('Password:',size=(7,1)),sg.Input('{}'.format(passwd), key='passwd', size=(15,1)),],
        [sg.Text('Database Name:',size=(12,1)),sg.Input('{}'.format(dbname), key='dbname', size=(21,1)),
        sg.Checkbox('Re-Create Database?', key='redb',default=True)]],title='Datbase Connection',title_color='red')],
        [sg.Frame(layout=[
        [sg.Text('Repalce Values:',size=(12,1)),sg.Input('{}'.format(na_values), key='na_values', size=(44,1)),],
        [sg.Text('File Directionry:',size=(12,1)),sg.Input('{}'.format(file_dir), key='file_dir', size=(35,1)),
        sg.FolderBrowse(initial_folder='{}'.format(file_dir))],
        [sg.Text('CSV Encoding:',size=(12,1)),sg.Input('{}'.format(csv_encoding), key='csv_encoding', size=(25,1)),]],title='Files',title_color='red')],
        [sg.Button('Start',size=(54,1))]
    ]
    return layout


# The interface for the program
window = sg.Window('Excel Importer {0}'.format(Version), generate_layout(), location=(700, 100))

while True:
    try:
        event, values = window.read()
        if event == "Start":
            from events.excelimporter import ImportExcel
            ImportExcel = ImportExcel()
            ImportExcel.main(values) 
        elif event == sg.WIN_CLOSED:
            break
    except:
        # display the any program error
        sg.PopupError(exception_format())
        