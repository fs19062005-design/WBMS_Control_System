import yaml

class Config:
    def __init__(self):
        self.config_file = "config.yaml"
        self._load_config()

    def _load_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                config_data = yaml.safe_load(file)
            
            # Network
            self.sonar_ip = config_data['sonar_ip']
            self.sonar_port = config_data['sonar_port']
            self.gui_ip = config_data['gui_ip']
            self.gui_port = config_data['gui_port']
            self.gui_ws_path = config_data['gui_ws_path']
            self.backseat_ip = config_data['backseat_ip']
            self.backseat_port = config_data['backseat_port']
            
            # Paths
            self.presets_file = config_data['presets_file']
            self.logs_directory = config_data.get('logs_directory')
            self.s7k_directory = config_data['s7k_directory']
            self.params_directory = config_data['params_directory']
            
            # Timing
            self.poll_interval = config_data.get('poll_interval')
            self.recording_delay = config_data['recording_delay']
            
        except FileNotFoundError:
            print(f"Config file {self.config_file} not found!")
            raise
        except KeyError as e:
            print(f"Missing config key: {e}")
            raise
        except Exception as e:
            print(f"Error loading config: {e}")
            raise

config = Config()