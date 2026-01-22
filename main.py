import yaml, asyncio, glob, os
from src.backseat_api import get_current_phase_id, get_current_mission_name, is_phase_enabled
from src.sonar_control import send_commands_to_sonar, send_external_trigger
from src.utils import log
from src.gui_control import start_recording, stop_recording
from src.config import config
from src.rename_folder import rename_last_folder


def normalize_keys(d):
    """Normalize dictionary keys to strings."""
    return {str(k): v for k, v in d.items()} if isinstance(d, dict) else d


def load_phase_to_preset(mission_name=None):
    """Load phase_to_preset mapping for specific mission. Returns empty dict if file not found."""
    if not mission_name:
        return {}
    
    pattern = os.path.join(config.params_directory, f"WBMS-VS_*{mission_name}.yaml")
    matching_files = glob.glob(pattern)

    if not matching_files:
        return {} 
    
    settings_file = matching_files[0]

    try:
        with open(settings_file, "r", encoding="utf-8") as f:
            log(f"Loading settings from: {settings_file}")
            data = yaml.safe_load(f)

            if data and 'WBMS_params' in data:
                return normalize_keys(data['WBMS_params'])
            else:
                return {}
    except Exception as e:
        log(f"Error loading {settings_file}: {e}")
        return {}


def load_presets():
    try:
        with open(config.presets_file, "r", encoding="utf-8") as f:
            return normalize_keys(yaml.safe_load(f) or {})
    except FileNotFoundError:
        log(f"Presets file not found: {config.presets_file}")
        return {}
    except Exception as e:
        log(f"Error loading {config.presets_file}: {e}")
        return {}


async def main():
    last_phase = None
    last_phase_had_preset = False
    last_phase_enabled = None
    current_mission_name = None
    phase_to_preset = {}
    presets = load_presets()

    send_external_trigger()
    await stop_recording()

    log("Mission phase tracker with recording control started")

    try:
        while True:
            try:
                phase_id = get_current_phase_id()
            except Exception as e:
                log(f"Error getting phase ID: {e}")
                await asyncio.sleep(config.poll_interval)
                continue

            if phase_id is not None:
                mission_name = get_current_mission_name()
                phase_enabled = is_phase_enabled()
                
                if mission_name != current_mission_name:
                    phase_to_preset = load_phase_to_preset(mission_name)
                    current_mission_name = mission_name
                    
                    if phase_to_preset: 
                        log(f"Mission changed: '{mission_name}' (sonar enabled)")
                    else: 
                        log(f"Mission changed: '{mission_name}' (sonar disabled - no config file)")
                
                phase_changed = str(phase_id) != str(last_phase)
                state_changed = phase_enabled != last_phase_enabled
                
                if phase_to_preset and (phase_changed or state_changed):
                    if phase_changed:
                        log(f"Phase changed: {phase_id} ('{mission_name}')")
                    if state_changed:
                        log(f"Phase state changed: {'enabled' if phase_enabled else 'disabled'}")
                    
                    # Stop current recording before switching presets
                    await stop_recording()
                    
                    # Small delay to ensure recording stops completely
                    await asyncio.sleep(config.recording_delay)
                    
                    # Rename previous phase folder ONLY if it had a preset (was recording)
                    if last_phase is not None and last_phase_had_preset:
                        rename_last_folder(mission_name, last_phase)
                    
                    preset = phase_to_preset.get(str(phase_id))
                    current_phase_has_preset = False

                    if preset:
                        commands = presets.get(str(preset))
                        if commands:
                            if phase_enabled:                           
                                send_commands_to_sonar(commands)
                                log(f"Applied preset '{preset}'")
                                    
                                recording_started = await start_recording()
                                if recording_started:
                                    current_phase_has_preset = True
                                else:
                                    log(f"Recording failed")    
                            else:
                                log(f"Preset '{preset}' not applied (phase disabled)")
                        else:
                            log(f"No commands found for preset '{preset}'")
                    else:
                        log(f"No preset assigned for phase {phase_id}")

                    last_phase = phase_id
                    last_phase_had_preset = current_phase_has_preset
                    last_phase_enabled = phase_enabled

            await asyncio.sleep(config.poll_interval)

    except KeyboardInterrupt:
        await stop_recording()
        log("Mission phase watcher stopped")


if __name__ == "__main__":
    asyncio.run(main())