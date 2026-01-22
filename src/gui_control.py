import asyncio, websockets, json
from src.utils import log
from src.config import config

async def _send_gui_command(command):
    """Internal function to send command to WBMS GUI via WebSocket."""
    uri = f"ws://{config.gui_ip}:{config.gui_port}/{config.gui_ws_path}"
    
    try:
        async with websockets.connect(uri) as websocket:
            log(f"Sending GUI command: {json.dumps(command)}")
            await websocket.send(json.dumps(command))
            return True
            
    except ConnectionRefusedError as e:
        log(f"Cannot connect to WBMS GUI at {uri}")
        log("Make sure GUI is running and WebSocket server is active")
        return False
    except Exception as e:
        log(f"Error sending GUI command: {type(e).__name__}: {e}")
        return False


async def start_recording():
    """Start WBMS recording and pinging."""
    log("Starting pinging...")
    ping_success = await _send_gui_command({"method": "start_pinging"})
    
    if not ping_success:
        log("Failed to start pinging")
        return False
    
    # Wait for pinging to initialize before starting recording
    await asyncio.sleep(0.5)
    
    log("Starting recording...")
    recording_success = await _send_gui_command({
        "method": "start_recording",
        "bin_size": 0.0
    })
    
    if recording_success:
        log("Recording started successfully")
    else:
        log("Failed to start recording")
    
    return recording_success


async def stop_recording():
    """Stop WBMS recording and pinging."""
    success = await _send_gui_command({"method": "stop_recording"})
    
    if success:
        
        # Wait before stopping pinging to ensure recording is fully stopped
        await asyncio.sleep(0.5)
        
        await _send_gui_command({"method": "stop_pinging"})
    else:
        log("Failed to stop recording")
    
    return success