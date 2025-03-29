import os
import subprocess
import psutil
import platform
import difflib
import speech_recognition as sr
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

def find_app(query):
    if not installed_apps_cache:
        update_installed_apps_cache()
    query = query.lower().strip()
    app_names = list(installed_apps_cache.keys())
    matches = difflib.get_close_matches(query, app_names, n=1, cutoff=0.6)
    if matches:
        return installed_apps_cache.get(matches[0])
    return None

def open_apps(app_queries):
    for app_query in app_queries:
        path = find_app(app_query)
        if path:
            print(f"[PC Control] Opening application: {path}")
            try:
                if platform.system() == "Windows":
                    os.system(f'start "" "{path}"')
                elif platform.system() == "Darwin":
                    os.system(f"open '{path}'")
                else:
                    subprocess.Popen([path])
            except Exception as e:
                print(f"[PC Control] Error opening app: {e}")
        else:
            print(f"[PC Control] No application found matching '{app_query}'.")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for app commands...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            if "open" in command:
                app_names = command.replace("open", "").strip().split(" and ")
                open_apps(app_names)
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
        except sr.RequestError:
            print("Speech recognition service is down.")

def continuous_listening():
    while True:
        recognize_speech()

if __name__ == "__main__":
    update_installed_apps_cache()
    threading.Thread(target=continuous_listening, daemon=True).start()