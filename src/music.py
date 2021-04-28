"""Music class."""
import pathlib
import config
from utils import get_current_directory

class Music:
    """Music class to acumulate data about the Music directory."""
    def __init__(self):
        self.data = {}


    def get_artists_in_filesystem(self, path: pathlib.Path, is_verbose: bool) -> list[str]:
        """
        returns a lsit of UPPERCASE artists in ~/Music/
        """
        if is_verbose:
            print('Getting list of artists.')
        tlist = []
        for tpath in path.iterdir():
            if tpath.is_dir():
                tlist.append(get_current_directory(tpath).upper())
                temp = get_current_directory(tpath)
                if temp not in self.data:
                    self.data[temp] = {}
        return tlist


    def get_albums_in_filesystem(self, path: pathlib.Path, artist: str,
                                 is_verbose: bool):
        """
        Returns list of UPPERCASE albums in filesystem for given artist
        """
        if is_verbose:
            print(f'Getting list of albums for {artist}.')
        tlist: list[str] = []
        new_path = path.joinpath(artist)
        for i in new_path.iterdir():
            if i.is_dir():
                tlist.append(get_current_directory(i).upper())
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
        if artist.upper() in artists:
            albums = self.get_albums_in_filesystem(base_dir, artist, is_verbose)
            if alb_name.upper() in albums:
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
