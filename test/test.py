import PySimpleGUI as sg

layout = [  [sg.Text('Demonstration of Multiline Element Printing')],
            [sg.MLine(key='-ML1-'+sg.WRITE_ONLY_KEY, size=(40,8))],
            [sg.MLine(key='-ML2-'+sg.WRITE_ONLY_KEY,  size=(40,8))],
            [sg.Button('Go'), sg.Button('Exit')]]

window = sg.Window('Window Title', layout, finalize=True)


# Note, need to finalize the window above if want to do these prior to calling window.read()
window['-ML1-'+sg.WRITE_ONLY_KEY].print(1,2,3,4,end='', text_color='red', background_color='yellow')
window['-ML1-'+sg.WRITE_ONLY_KEY].print('\n', end='')
window['-ML1-'+sg.WRITE_ONLY_KEY].print(1,2,3,4,text_color='white', background_color='green')
counter = 0

while True:             # Event Loop
    event, values = window.read(timeout=100)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == 'Go':
        window['-ML1-'+sg.WRITE_ONLY_KEY].print(event, values, text_color='red')
    window['-ML2-'+sg.WRITE_ONLY_KEY].print(counter)
    counter += 1
window.close()