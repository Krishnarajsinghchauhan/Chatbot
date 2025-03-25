import os
import subprocess
import psutil
import platform
import difflib
import threading

installed_apps_cache = {}

def scan_installed_apps():
    apps = {}
    system = platform.system()
    if system == "Windows":
        directories = [os.environ.get("ProgramFiles", "C:\\Program Files"),
                       os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"),
                       os.path.expanduser("~\\AppData\\Local\\Programs")]
        for directory in directories:
            if os.path.exists(directory):
                for root, _, files in os.walk(directory):
                    for file in files:
                        if file.lower().endswith(".exe"):
                            name = os.path.splitext(file)[0].lower()
                            full_path = os.path.join(root, file)
                            apps[name] = full_path
    elif system == "Darwin":
        directory = "/Applications"
        if os.path.exists(directory):
            for file in os.listdir(directory):
                if file.lower().endswith(".app"):
                    name = file.lower().replace(".app", "")
                    full_path = os.path.join(directory, file)
                    apps[name] = full_path
    else:
        directories = ["/usr/bin", "/usr/local/bin"]
        for directory in directories:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    full_path = os.path.join(directory, file)
                    if os.access(full_path, os.X_OK):
                        apps[file.lower()] = full_path
    return apps

def update_installed_apps_cache():
    global installed_apps_cache
    installed_apps_cache = scan_installed_apps()
    print(f"[PC Control] Found {len(installed_apps_cache)} applications.")

update_installed_apps_cache()

def find_app(query):
    if not installed_apps_cache:
        update_installed_apps_cache()
    query = query.lower().strip()
    app_names = list(installed_apps_cache.keys())
    matches = difflib.get_close_matches(query, app_names, n=1, cutoff=0.6)
    if matches:
        best_match = matches[0]
        return installed_apps_cache.get(best_match)
    return None

def open_app(app_query):
    path = find_app(app_query)
    if path:
        system = platform.system()
        print(f"[PC Control] Opening application: {path}")
        try:
            if system == "Windows":
                os.system(f'start "" "{path}"')
            elif system == "Darwin":
                os.system(f"open '{path}'")
            else:
                subprocess.Popen([path])
        except Exception as e:
            print(f"[PC Control] Error opening app: {e}")
    else:
        print(f"[PC Control] No application found matching '{app_query}'.")

def close_app(app_query):
    system = platform.system()
    running = [proc.info['name'] for proc in psutil.process_iter(attrs=['name'])]
    best_match = difflib.get_close_matches(app_query.lower(), [r.lower() for r in running], n=1, cutoff=0.6)
    if best_match:
        process_name = best_match[0]
        print(f"[PC Control] Closing process: {process_name}")
        try:
            if system == "Windows":
                os.system(f"taskkill /f /im {process_name}")
            else:
                os.system(f"pkill -f {process_name}")
        except Exception as e:
            print(f"[PC Control] Error closing app: {e}")
    else:
        print(f"[PC Control] No running process found matching '{app_query}'.")

def list_processes():
    processes = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def kill_process(app_query):
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if app_query.lower() in proc.info['name'].lower():
                proc.kill()
                print(f"[PC Control] Killed process: {proc.info}")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"[PC Control] Error killing process: {e}")
