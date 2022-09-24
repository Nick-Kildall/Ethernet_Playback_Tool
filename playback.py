import PySimpleGUI as sg
import dpkt
from scapy.all import sendp
import time

class Playback():
    def __init__(self) -> None:
        pass

    def send_packets(self, path):
        try: # Use, dpkt to read and store packets as raw bytes
            with open(path, 'rb') as pcap_file:
                if path.endswith(".pcapng"):
                    pcap = dpkt.pcapng.Reader(pcap_file)
                elif path.endswith(".pcap") or path.endswith(".cap"):
                    pcap = dpkt.pcapng.Reader(pcap_file)

                packets = []
                count = 0
                for _timestamp, buf in pcap:
                    # unpack the Eth frame (mac, src/dst, ethertype)
                    eth = dpkt.ethernet.Ethernet(buf)
                    packets.append(eth) 
                    count += 1
        except FileNotFoundError as error:
            raise(error)
            
if __name__ == "__main__":
    layout = [  
            [sg.Text("Choose a CSV file:")],
            [sg.InputText(key="-FILE_PATH-"), 
            sg.FileBrowse()],
            [sg.Button('Submit'), sg.Exit()]
        ]

    window = sg.Window("Display CSV", layout)
    playback = Playback()

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        elif event == "Submit":
            file_path = values["-FILE_PATH-"]
            print(file_path)
            playback.send_packets(values["-FILE_PATH-"])
    window.close()
