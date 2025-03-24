import os
import subprocess
import psutil
import platform

def open_app(app_path):
    """
    Open an application using its path or a system command.
    For Windows, you can use the 'start' command.
    For macOS, use 'open', and for Linux use the app's command.
    """
    system = platform.system()
    try:
        if system == "Windows":
            os.system(f"start {app_path}")
        elif system == "Darwin":  # macOS
            os.system(f"open {app_path}")
        else:  # Linux or others
            subprocess.Popen(app_path.split())
    except Exception as e:
        print(f"Error opening app: {e}")

def close_app(process_name):
    """
    Close an application by its process name.
    For Windows, uses 'taskkill'. For Unix-based systems, uses 'pkill'.
    """
    system = platform.system()
    try:
        if system == "Windows":
            os.system(f"taskkill /f /im {process_name}")
        else:
            os.system(f"pkill -f {process_name}")
    except Exception as e:
        print(f"Error closing app: {e}")

def list_processes():
    """
    Return a list of currently running processes with their PID and name.
    """
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def kill_process(process_name):
    """
    Kill a process by its name.
    Iterates over running processes and terminates those matching the name.
    """
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if process_name.lower() in proc.info['name'].lower():
                proc.kill()
                print(f"Killed process: {proc.info}")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"Error killing process: {e}")
