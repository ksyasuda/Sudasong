#!/usr/bin/env python
"""
Test whether the correct directories with the correct structure are created.
"""

import pathlib
from shutil import rmtree
import pytest
from get_song import config, create_dirs


base_dir = pathlib.Path(config.BASE_DIR)
not_created = pathlib.Path('')


def cleanup(path: pathlib.Path):
    """
    Removes tests directories.

    Input:
        path: path to the base_dir/Name
    """
    rmtree(path)


def cleanup_album(path: pathlib.Path):
    """
    Removes test album directory.

    Input:
        path: path to the base_dir/Name/Album
    """
    # use rmdir here since the directory I created is empty and don't risk
    # deleting anything else.
    path.rmdir()


def test_1():
    """
    Tests creating directory for Yannick Nandury and his album: Freud.
    """
    name = "Yannick Nandury"
    album = "Freud"
    create_dirs(name, album, True)
    del_path = base_dir.joinpath(name)
    # the path to base_dir/"Yannick Nandury"/ should exist
    assert del_path.exists()
    full_path = del_path.joinpath(album)
    # path to base/yannick/frued should exist
    assert full_path.exists()
    cleanup(del_path)


def test_2():
    """
    Tests trying to create directories that already exist.
    """
    name = "Lil Tecca"
    album = "VirgoWorld"
    path = create_dirs(name, album, True)
    assert path == not_created


def test_3():
    """
    Tests trying to create dir when artist exists but album does not.
    """
    name = "Lil Tecca"
    album = "Charles Altman IV"
    parent_path = base_dir.joinpath(name)
    assert parent_path.exists()
    path = create_dirs(name, album, True)
    assert parent_path.exists()
    assert path.exists()
    cleanup_album(path)
    assert not path.exists()
    assert parent_path.exists()


if __name__ == '__main__':
    pytest.main(["-vv", "-k TestCheckCreteCorrectDirs"])
