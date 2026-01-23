# S7K-Maker: WBMS Automation

Software project for the replacement of the default WBMS Sonar Integration system. Allows the generation of s7k files with all possible types of data during the mission.

## Features

* Monitor current mission and phase via Backseat API
* Automatic application of sonar presets
* Management of the S7K data recording process
* Automatic data folder renaming after phase and mission
* Dynamic configuration loading per mission

## Installation

Copy all the components to the computer in AUV.
Install and configure Norbit WBMS GUI for headless usage on the same machine.
Create a service in systemd for automatic program launch on boot.
main.py is the entry point for the project; this file should be launched before mission start for proper sonar operation.

## Configuration

After installation, edit the required configuration parameters.
Correct parameters in config.yaml, which are critical for proper function:
sonar_ip            #IP address of the WBMS sonar inside AUV
sonar_port          #Port of the WBMS sonar for control commands
gui_ip              #IP address of the computer with WBMS GUI running (normally localhost)
gui_port            #Port for control commands for WBMS GUI
backseat_ip         #IP address of the computer with the backseat driver interface active
backseat_port       #Port for the Backseat Driver API
logs_directory      #Directory for logs storage
s7k_directory       # Directory where s7k files are saved (configured in WBMS GUI initially)
params_directory    #Directory where mission-specific yaml files with sonar presets are stored

## Project Structure

```
WBMS_Control_System/
├── main.py              # Main monitoring loop and entry point
├── config.yaml          # Application configuration
├── presets.yaml         # Sonar settings list for each preset
├── requirements.txt     # Dependencies
└── src/
   ├── backseat_api.py     # Current phase information source
   ├── sonar_control.py    # Sonar settings management
   ├── gui_control.py      # Recording management
   ├── rename_folder.py    # Folder renaming
   ├── config.py           # Configuration loader
   └── utils.py            # Logging utilities
```

## Mission Configuration Files

Place in params_directory:

WBMS-VS_params_<mission_name>.yaml

WBMS_params:
  13: "3-50_400_140_ED_512_2048"
  17: "3-50_400_140_ED_512_2048"
  19: "3-50_400_140_ED_512_2048"

Search pattern: WBMS-VS_params_*{mission_name}*.yaml

## Workflow

1. Get the current phase and mission from the Backseat API.
2. If mission changed → load new configuration
3. If phase/state changed → stop current recording.
4. Apply the corresponding preset.
5. Start S7K data recording.
6. Rename the previous phase folder.

## Requirements

* Python 3.10+
* PyYAML 6.0.2
* requests 2.32.5
* websockets 15.0.1

## Author

Feliks Sizemskii