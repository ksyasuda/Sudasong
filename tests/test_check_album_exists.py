#!/usr/bin/env python
"""
Test to check the check_album_exists(artist, album, verbose) funtion
"""

import pathlib
import get_song
import pytest
from utils import get_artist_dir

MUSIC = get_song.Music()


def check_album_helper(name, album, assertion):
    """Helper method to call check_album_exists()."""
    exists = MUSIC.check_album_exists(name, album, False)
    assert exists == assertion


def test_does_exist1():
    """Checks an album from artist that does exist."""
    album = 'Legends Never Die'
    name = 'Juice WRLD'
    check_album_helper(name, album, True)


def test_doesnt_exist1():
    """Album/Artist that both don't exist."""
    album = 'Lil Pump'
    name = 'Lil Pump'
    check_album_helper(name, album, False)


def test_doesnt_exist2():
    """Artist exists but Album does not."""
    name = 'BROCKHAMPTON'
    album = 'SATURATION III'
    check_album_helper(name, album, False)


def test_exist_with_different_casing():
    """Test with name/album that exists but with different letter casings."""
    name = 'lil tecca'
    album = 'VIRgO woRlD'
    check_album_helper(name, album, True)
    check_album_helper('LIl Tec c a', album, True)


def test_not_exist_with_diff_casing():
    """
    Test with name that exists, album that doesn't exist and different
    letter casings.
    """
    name = '2 1 SaV age'
    album = 'isaAl bum'
    base_dir = get_song.config.BASE_DIR
    albums = MUSIC.get_albums_in_filesystem(pathlib.Path(base_dir),
                                            get_artist_dir(name), False)
    assert len(albums) > 0
    check_album_helper(name, album, False)


if __name__ == '__main__':
    pytest.main(["-vv", "-k check_album_exists"])
