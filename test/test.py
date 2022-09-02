import PySimpleGUI as sg
import time

def my_function():
    time.sleep(30)

def my_function_with_parms(duration):
    time.sleep(duration)
    return 'My Return Value'

layout = [  [sg.Text('Call a lengthy function')],
            [sg.Button('Start'), sg.Button('Start 2'), sg.Button('Exit')]  ]

window = sg.Window('Long Operation Example', layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Start':
        window.perform_long_operation(my_function, '-FUNCTION COMPLETED-')
    elif event == 'Start 2':
        window.perform_long_operation(lambda: my_function_with_parms(10), '-FUNCTION COMPLETED-')
    elif event == '-FUNCTION COMPLETED-':
        sg.popup('Your function completed!')
window.close()
