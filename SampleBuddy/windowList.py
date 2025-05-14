from imports import sg, mb
from Wdgt import wdgt

icons = wdgt()
play = icons["play"]
pause = icons["pause"]
stop = icons["stop"]
loop = icons["loop"]

layout = [
    [sg.MenuBar(mb)],
    [sg.Text("Select Directory:"), sg.Input(key="-DIR-", enable_events=True), sg.FolderBrowse()],
    [sg.Text("Search/Select Audio Files:"), sg.Input(key="-SEARCH-", enable_events=True)],
    [sg.Listbox(values=[], size=(60, 20), key="-FILE LIST-", enable_events=True)],
    [sg.Text("Volume")],
    [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=70, enable_events=True, key="-VOLUME-")],
    [sg.Text("Tempo")],
    [sg.Slider(range=(50, 150), orientation='h', size=(20, 15), default_value=100, enable_events=True, key="-TEMPO-")],
    [sg.Button(key="-PLAY-", image_filename=play, image_size=(5, 5), pad=(0)),
     sg.Button(key="-PAUSE-", image_filename=pause, image_size=(0.5, 0.5), pad=(1)),
     sg.Button(key="-STOP-", image_filename=stop, image_size=(5, 5), pad=(2)),
     sg.Button(key="-LOOP-", image_filename=loop, image_size=(5, 5), pad=(3))],
    [sg.Button("Export")],
]

if __name__ == "__main__":
    print(layout, mb)