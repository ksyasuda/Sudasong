"""Utility functions for get_song.py"""
import pathlib

def get_current_directory(path: pathlib.Path) -> str:
    """
    Returns the artist name from the passed in path.
    """
    spath = str(path)
    return spath[spath.rfind('/') + 1:]


def get_space_separated(tname: str) -> str:
    """
    Gets space separated artists name based on directory name.
    ex. YoungThug -> Young Thug
    """
    name = ''
    for idx, i in enumerate(tname):
        if i.isupper() and idx != 0 or i.isnumeric():
            name += ' ' + i
            continue
        name += i
    return name
