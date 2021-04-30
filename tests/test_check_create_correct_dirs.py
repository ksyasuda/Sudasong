#!/usr/bin/env python
"""
Test whether the correct directories with the correct structure are created.
"""

import pathlib
from shutil import rmtree
import pytest
from get_song import config, create_dirs
from utils import get_space_separated


# base_dir = tests directory
base_dir = pathlib.Path(__file__[:__file__.rfind('/')])
not_created = pathlib.Path('')
tmp = base_dir.joinpath('tmp')
if not tmp.exists():
    tmp.mkdir()


def cleanup(path: pathlib.Path):
    """
    Removes tests directories.

    Input:
        path: path to the tmp folder
    """
    rmtree(path)
    tmp.mkdir()


def tmp_clean() -> bool:
    """
    Checks that the tmp folder doesn't contain anything yet and can begin testing.
    """
    return len([str(i) for i in tmp.iterdir()]) == 0


def test_neither_exists():
    """
    Tests creating directory for Yannick Nandury and his album: Freud.
    """
    if not tmp_clean():
        cleanup(tmp)
    name = "Yannick Nandury"
    album = "Freud"
    create_dirs(str(tmp), name, album, True)
    t_path = tmp.joinpath(name)
    # the path to base_dir/"Yannick Nandury"/ should exist
    assert t_path.exists()
    full_path = t_path.joinpath(album)
    # path to base/yannick/frued should exist
    assert full_path.exists()
    cleanup(tmp)


def test_both_exist():
    """
    Tests trying to create directories that already exist.
    """
    if not tmp_clean():
        cleanup(tmp)
    name = "Lil Tecca"
    album = "VirgoWorld"
    path = tmp.joinpath(name)
    path.mkdir()
    path = path.joinpath(album)
    path.mkdir()
    path = create_dirs(str(tmp), name, album, True)
    assert path == not_created
    cleanup(tmp)


def test_artist_exist():
    """
    Tests trying to create dir when artist exists but album does not.
    """
    if not tmp_clean():
        cleanup(tmp)
    name = "Lil Tecca"
    album = "Charles Altman IV"
    parent_path = tmp.joinpath(name)
    parent_path.mkdir()
    assert parent_path.exists()
    path = create_dirs(str(tmp), name, album, True)
    assert parent_path.exists()
    assert path.exists()
    assert parent_path.exists()
    cleanup(tmp)


def test_same_album_name_different_artist():
    """
    Like the name says.
    """
    if not tmp_clean():
        cleanup(tmp)
    name = "Yannick nandury"
    album = "Freud"
    name2 = "Charles Chobanimus Altimus IV"
    yannick = tmp.joinpath(name)
    charlie = tmp.joinpath(name2)
    # create dirs for artists
    yannick.mkdir()
    charlie.mkdir()
    # create dirs for albums
    frued_path = yannick.joinpath(album)
    frued_path.mkdir()
    charles_path = charlie.joinpath('Not Frued')
    charles_path.mkdir()
    path = create_dirs(str(tmp), name2, album, True)
    assert path.exists()
    assert frued_path.exists()
    cleanup(tmp)


if __name__ == '__main__':
    # creates tmp dir in the tests folder
    pytest.main(["-vv", "-k create_correct_dirs"])
