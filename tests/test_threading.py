#!/usr/bin/env python
"""Tests using threading."""

import pathlib
import pytest
from threading import Thread
from test_utils import create_test_dir, create_test_song, delete_tree
from get_song import get_cover, move_song


test_dir = pathlib.Path(__file__[:__file__.rfind('/')])


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
    cover_thread = Thread(target=get_cover, args=[name, album, True])
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
