import requests
from src.utils import log
from src.config import config

BASE_URL = f"http://{config.backseat_ip}:{config.backseat_port}"

_last_phase_info = None

def get_current_phase_info():

    global _last_phase_info
    url = f"{BASE_URL}/missions/current"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        mission = resp.json()
        _last_phase_info = mission
        return mission
    except Exception as e:
        log(f"Error fetching current phase info: {e}")
        return None

def get_current_phase_id():

    phase_info = get_current_phase_info()
    if phase_info is None:
        return None
    return phase_info.get("currentPhaseId")

def get_current_mission_name():

    phase_info = get_current_phase_info()
    if phase_info is None:
        return "Unknown"
    return phase_info.get("name", "Unknown")

def is_phase_enabled():

    phase_info = get_current_phase_info()
    if phase_info is None:
        log("WARNING: Could not get phase info from Backseat API")
        return False
    
    state = phase_info.get("state")
    phase_name = phase_info.get("name", "Unknown")
    
    if state == "Enabled":
        return True
    else:
        return False
