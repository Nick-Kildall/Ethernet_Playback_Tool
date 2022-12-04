"""
Opens a GUI where you can select a pcap file to playback.
There are multiple options for playback, including:
changing ip and mac addresses and recalculating the checksum.
"""

import PySimpleGUI as sg

from scapy.all import *
from scapy.layers.http import *
import time

if __name__ == "__main__":
    # Create the GUI
    layout = [  
            [sg.Text("Choose a CSV file: (Required)")],
            [sg.InputText(key="-FILE_PATH-"), sg.FileBrowse()],
            [sg.Text("Choose a src IP:")],
            [sg.InputText(key="-src_ip-")],
            [sg.Text("Choose a dst IP:")],
            [sg.InputText(key="-dst_ip-")],
            [sg.Text("Choose a src mac:")],
            [sg.InputText(key="-src_mac-")],
            [sg.Text("Choose a dst mac:")],
            [sg.InputText(key="-dst_mac-")],
            [sg.Checkbox('Recalculate checksum:', key="-checksum-",default=True)],
            [sg.Button('Submit'), sg.Exit()]
        ]

    window = sg.Window("Display CSV", layout)

    # Run the GUI while the application is running
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "Submit": # User wants to playback a file
            # grab packets
            file_path = values["-FILE_PATH-"]
            packets = rdpcap(file_path)

            # grab playback options
            src_mac = values["-src_mac-"]
            dst_mac = values["-dst_mac-"]
            src_ip = values["-src_ip-"]
            dst_ip = values["-dst_ip-"]
            recaluculate_checksum = values["-checksum-"]

            # Modify packets with playback options
            edited_packets = []
            for pkt in packets:
                if Ether in pkt: # change mac addresses  and checksum
                    if src_mac != "":
                        pkt[Ether].src= src_mac
                    if dst_mac != "":
                        pkt[Ether].dst= dst_mac
                    if recaluculate_checksum:
                        del(pkt[Ether].chksum) # remove checksum to recalculate
                
                if IP in pkt: # change ip addresses and checksum
                    if src_ip != "":
                        pkt[IP].src= src_ip 
                    if dst_ip != "":
                        pkt[IP].dst= dst_ip
                    if recaluculate_checksum:
                        del(pkt[IP].chksum) # remove checksum to recalculate
                    
                if TCP in pkt and recaluculate_checksum:
                    del(pkt[TCP].chksum) # remove checksum to recalculate

                edited_packets.append(pkt)

            # send packets
            st = time.time()
            sendp(edited_packets, realtime=True, verbose=False) 
            ft = time.time()
            
            print(f"Took {ft-st} seconds to send the pcap file")  
    window.close()
