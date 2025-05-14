from imports import *

# Initialize Pygame Mixer for audio playback
pygame.mixer.init()

# Adjust tempo using pydub
def change_tempo(file_path, tempo_factor):
    audio = AudioSegment.from_file(file_path)
    new_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * tempo_factor)
    }).set_frame_rate(audio.frame_rate)

    # Write the modified audio to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    new_audio.export(temp_file.name, format="wav")
    return temp_file.name

# Function to play/pause the selected audio file
def toggle_play_pause(file_path, is_paused):
    if is_paused:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

# Function to stop audio
def stop_audio():
    pygame.mixer.music.stop()

# Function to loop audio (play indefinitely)
def loop_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(loops=-1)

# Function to search audio files based on user input
def search_files(search_term, file_list):
    return [f for f in file_list if search_term.lower() in f.lower()]

# Function to call FFmpeg for exporting the file
def export_audio_ffmpeg(input_file, output_file):
    command = ['ffmpeg', '-i', input_file, '-vn', output_file]
    subprocess.run(command)


def create_window():
    from windowList import layout
    return sg.Window("Audio Player", layout, element_justification='c', finalize=True)
    

# Event loop
audio_files = []
is_paused = False
is_looping = False  # Track loop state
current_file = None
modified_file = None
audio_directory = None  # Initialize audio_directory to avoid undefined variable error

window = create_window()
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        window.close()
        pygame.mixer.quit()
        sys.exit()
    elif event == "-DIR-":
        # Update the list of audio files when a directory is selected
        audio_directory = values["-DIR-"]
        if os.path.exists(audio_directory):
            audio_files = [f for f in os.listdir(audio_directory) if f.endswith(('.wav', '.mp3', '.flac'))]
            window["-FILE LIST-"].update(audio_files)
    elif event == "-SEARCH-":
        search_term = values["-SEARCH-"]
        filtered_files = search_files(search_term, audio_files)
        window["-FILE LIST-"].update(filtered_files)
    elif event == "-FILE LIST-":
        if audio_directory:  # Ensure audio_directory is defined
            selected_file = values["-FILE LIST-"][0]
            full_path = os.path.join(audio_directory, selected_file)
            window["-SEARCH-"].update(full_path)
            current_file = full_path
            modified_file = current_file  # Initially, no tempo adjustment
        else:
            sg.popup_error("Please select a directory first")
    elif event == "-PLAY-":
        if modified_file and os.path.exists(modified_file):
            toggle_play_pause(modified_file, is_paused)
            is_paused = False
        else:
            sg.popup_error("Please select a valid audio file")
    elif event == "-PAUSE-":
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            is_paused = True
    elif event == "-STOP-":
        if pygame.mixer.music.get_busy():
            stop_audio()
            is_paused = False
            is_looping = False  # Stop loop if music stops
            window["-LOOP-"].update(button_color=("white", "gray"))  # Reset loop button color
    elif event == "-LOOP-":
        if modified_file and os.path.exists(modified_file):
            if not is_looping:
                loop_audio(modified_file)
                is_looping = True
                window["-LOOP-"].update(button_color=("white", "green"))  # Highlight when looping
            else:
                stop_audio()  # Stop the loop when toggled off
                is_looping = False
                window["-LOOP-"].update(button_color=("white", "gray"))  # Reset color when loop is off
    elif event == "Export":
        if current_file:
            # Get the output file path and call FFmpeg
            output_file = sg.popup_get_file("Save As", save_as=True, no_window=True, default_extension=".wav")
            if output_file:
                export_audio_ffmpeg(modified_file, output_file)
                sg.popup(f"Audio exported to {output_file}")
    # Update the volume based on slider input
    if "-VOLUME-" in values:
        pygame.mixer.music.set_volume(values["-VOLUME-"] / 100)
    # Update the tempo if the tempo slider is changed
    if current_file and event == "-TEMPO-":
        tempo_factor = values["-TEMPO-"] / 100.0  # 100% is normal speed
        modified_file = change_tempo(current_file, tempo_factor)  # Create the new modified audio
        if pygame.mixer.music.get_busy():
            toggle_play_pause(modified_file, is_paused)  # Play the modified audio if already playing
    if event == 'About':
        sg.popup("SampleBuddy", "Version 1.0\nMade by Marc\nAll vibes, no bugs.")
    elif event == 'Exit':
        window.close()
window.close()
pygame.mixer.quit()

# Close the window and quit pygame
