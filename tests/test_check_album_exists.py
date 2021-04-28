#!/usr/bin/env python
"""
Test to check the check_album_exists(artist, album, verbose) funtion
"""

import unittest
import get_song
import pytest

MUSIC = get_song.Music()

class TestCheckAlbumExists(unittest.TestCase):
    """Test checkalbum exists."""
    def check_album_helper(self, name, album, assertion):
        """Helper method to call check_album_exists()."""
        exists = MUSIC.check_album_exists(name, album, False)
        self.assertEqual(exists, assertion)


    def test_does_exist1(self):
        """Checks an album from artist that does exist."""
        album = 'LegendsNeverDie'
        name = 'JUICEWRLD'
        self.check_album_helper(name, album, True)

    def test_doesnt_exist1(self):
        """Album/Artist that both don't exist."""
        album = 'LilPump'
        name = 'LilPump'
        self.check_album_helper(name, album, False)


if __name__ == '__main__':
    # unittest.main()
    # run pytest in very verbose mode
    pytest.main(["-vv"])
