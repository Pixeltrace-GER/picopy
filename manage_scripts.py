import subprocess
import time
import os

# Pfade zu den Python-Skripten
scripts = [
    "/home/pi/picopy/led_server.py",
    "/home/pi/picopy/picopy.py",
    "/home/pi/picopy/shutdown.py"
]

def is_running(script):
    """Check if a script is currently running."""
    try:
        # Use pgrep to check if there is any process matching the script path
        output = subprocess.check_output(['pgrep', '-f', script])
        return bool(output.strip())
    except subprocess.CalledProcessError:
        return False

def start_script(script):
    """Start a script using Python interpreter."""
    print(f"Starting {script}")
    subprocess.Popen(['/usr/bin/python3', script])

def main():
    while True:
        for script in scripts:
            if not is_running(script):
                start_script(script)
            else:
                print(f"{script} is running.")
        time.sleep(60)  # Überprüft alle 60 Sekunden

if __name__ == "__main__":
    main()

