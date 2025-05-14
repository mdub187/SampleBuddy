import PySimpleGUI as sg
import pygame
from pydub import AudioSegment
from pydub.playback import play

# Initialize PyGame mixer
pygame.mixer.init()

# Load your audio sample using pydub
audio = AudioSegment.from_file('your_audio_sample.mp3')

# Define a function to change the tempo
def change_tempo(sound, speed=1.0):
    return sound.speedup(playback_speed=speed)

# Define the layout with a tempo slider
layout = [
    # [sg.Button('Play'), sg.Button('Pause'), sg.Button('Stop')],
    [sg.Text('Tempo'), sg.Slider(range=(0.5, 2.0), resolution=0.1, default_value=1.0, orientation='h', key='tempo_slider')],
]

window = sg.Window('Audio Player', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    elif event == 'Play':
        # Get the value of the slider and adjust the speed
        playback_speed = values['tempo_slider']
        modified_audio = change_tempo(audio, playback_speed)
        
        # Export the modified audio to a temporary file and play it
        modified_audio.export('temp_audio.mp3', format='mp3')
        pygame.mixer.music.load('temp_audio.mp3')
        pygame.mixer.music.play()

    elif event == 'Pause':
        pygame.mixer.music.pause()

    elif event == 'Stop':
        pygame.mixer.music.stop()

window.close()
