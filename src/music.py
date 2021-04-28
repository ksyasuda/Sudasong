"""Music class."""
import pathlib
import sys
import config
from utils import get_current_directory, remove_spaces, get_artist_dir

class Music:
    """Music class to acumulate data about the Music directory."""
    def __init__(self):
        self.data = {}


    def get_artists_in_filesystem(self, path: pathlib.Path, is_verbose: bool) -> list[str]:
        """
        returns a list of artists in ~/Music/
        """
        if is_verbose:
            print('Getting list of artists.')
        tlist = []
        for tpath in path.iterdir():
            if tpath.is_dir():
                upper = get_current_directory(tpath)
                tlist.append(remove_spaces(upper))
                temp = get_current_directory(tpath)
                if temp not in self.data:
                    self.data[temp] = {}
        return tlist


    def get_albums_in_filesystem(self, path: pathlib.Path, artist: str,
                                 is_verbose: bool):
        """
        Returns list of UPPERCASE album names (with spaces removed)
        in filesystem for given artist
        """
        if is_verbose:
            print(f'Getting list of albums for {artist}.')
        tlist: list[str] = []
        new_path = path.joinpath(artist)
        for i in new_path.iterdir():
            if i.is_dir():
                upper = get_current_directory(i)
                tlist.append(remove_spaces(upper))
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
        upper_artists = [i.upper() for i in artists]
        if artist.upper() in upper_artists or remove_spaces(artist.upper()) in upper_artists:
            artist_dir = get_artist_dir(artist)
            if artist_dir == '':
                print('Error: Artist not found')
                sys.exit(1)
            albums = self.get_albums_in_filesystem(base_dir, artist_dir, is_verbose)
            upper_albums = [i.upper() for i in albums]
            if alb_name.upper() in upper_albums or \
                    remove_spaces(alb_name.upper()) in upper_albums:
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
