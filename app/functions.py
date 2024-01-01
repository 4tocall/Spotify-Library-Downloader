from app.auth import spotipy
from app.library_config import get_base_directory, load_from_config
from app.utils import from_json, printc, to_json, set_folder_icon, error_handler
from app.auth import os
import subprocess

@error_handler
def create_track_dict(track):
    if track['track']['album']['album_type'] != "album": 
        album = f"{track['track']['album']['name']} ({track['track']['album']['album_type']})"
    else:
        album = track['track']['album']['name']
    
    return {
        'name': track['track']['name'],
        'artist': track['track']['artists'][0]['name'],
        'album': album.replace("/", "-"),
        'url': track['track']['external_urls']['spotify'],
        'album_image': track["track"]["album"]["images"][0]["url"]
    }

@error_handler
def get_user_playlists(spotify_connection):
    printc("Retrieving playlist information...", 'white', 0.2)
    tracks = []  
    playlists = spotify_connection.current_user_playlists()
    for playlist in playlists["items"]:
        playlist_tracks = spotify_connection.playlist_items(playlist["id"])
        for track in playlist_tracks["items"]:
            track_dict = create_track_dict(track)
            tracks.append(track_dict)
    to_json(tracks, 'tracks.json', 'w')
    printc("Playlist information retrieved", 'white', 0.5)

@error_handler
def update_library():
    base_directory = load_from_config()
    
    if base_directory is None:
        printc("Base directory not configured. Initializing the folder...", "yellow", 0.2)
        get_base_directory()
        base_directory = load_from_config()
    
    printc("Updating Library...", "white", 0.5)
    
    tracks = from_json("tracks.json")
    for track in tracks:
        album_folder = os.path.join(base_directory, f"{track['artist']} - {track['album']}")
        if not os.path.exists(album_folder):
            os.makedirs(album_folder)
            set_folder_icon(album_folder, track['album_image'])
        
        os.chdir(album_folder)
        output_filename = "{} - {}.mp3".format(track['artist'], track['name']).replace("/","").replace("?", "").replace('"', "'")
        found = False
        for root, dirs, files in os.walk(album_folder):
            if output_filename in files:
                found = True
                break
        if not found:
            subprocess.run(['spotdl', track['url'], '--overwrite', 'skip'], check=True)

        os.chdir(base_directory)
    printc("Library up to date !", "green", 0.5)