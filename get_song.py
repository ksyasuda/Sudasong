#!/usr/bin/env python
"""
Downloads a song and album cover if cover for album does not exist.
Creates and places files in appropriate directories
"""

import sys
import os
import pathlib
from getopt import gnu_getopt, GetoptError
import config


def get_current_directory(path: pathlib.Path) -> str:
    """
    Returns the artist name from the passed in path.
    """
    spath = str(path)
    return spath[spath.rfind('/') + 1:]


class Music:
    """Music class to acumulate data about the Music directory."""
    def __init__(self):
        self.data = {}


    def get_artists_in_filesystem(self, path: pathlib.Path, is_verbose: bool) -> list[str]:
        """
        returns a lsit of artists in ~/Music/
        """
        if is_verbose:
            print('Getting list of artists.')
        tlist = []
        for tpath in path.iterdir():
            if tpath.is_dir():
                tlist.append(get_current_directory(tpath))
                temp = get_current_directory(tpath)
                if temp not in self.data:
                    self.data[temp] = {}
        return tlist


    def get_albums_in_filesystem(self, path: pathlib.Path, artist: str,
                                 is_verbose: bool):
        """
        Returns list of albums in filesystem for given artist
        """
        if is_verbose:
            print(f'Getting list of albums for {artist}.')
        tlist: list[str] = []
        new_path = path.joinpath(artist)
        for i in new_path.iterdir():
            if i.is_dir():
                tlist.append(get_current_directory(i))
                album = get_current_directory(i)
                if album not in self.data[artist]:
                    self.data[artist][album] = []
        return tlist


    def check_album_exists(self, artist: str, alb_name: str, is_verbose: bool) -> bool:
        """
        Returns whether or not the album exists in the filesystem at ~/Music/Artist/
        """
        base_dir = pathlib.Path(config.BASE_DIR)
        if is_verbose:
            print(f"Checking whether {alb_name} exists in {base_dir}.")
        artists = self.get_artists_in_filesystem(base_dir, is_verbose)
        if artist in artists:
            albums = self.get_albums_in_filesystem(base_dir, artist, is_verbose)
            if alb_name in albums:
                if is_verbose:
                    print(f"Found {alb_name} in directory.")
                return True
        if is_verbose:
            print(f"Did not find {alb_name} in directory.")
        return False


    def print_data(self):
        """Prints data."""
        for artist, vals in self.data.items():
            for album, songs in vals.items():
                print(artist, album, songs)


def get_song(link: str) -> pathlib.Path:
    """
    Gets the song with youtube-dl, given a link.
    Sends downloaded file to ~/temp/
    Returns path to the downloaded song.
    """
    temp_dir = pathlib.Path(config.TEMP_DIR)
    command = f"yta-mp3 {link}"
    command = f"youtube-dl --extract-audio --audio-format mp3 \
        --config-location /home/sudacode/.config/youtube-dl/config.audio {link}"
    os.system(command)
    path = pathlib.Path()
    for i in temp_dir.iterdir():
        path = i
    return path


def create_dirs(artist_name: str, album_name: str, is_verbose: bool) -> pathlib.Path:
    """
    Creates directory for the artist and album and returns the path to the
    album.
    """
    base_dir = pathlib.Path(config.BASE_DIR)
    new_path = base_dir.joinpath(artist_name)
    try:
        if is_verbose:
            print(f"Trying to create directory for {artist_name}")
        new_path.mkdir(parents=True)
        new_path = new_path.joinpath(album_name)
        if is_verbose:
            print('Creating new directory for {album_name} in {artist_name}')
        new_path.mkdir(parents=True)
    except FileExistsError:
        if is_verbose:
            print(f"{artist_name} already exists in filesystem...")
        new_path = new_path.joinpath(album_name)
        if is_verbose:
            print('Creating new directory for {album_name} in {artist_name}')
        new_path.mkdir(parents=True)
    return new_path


def move_song(old_path: pathlib.Path, new_path: pathlib.Path, is_verbose: bool):
    """
    Move song from download location to the passed in path.
    """
    song = get_current_directory(old_path)
    new_path = new_path.joinpath(song)
    old_path.rename(new_path)
    if is_verbose:
        print(f'Moved {song} to {new_path}')


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


def get_cover(art_name: str, alb_name: str, is_verbose: bool):
    """
    Gets the album cover for a given album by artists.
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


def run(song_link: str, artist_name: str, album_name: str, is_verbose: bool):
    """Gets the song with youtube-dl and creates directory if doesn't exist."""
    music = Music()
    temp_path = get_song(song_link)
    has_album = music.check_album_exists(artist_name, album_name, is_verbose)
    if not has_album:
        path = create_dirs(artist_name, album_name, is_verbose)
        move_song(temp_path, path, is_verbose)
        get_cover(artist_name, album_name, is_verbose)
        update_database()
    else:
        print(config.AlBUM_EXISTS.format(album_name))
        path = pathlib.Path(config.BASE_DIR)
        path = path.joinpath(artist_name, album_name)
        move_song(temp_path, path, is_verbose)
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
        NEED_HELP=''
        COVER=''
        VERBOSE=False
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
                COVER = arg
            elif opt in ('-v', '--verbose'):
                VERBOSE = True
        if NAME == '' or ALBUM == '':
            usage()
            sys.exit(1)
        run(LINK, NAME, ALBUM, VERBOSE)

    except GetoptError:
        print('Getopt Error')
        sys.exit(1)
