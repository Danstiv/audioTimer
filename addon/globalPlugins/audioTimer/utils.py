from pathlib import Path

import nvwave


def play_sound(file_path: Path):
    nvwave.playWaveFile(str(file_path), asynchronous=True)
