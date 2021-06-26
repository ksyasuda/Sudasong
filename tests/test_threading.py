#!/usr/bin/env python
"""Tests using threading."""

import pathlib
import pytest
from threading import Thread
from shutil import rmtree
from get_song import get_cover, move_song

test_dir = pathlib.Path(__file__[:__file__.rfind('/')])


def delete_tree(path: pathlib.Path):
    """
    Deletes the tree of files using shutil.
    Basically rm -rf
    """
    rmtree(path)


def create_test_dir(path: pathlib.Path, name,
                     album):
    """
    Creates a test directory for a song.
    """
    new_path = path.joinpath(name, album)
    if not new_path.exists():
        new_path.mkdir(parents=True)
    return new_path


def create_test_song(path: pathlib.Path, name,
                     album, song):
    """
    Creates a test directory for a song.
    """
    new_path = path.joinpath(name, album)
    if not new_path.exists():
        new_path.mkdir(parents=True)
    new_path = new_path.joinpath(song)
    if not new_path.exists():
        new_path.touch()
    return new_path


def cleanup():
    """
    Performs cleaup [deleting] on the test_1 input and output directories.
    """
    glob = 'test1_*'
    to_delete = test_dir.glob(glob)
    for i in to_delete:
        delete_tree(i)


def test_threading_1():
    """Test with threading."""
    name = 'Lil Tecca'
    album = 'Virgo World'
    song = 'Out of Love'
    temp_path = create_test_song(test_dir/'tmp', name, album, song + '.mp3')
    assert temp_path.exists()
    new_path = create_test_dir(test_dir/'out', name, album)
    assert new_path.exists()

    move_thread = Thread(target=move_song, args=[temp_path, new_path, True])
    # get_cover puts cover in Music dir automatically
    # cover_thread = Thread(target=get_cover, args=[name, album, True])
    move_thread.start()
    cover_thread.start()
    move_thread.join()
    cover_thread.join()

    assert not temp_path.exists()
    assert new_path.exists()

    delete_tree(test_dir/'tmp')
    delete_tree(test_dir/'out')


if __name__ == '__main__':
    pytest.main(["-vv", "-k test_threading"])
