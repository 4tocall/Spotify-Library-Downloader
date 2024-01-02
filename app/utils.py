import time, json
from AppKit import NSImage, NSWorkspace
from requests import get
from Foundation import NSData
from app.auth import os
from PIL import Image
from io import BytesIO

def printc(message, color='white', duration=None):
    COLORS = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '',
        'gray': '\033[90m',
    }

    if color not in COLORS:
        color = 'white'

    print(f"{COLORS[color]}{message}{COLORS['reset']}")

    if duration is not None:
        time.sleep(duration)

def to_json(data, file, mode):
    try:
        with open(file, mode, encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")
    except Exception as e:
        print(f"An error occurred while saving {data}: {e}")

def from_json(file):
    try:
        with open(file, 'r') as file:
            config_data = json.load(file)
            return config_data
    except Exception as e:
        print(f"Error loading {file}: {e}")
        return None

def set_folder_icon(folder_path, image_url):
    try:
        response = get(image_url)
        image_data = Image.open(BytesIO(response.content))
        image_data.thumbnail((256, 256)) 
        output_buffer = BytesIO()
        image_data.save(output_buffer, format="PNG")
        compressed_image_data = NSData.dataWithBytes_length_(output_buffer.getvalue(), len(output_buffer.getvalue()))
        image = NSImage.alloc().initWithData_(compressed_image_data)
        NSWorkspace.sharedWorkspace().setIcon_forFile_options_(image, folder_path, 0)

        printc(f'Album image for "{os.path.basename(os.path.normpath(folder_path))}" folder defined.', "white")
    except Exception as e:
        printc(f"An error occurred while setting the icon for the folder '{folder_path}': {e}", "red")
