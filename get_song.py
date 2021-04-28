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


    def get_artists_in_filesystem(self, path: pathlib.Path) -> list[str]:
        """
        returns a lsit of artists in ~/Music/
        """
        tlist = []
        for tpath in path.iterdir():
            if tpath.is_dir():
                tlist.append(get_current_directory(tpath))
                artist = get_current_directory(tpath)
                if artist not in self.data:
                    self.data[artist] = {}
        return tlist


    def get_albums_in_filesystem(self, path: pathlib.Path, artist: str):
        """
        Returns list of albums in filesystem for given artist
        """
        tlist: list[str] = []
        new_path = path.joinpath(artist)
        for i in new_path.iterdir():
            if i.is_dir():
                tlist.append(get_current_directory(i))
                album = get_current_directory(i)
                if album not in self.data[artist]:
                    self.data[artist][album] = []
        return tlist


    def check_album_exists(self, artist, alb_name: str) -> bool:
        """
        Returns whether or not the album exists in the filesystem at ~/Music/Artist/
        """
        base_dir = pathlib.Path(config.BASE_DIR)
        artists = self.get_artists_in_filesystem(base_dir)
        if artist in artists:
            albums = self.get_albums_in_filesystem(base_dir, artist)
            if alb_name in albums:
                return True
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


def create_dirs(artist_name: str, album_name: str) -> pathlib.Path:
    """
    Creates directory for the artist and album and returns the path to the
    album.
    """
    base_dir = pathlib.Path(config.BASE_DIR)
    new_path = base_dir.joinpath(artist_name)
    new_path.mkdir(parents=True)
    new_path = new_path.joinpath(album_name)
    new_path.mkdir(parents=True)
    return new_path


def move_song(old_path: pathlib.Path, new_path: pathlib.Path):
    """
    Move song from download location to the passed in path.
    """
    song = get_current_directory(old_path)
    new_path = new_path.joinpath(song)
    old_path.rename(new_path)
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


def get_cover(art_name, alb_name):
    """
    Gets the album cover for a given album by artists.
    """
    aname = get_space_separated(art_name)
    bname = get_space_separated(alb_name)
    print(f"Getting cover for {aname} {bname}")
    base_dir = config.BASE_DIR
    path = pathlib.Path(base_dir)
    out_path = str(path.joinpath(art_name, alb_name, 'cover.jpg'))
    command = f"sacad '{aname}' '{bname}' 1000 '{out_path}'"
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


def run(song_link: str, artist_name: str, album_name: str):
    """Gets the song with youtube-dl and creates directory if doesn't exist."""
    music = Music()
    temp_path = get_song(song_link)
    has_album = music.check_album_exists(artist_name, album_name)
    has_album = False
    if not has_album:
        path = create_dirs(artist_name, album_name)
        move_song(temp_path, path)
        get_cover(artist_name, album_name)
        update_database()
    else:
        print(config.AlBUM_EXISTS.format(album_name))


if __name__ == '__main__':
    args = ['help=', 'link=', 'name=', 'album=', 'help=', 'cover=']
    try:
        options, remainder = gnu_getopt(sys.argv[1:], 'l:n:a:c:h', args)
        if len(options) == 0:
            usage()
            sys.exit(1)
        LINK = ''
        NAME = ''
        ALBUM = ''
        NEED_HELP=''
        COVER=''
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
        run(LINK, NAME, ALBUM)
    except GetoptError:
        print('Getopt Error')
        sys.exit(1)
