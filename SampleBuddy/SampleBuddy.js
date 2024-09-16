var os = require('os');
var sg = require('PySimpleGUI');
var pygame = require('pygame');
from pydub var AudioSegment = require('AudioSegment');
var tempfile = require('tempfile');

// Initialize Pygame Mixer for audio playback
pygame.mixer.init();

// Adjust tempo using pydub
function change_tempo(file_path, tempo_factor) {
    audio = AudioSegment.from_file(file_path);
    new_audio = audio._spawn(audio.raw_data, overrides={
        'frame_rate': Number(audio.frame_rate * tempo_factor)
    }).set_frame_rate(audio.frame_rate);
}
    // Write the modified audio to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=false, suffix='.wav');
    new_audio.export(temp_file.name, format='wav');
    return temp_file.name;

// Function to play/pause the selected audio file
function toggle_play_pause(file_path, is_paused) {
    if (is_paused) {
        pygame.mixer.music.unpause();
    } else {
        pygame.mixer.music.load(file_path);
        pygame.mixer.music.play();
    }
// Function to stop audio
function stop_audio() {
    pygame.mixer.music.stop();
}
// Function to loop audio (play indefinitely)
function loop_audio(file_path) {
    pygame.mixer.music.load(file_path);
    pygame.mixer.music.play(loops=-1);
}
// Function to search audio files based on user input
function search_files(search_term, file_list) {
    return [f for (f in file_list if (search_term.lower() in f.lower()];

// importing images for the GUI layouot
image_play = './Wdgt/Play.ico';
image_pause = './Wdgt/Pause.ico';
image_stop = './Wdgt/Stop.ico';
image_loop = './Wdgt/Loop.png';

// GUI layout
layout = [;
    [sg.Text('Select Directory:'), sg.Input(key='-DIR-', enable_events=true), sg.FolderBrowse()],
    [sg.Text('Search/Select Audio Files:'), sg.Input(key='-SEARCH-', enable_events=true)],
    [sg.Listbox(values=[], size=(60, 20), key='-FILE LIST-', enable_events=true)],
    [sg.Text('Volume')],
    [sg.Slider(range=(0, 100), orientation='h', size=(20, 15), default_value=70, enable_events=true, key='-VOLUME-')],
    [sg.Text('Tempo')],
    [sg.Slider(range=(50, 150), orientation='h', size=(20, 15), default_value=100, enable_events=true, key='-TEMPO-')],
    [sg.Button(key='-PLAY-', image_filename=image_play, image_size=(5, 5), pad=(0)), sg.Button(key='-PAUSE-', image_filename=image_pause, image_size=(.5, .5), pad=(1)), sg.Button(key='-STOP-', image_filename=image_stop, image_size=(5, 5), pad=(2)), sg.Button(key='-LOOP-', image_filename=image_loop, image_size=(5, 5), pad=(3))],
//    [sg.Button("Loop", key="-LOOP-", button_color=("white", "gray"))],  # Default loop button color
    [sg.Button('Clear', key='-CLEAR-'), sg.Button('Exit')];
];

// Create the window
window = sg.Window('Sample Buddy', layout, element_justification='c');

// Event loop
audio_files = [];
is_paused = false;
is_looping = false  // Track loop state
current_file = null;
modified_file = null;

while (true) {
    event, values = window.read();
}
    if (event == sg.WINDOW_CLOSED || event == 'Exit') {
        break;
    } else if (event == '-DIR-') {
        // Update the list of audio files when a directory is selected
        audio_directory = values['-DIR-'];
        if (os.path.exists(audio_directory)) {
            audio_files = [f for (f in os.listdir(audio_directory) if (f.endswith(('.wav', '.mp3', '.flac'))];
            window['-FILE LIST-'].update(audio_files);
    } else if (event == '-SEARCH-') {
        search_term = values['-SEARCH-'];
        filtered_files = search_files(search_term, audio_files);
        window['-FILE LIST-'].update(filtered_files);
    } else if (event == '-FILE LIST-') {
        selected_file = values['-FILE LIST-'][0];
        full_path = os.path.join(audio_directory, selected_file);
        window['-SEARCH-'].update(full_path);
        current_file = full_path;
        modified_file = current_file  // Initially, no tempo adjustment
    } else if (event == '-PLAY-') {
        if (modified_file && os.path.exists(modified_file)) {
            toggle_play_pause(modified_file, is_paused);
            is_paused = false;
        } else {
            sg.popup_error('Please select a valid audio file');
    } else if (event == '-PAUSE-') {
        if (pygame.mixer.music.get_busy()) {
            pygame.mixer.music.pause();
            is_paused = true;
    } else if (event == '-STOP-') {
        if (pygame.mixer.music.get_busy()) {
            stop_audio();
            is_paused = false;
            is_looping = false  // Stop loop if music stops
            window['-LOOP-'].update(button_color=('white', 'gray'))  // Reset loop button color
    } else if (event == '-LOOP-') {
        if (modified_file && os.path.exists(modified_file)) {
            if (!is_looping) {
                loop_audio(modified_file);
                is_looping = true;
                window['-LOOP-'].update(button_color=('white', 'green'))  // Highlight when looping
            } else {
                stop_audio()  // Stop the loop when toggled off
                is_looping = false;
                window['-LOOP-'].update(button_color=('white', 'gray'))  // Reset color when loop is off
        } else {
            sg.popup_error('Please select a valid audio file');
    } else if (event == '-CLEAR-') {
        window['-SEARCH-'].update('');
        window['-FILE LIST-'].update([]);
        current_file = null;
        modified_file = null;
            }
    // Update the volume based on slider input
    pygame.mixer.music.set_volume(values['-VOLUME-'] / 100);
        }
    // Update the tempo if the tempo slider is changed
    if (current_file && event == '-TEMPO-') {
        tempo_factor = values['-TEMPO-'] / 100.0  // 100% is normal speed
        modified_file = change_tempo(current_file, tempo_factor)  // Create the new modified audio
        if (pygame.mixer.music.get_busy()) {
            toggle_play_pause(modified_file, is_paused)  // Play the modified audio if already playing
        }
// Close the window and quit pygame
window.close();
pygame.mixer.quit();

    }
        }

        }

        }

        }

    }

}

}
