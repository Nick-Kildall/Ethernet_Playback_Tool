import PySimpleGUI as sg
from scapy.all import sendp, rdpcap
import time

if __name__ == "__main__":
    layout = [  
            [sg.Text("Choose a CSV file:")],
            [sg.InputText(key="-FILE_PATH-"), 
            sg.FileBrowse()],
            [sg.Button('Submit'), sg.Exit()]
        ]

    window = sg.Window("Display CSV", layout)

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "Submit":
            file_path = values["-FILE_PATH-"]
            packets = rdpcap(file_path)
            st = time.time()
            sendp(packets, realtime=True, verbose=False) 
            ft = time.time()
            print(ft-st)  
    window.close()
