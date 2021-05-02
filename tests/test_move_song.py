#!/usr/bin/env python
"""Tests move song function."""

import pathlib
from shutil import rmtree
import pytest
from get_song import move_song

test_dir = pathlib.Path(__file__[:__file__.rfind('/')])
print(test_dir)

def delete_tree(path: pathlib.Path):
    """
    Deletes the tree of files using shutil.
    Basically rm -rf
    """
    rmtree(path)


def create_test_song(path: pathlib.Path, name,
                     album, song):
    """
    Creates a test directory for a song.
    """
    new_path = path.joinpath(name, album)
    new_path.mkdir(parents=True)
    new_path = new_path.joinpath(song)
    new_path.touch()
    return new_path


def test_move_song1():
    """Tests moving a song to intended directory."""
    name = 'Yannick Nandury'
    album = 'Chronicles of Frued'
    song = 'Frued.mp3'
    path = create_test_song(test_dir/'test1_in', name, album, song)
    assert path.exists()
    new_path = pathlib.Path(test_dir/'test1_out'/name/album/song)
    move_song(path, new_path, True)
    assert not path.exists()
    assert new_path.exists()


if __name__ == '__main__':
    pytest.main(["-vv", "-k move_song"])
