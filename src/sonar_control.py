import socket
from src.utils import log
from src.config import config

SONAR_IP = config.sonar_ip
SONAR_PORT = config.sonar_port

def send_commands_to_sonar(commands):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SONAR_IP, SONAR_PORT))
            welcome = sock.recv(1024).decode("ascii")
            log(f"Sonar welcome: {welcome}")

            all_success = True
            for cmd in commands:
                log(f"Sending: {cmd.strip()}")
                sock.sendall((cmd + "\n").encode("ascii"))
                reply = sock.recv(1024).decode("ascii").strip()
                log(f"Sonar reply: {reply}")

                if not reply.startswith(cmd.split()[0]):
                    log(f"Unexpected reply for command '{cmd.strip()}': {reply}")
                    all_success = False

            return all_success
    except Exception as e:
        log(f"Error sending commands to sonar: {e}")
        return False       
    

def send_external_trigger():
    cmd = "set_trigger_mode 4"

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((SONAR_IP, SONAR_PORT))
            welcome = sock.recv(1024).decode("ascii")
            
            log(f"Sending: {cmd.strip()}")
            sock.sendall((cmd + "\n").encode("ascii"))
            reply = sock.recv(1024).decode("ascii").strip()
            log(f"Sonar reply: {reply}")
            if reply.startswith(cmd.split()[0]):
                return True
            else:
                log(f"Unexpected reply for command '{cmd}': {reply}")
                return False
    except Exception as e:
        log(f"Error sending external ping command: {e}")
        return False