"""Utility functions for get_song.py"""
import pathlib
from config import BASE_DIR

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


def remove_spaces(string: str) -> str:
    """Returns string without the spaces."""
    return ''.join(string.split(' ')[:])


def get_artist_dir(artist: str) -> str:
    """Gets the string of the artists name in the filesystem."""
    base_dir = pathlib.Path(BASE_DIR)
    for i in base_dir.iterdir():
        t_artist = get_current_directory(i)
        if artist.upper() == t_artist.upper() or \
                remove_spaces(artist.upper()) == \
                remove_spaces(t_artist.upper()):
            return str(t_artist)
    return ''
