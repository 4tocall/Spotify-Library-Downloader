from dotenv import load_dotenv
import os, spotipy
from app.utils import printc, error_handler

load_dotenv()

@error_handler
def validate_environment_variables(required_vars):
    for var in required_vars:
        if var not in os.environ:
            raise ValueError(f"Missing environment variable: {var}")

@error_handler
def connect_to_spotify():
    sp = spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope='playlist-read-private',
            cache_path=os.path.join(".", ".cache")
        )
    )
    printc("Connected to Spotify.", 'white', 0.2)
    return sp