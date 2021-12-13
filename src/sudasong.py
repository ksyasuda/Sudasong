#!/usr/bin/env python
"""
Downloads a song and album cover if cover for album does not exist.
Creates and places files in appropriate directories
"""


import os
import pathlib
import sys
from getopt import GetoptError, gnu_getopt
from threading import Thread
from typing import Union

import config
from music import Music
from utils import get_current_directory, get_space_separated, remove_spaces


def get_song(link: str) -> pathlib.Path:
    """
    Gets the song with youtube-dl, given a link.
    Sends downloaded file to ~/temp/
    Returns path to the downloaded song.
    """
    temp_dir = pathlib.Path(config.TEMP_DIR)
    command = f"yta-mp3 {link}"
    command = f"yt-dlp --extract-audio --audio-format mp3 \
        --config-location \
        /home/sudacode/.config/yt-dlp/config.audio {link}"
    os.system(command)
    path = pathlib.Path()
    for i in temp_dir.iterdir():
        path = i
    return path


def create_dirs(path: str, artist_name: str,
                album_name: str, is_verbose: bool) -> pathlib.Path:
    """
    Creates directory for the artist and album and returns the path to the
    album.

    Returns empty pathlib.Path if artist and album already exist in filesystem
    """
    base_dir = pathlib.Path(path)
    new_path = base_dir.joinpath(artist_name)
    try:
        if is_verbose:
            print(f'Trying to create directory for "{artist_name}"')
        new_path.mkdir(parents=True)
        new_path = new_path.joinpath(album_name)
        if is_verbose:
            print(f'Creating new directory for \
            "{album_name}" in "{artist_name}"')
        new_path.mkdir(parents=True)
    except FileExistsError:
        if is_verbose:
            print(f"{artist_name} already exists in filesystem...")
        new_path = new_path.joinpath(album_name)
        if is_verbose:
            print('Creating new directory for \
                  "{album_name}" in "{artist_name}"')
        try:
            new_path.mkdir(parents=True)
        except FileExistsError:
            print('Album already exists in filesystem..')
            print('Nothing to do...\nExiting')
            return pathlib.Path('')
    return new_path


def move_song(old_path: pathlib.Path, new_path: pathlib.Path,
              is_verbose: bool) -> Union[pathlib.Path, int]:
    """
    Move song from download location to the passed in path.

    Inputs:
        old_path: path to the file currently [includes song.mp3]
        new_path: new path to the album [not includes song.mp3]
        is_verbose: verbose
    """
    if not old_path.exists():
        print(f'{str(old_path)} in path does not exist in the filesystem')
        return -1
    song = get_current_directory(old_path)
    if new_path.joinpath(song).exists():
        # if the song is already in the library, delete old_path
        print(f"{song} already in the filesystem at {str(old_path)}.")
        print(f"Deleting {str(old_path)}")
        old_path.unlink()
        return -1
    if not new_path.exists():
        # if the artist/album directories don't exist, create them first
        new_path.mkdir(parents=True)
    # move from temp folder to corect location in Music dir
    temp = old_path.rename(new_path.joinpath(song))
    if is_verbose:
        print(f'Moved {song} to {temp}')
    return new_path


def get_cover(art_name: str, alb_name: str, is_verbose: bool):
    """
    Gets the album cover for a given album by artists.

    Outputs the image to ~/Music/art_name/alb_name/cover.jpg
    """
    aname = get_space_separated(art_name)
    bname = get_space_separated(alb_name)
    base_dir = config.BASE_DIR
    path = pathlib.Path(base_dir)
    out_path = str(path.joinpath(art_name, alb_name, 'cover.jpg'))
    command = f"sacad '{aname}' '{bname}' 1000 '{out_path}'"
    if is_verbose:
        print(f"Getting cover for {aname} {bname}")
    os.system(command)


def update_database():
    """Runs the update command to update the database."""
    os.system(config.UPDATE)


def usage():
    """Prints usage info."""
    print('Usage:')
    print('-l, --link\t\tlink to song')
    print('-n, --name\t\tname of artist')
    print('-a, --album-name\tname of album')
    print('-c, --cover\t\tonly download cover')
    print('-h, --help\t\thelp menu (this menu)')


def run(song_link: str, artist_name: str, album_name: str, is_verbose: bool,
        cover: bool):
    """
    Driver function of the module.
    Gets the song with youtube-dl and creates directory if doesn't exist.  Then
    get's the album artwork unless otherwise specified.

    Params:
        song_link: link to the song, link that will be used in youtube-dl call
        artist_name: name of the artist
        album_name: name of the album
        is_verbose: print verbose output
        cover: if there is already an album cover for
            [album_name] by [artist_name]
    """
    music = Music()
    temp_path = get_song(song_link)
    has_album = music.check_album_exists(remove_spaces(artist_name),
                                         remove_spaces(album_name), is_verbose)
    if not has_album:
        path = create_dirs(config.BASE_DIR, artist_name,
                           album_name, is_verbose)
        # move_song(temp_path, path, is_verbose)

        threads = []
        if not cover:
            # get_cover(artist_name, album_name, is_verbose)
            cover_thread = Thread(target=get_cover, args=[artist_name, album_name,
                                  is_verbose])
            cover_thread.start()
            threads.append(cover_thread)

        move_thread = Thread(target=move_song, args=[temp_path, path, is_verbose])
        move_thread.start()
        threads.append(move_thread)

        # wait for threads to finish
        for thread in threads:
            thread.join()

        update_database()
    else:
        print(config.ALBUM_EXISTS.format(album_name))
        path = pathlib.Path(config.BASE_DIR)
        path = path.joinpath(artist_name, album_name)
        res = move_song(temp_path, path, is_verbose)
        if res == -1:
            return 1
        update_database()


if __name__ == '__main__':
    args = ['link=', 'name=', 'album=', 'cover=', 'help=', 'verbose=']
    try:
        options, remainder = gnu_getopt(sys.argv[1:], 'l:n:a:c:hv:', args)
        if len(options) == 0:
            usage()
            sys.exit(1)
        LINK = ''
        NAME = ''
        ALBUM = ''
        NEED_HELP = ''
        COVER = False
        VERBOSE = False
        for opt, arg in options:
            if opt in ('-h', '--help'):
                usage()
                sys.exit(1)
            if opt in ('-l', '--link'):
                LINK = arg
            elif opt in ('-n', '--name'):
                NAME = arg
            elif opt in ('-a', '--album-name'):
                ALBUM = arg
            elif opt in ('-c', '--cover'):
                COVER = True
            elif opt in ('-v', '--verbose'):
                VERBOSE = True
        if NAME == '' or ALBUM == '':
            usage()
            sys.exit(1)
        run(LINK, NAME, ALBUM, VERBOSE, COVER)

    except GetoptError:
        print('Getopt Error')
        sys.exit(1)
