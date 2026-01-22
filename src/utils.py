import os
from datetime import datetime
from src.config import config

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f"WBMS_{timestamp}.log"
log_filepath = os.path.join(config.logs_directory, log_filename)

os.makedirs(config.logs_directory, exist_ok=True)

def log(message):
    """Log message to both console and timestamped file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} {message}"
    
    print(log_entry)
    
    try:
        with open(log_filepath, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    except Exception as e:
        print(f"Error writing to log file: {e}")

def get_current_log_file():
    """Get current log file path."""
    return log_filepath