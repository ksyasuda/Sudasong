#!/usr/bin/env python
"""Test utils."""

import pathlib
from shutil import rmtree


test_dir = pathlib.Path(__file__[:__file__.rfind('/')])


def delete_tree(path: pathlib.Path):
    """
    Deletes the tree of files using shutil.
    Basically rm -rf
    """
    rmtree(path)


def create_test_dir(path: pathlib.Path, name,
                     album) -> pathlib.Path:
    """
    Creates a test directory for a song.
    """
    new_path = path.joinpath(name, album)
    if not new_path.exists():
        new_path.mkdir(parents=True)
    return new_path


def create_test_song(path: pathlib.Path, name,
                     album, song) -> pathlib.Path:
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


def cleanup() -> None:
    """
    Performs cleaup [deleting] on the test_1 input and output directories.
    """
    glob = 'test1_*'
    to_delete = test_dir.glob(glob)
    for i in to_delete:
        delete_tree(i)
