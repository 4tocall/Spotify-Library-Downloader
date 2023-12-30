from app.auth import os
from app.utils import printc, from_json, to_json
os.environ['TK_SILENCE_DEPRECATION'] = '1'
from tkinter import Tk, filedialog

def get_base_directory():
    root = Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    print("Select the base directory folder...")
    base_directory = filedialog.askdirectory(title="Select Base Directory")
    save_to_config(base_directory)
    printc("Base directory configured successfully.", "green")
    root.destroy()
    return base_directory

def save_to_config(base_directory):
    config_data = {"base_directory": base_directory}
    to_json(config_data, "config.json", "w")
    printc("Base directory saved to the config file.", 'green')

def load_from_config():
    config_data = from_json("config.json")
    base_directory = config_data.get("base_directory")
    printc("Base directory loaded from the config file.", 'white')
    return base_directory