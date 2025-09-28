from pathlib import Path

import nvwave


def play_sound(file_path: Path):
    nvwave.playWaveFile(str(file_path), asynchronous=True)


def format_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    result = f"{minutes:02d}:{seconds:02d}"
    if hours > 0:
        result = f"{hours:02d}:{result}"
    return result
