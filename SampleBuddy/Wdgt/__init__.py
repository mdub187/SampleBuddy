import os

def wdgt():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))
    return {
        "loop": os.path.join(base_path, "Loop.png"),
        "pause": os.path.join(base_path, "Pause.png"),
        "play": os.path.join(base_path, "Play.png"),
        "stop": os.path.join(base_path, "Stop.png")
    }