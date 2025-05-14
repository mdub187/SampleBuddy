from pydub.playback import play
from imports import sg, AudioSegment, pygame, play

# Initialize PyGame mixer
pygame.mixer.init()

# Load your audio sample using pydub
audio = AudioSegment.from_file('your_audio_sample.mp3')

# Define a function to change the tempo
def change_tempo(sound, speed=1.0):
    return sound.speedup(playback_speed=speed)

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
