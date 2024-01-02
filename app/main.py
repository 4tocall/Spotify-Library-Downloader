from app.auth import connect_to_spotify, validate_environment_variables
from app.functions import get_user_playlists, update_library
from app.library_config import get_base_directory
from app.utils import printc
import argparse

def show_menu():
    printc("Select an option".center(40, "-"), "white")
    printc("[1] Configure library folder", "cyan")
    printc("[2] Retrieving Spotify Library Information", "cyan")
    printc("[3] Update Library !", "cyan")
    printc("[0] Quit", "cyan")

def app():
    parser = argparse.ArgumentParser(description='Spotify Library Downloader')
    parser.add_argument('-update', action='store_true')
    
    args = parser.parse_args()

    update = args.update

    printc("Logging in to Spotify...", "white", 0.2)
    required_env_vars = ["SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET", "SPOTIPY_REDIRECT_URI"]
    try:
        validate_environment_variables(required_env_vars)
        printc("Validating environment variables...", "white", 0.2)
        spotify_connection = connect_to_spotify()

        if spotify_connection:
            if update:
                get_user_playlists(spotify_connection)
                update_library()
            else:
                printc("Program started successfully.", "white", 0.5)
                while True:
                    show_menu()       
                    choice = input()
                    if choice == "1":
                        get_base_directory()
                    elif choice == "2":
                        get_user_playlists(spotify_connection)
                    elif choice == "3":
                        update_library()  
                    elif choice == "0":
                        printc("Pye !", "magenta")
                        break
                    else:
                        printc("Invalid choice. Please enter a valid number.", "red", 0.3)
        else:
            printc("Unable to connect to Spotify. Please check authentication information.", "red")
    except ValueError as ve:
        printc(str(ve), 'red')

if __name__ == "__main__":
    app()