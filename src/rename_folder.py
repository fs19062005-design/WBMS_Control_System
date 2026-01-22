import os
from src.utils import log
from src.config import config

base_path = config.s7k_directory

def get_last_folder(path):
    try:
        subdirectories = [
            os.path.join(path, d)
            for d in os.listdir(path)
            if os.path.isdir(os.path.join(path, d))
        ]
        last_modified_folder = max(subdirectories, key=os.path.getmtime)
        return last_modified_folder
    except Exception as e:
        log(f"Error getting last folder: {e}")
        return None
    
def rename_last_folder(mission_name, phase_id):
    old_path = get_last_folder(base_path)
    if old_path is None:
        log(f"Error: Could not find folder to rename in {config.s7k_directory}")
        return
    
    try:
        old_name = os.path.basename(old_path)
        new_name = f"{mission_name}_{phase_id}_{old_name}"
        new_path = os.path.join(base_path, new_name)
        os.rename(old_path, new_path)
        log(f"Renamed last folder to {new_name}")

    except FileNotFoundError:
        log(f"Error: The file '{old_path}' was not found.")
    except Exception as e:
        log(f"An error occurred: {e}")  