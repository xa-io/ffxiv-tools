"""
Process ID Monitor

A utility that monitors specified processes and plays an alert sound if any process stops running.
This is useful for monitoring critical processes and getting immediate notification if they crash.

Dependencies:
    - psutil: For process monitoring
    - playsound: For playing alert sounds
"""

# Standard library imports
import time

# Third-party imports
import psutil
from playsound import playsound

# requirements: pip install psutil playsound

# List of process IDs to monitor.
# Update these values on each reboot as needed.
# Replace with the PIDs of the processes you want to monitor.
PIDS_TO_MONITOR = [12345, 67890] 

# Path to the audio file for the alert sound.
# Update this path to point to your desired alert sound file.
ALERT_AUDIO_PATH = r"E:\!gil\Crash Detected.mp3"

def check_processes(pids):
    """
    Checks if each process in the list is running.
    Returns (True, None) if all processes are active,
    or (False, pid) for the first PID that is no longer running.
    """
    for pid in pids:
        if not psutil.pid_exists(pid):
            return False, pid
    return True, None

def main():
    print("Process monitor started.")
    print("Monitoring the following PIDs:", PIDS_TO_MONITOR)
    
    # Continuously monitor the given processes.
    while True:
        all_running, crashed_pid = check_processes(PIDS_TO_MONITOR)
        if not all_running:
            print(f"Process with PID {crashed_pid} has stopped!")
            print("Triggering audio alert. Press Ctrl+C to stop the script.")
            # Once a process stops, play the alert repeatedly every 5 seconds.
            while True:
                try:
                    playsound(ALERT_AUDIO_PATH)
                except Exception as e:
                    print("Error playing sound:", e)
                time.sleep(300)
        # Check processes every second.
        time.sleep(1)

if __name__ == "__main__":
    main()
