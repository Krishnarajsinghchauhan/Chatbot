import json
import time
import threading
import psutil
import schedule
from datetime import datetime, timedelta
from modules.speech import speak, listen
import os
import tkinter as tk
from tkinter import messagebox

# ------------------------------
# File Persistence for Reminders
# ------------------------------
REMINDER_FILE = "reminders.json"

if not os.path.exists(REMINDER_FILE):
    with open(REMINDER_FILE, "w") as f:
        json.dump([], f)

# ------------------------------
# 1. Reminder Management
# ------------------------------
def load_reminders():
    """Load reminders from the JSON file. Returns an empty list if the file is missing or corrupted."""
    try:
        with open(REMINDER_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_reminders(reminders):
    """Save the reminders list back to the JSON file."""
    with open(REMINDER_FILE, "w") as file:
        json.dump(reminders, file, indent=4)

def parse_time_str(time_str):
    """
    Parse user-input time formats into 24-hour format (HH:MM).
    Acceptable formats:
      - "10:52 PM", "10:52PM", "10:52 p.m."
      - "22:52"
    Returns formatted time as string or None if invalid.
    """
    normalized = time_str.strip().upper().replace('.', '')
    possible_formats = ["%I:%M %p", "%I:%M%p", "%H:%M"]
    for fmt in possible_formats:
        try:
            dt = datetime.strptime(normalized, fmt)
            return dt.strftime("%H:%M")  # Convert to 24-hour format
        except ValueError:
            continue
    return None

def set_reminder(time_str, message):
    """
    Set a reminder at a given time, store it in the reminders.json file, and schedule it.
    """
    formatted_time = parse_time_str(time_str)
    if not formatted_time:
        speak("Invalid time format. Please specify a valid format like '11:45 PM'.")
        return

    reminders = load_reminders()
    reminders.append({"time": formatted_time, "message": message})
    save_reminders(reminders)

    print(f"[Reminder] Reminder saved: {formatted_time} - {message}")

    # Schedule the reminder task
    schedule.every().day.at(formatted_time).do(trigger_reminder, message=message)
    speak(f"Reminder set for {formatted_time}: {message}")

def trigger_reminder(message):
    """
    Function that triggers the reminder and speaks it out.
    """
    speak(f"Reminder alert: {message}")
    print(f"⏰ Reminder Triggered: {message}")

    # Remove the reminder from the file after execution
    reminders = load_reminders()
    reminders = [rem for rem in reminders if rem["message"] != message]  # Remove executed reminder
    save_reminders(reminders)

def check_reminders():
    """
    Background thread to check reminders every 30 seconds.
    If a reminder matches the current time, it is triggered and removed.
    """
    while True:
        now = datetime.now().strftime("%H:%M")
        reminders = load_reminders()
        remaining_reminders = []

        for reminder in reminders:
            if reminder["time"] == now:
                trigger_reminder(reminder["message"])
            else:
                remaining_reminders.append(reminder)

        save_reminders(remaining_reminders)
        time.sleep(30)  # Check reminders every 30 seconds

# ------------------------------
# 2. Start Background Threads
# ------------------------------
def start_background_tasks():
    """
    Start background processes:
      - Reminder Checker
      - Scheduler Loop
    """
    threading.Thread(target=check_reminders, daemon=True).start()
    threading.Thread(target=run_scheduler, daemon=True).start()

def run_scheduler():
    """Runs scheduled tasks in an infinite loop."""
    while True:
        schedule.run_pending()
        time.sleep(1)

# ------------------------------
# 3. Background Process Monitor
# ------------------------------
def get_unused_tasks(threshold_cpu=0.5, threshold_mem=10):
    """
    Get a list of processes using minimal CPU and memory.
    - threshold_cpu: CPU usage below this threshold (%) is considered idle.
    - threshold_mem: Memory usage below this threshold (MB) is considered idle.
    """
    unused_tasks = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            cpu_usage = proc.info['cpu_percent']
            mem_usage_mb = proc.info['memory_info'].rss / (1024 * 1024)

            # Identify processes using low CPU and memory
            if cpu_usage < threshold_cpu and mem_usage_mb < threshold_mem:
                unused_tasks.append({"pid": proc.info['pid'], "name": proc.info['name']})

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

    return unused_tasks

def kill_process(pid):
    """Kill a process by its PID."""
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        print(f"[Task Manager] Process {proc.name()} (PID: {pid}) terminated successfully.")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print(f"[Task Manager] Unable to terminate process PID: {pid}")

def show_task_popup(unused_tasks):
    """
    Generate a pop-up asking the user if they want to kill unused tasks.
    """
    if not unused_tasks:
        return  # No unused tasks to notify about

    def on_confirm():
        """Terminate selected tasks on confirmation."""
        for task in unused_tasks:
            kill_process(task['pid'])
        messagebox.showinfo("Task Manager", "Unused tasks terminated successfully!")
        root.destroy()

    def on_cancel():
        """Ignore the unused tasks."""
        messagebox.showinfo("Task Manager", "No changes made. Unused tasks ignored.")
        root.destroy()

    # Create pop-up window
    root = tk.Tk()
    root.withdraw()  # Hide root window

    task_list = "\n".join([f"{task['name']} (PID: {task['pid']})" for task in unused_tasks])
    response = messagebox.askyesno(
        "Task Manager Alert",
        f"The following unused tasks are detected:\n\n{task_list}\n\nDo you want to terminate them?"
    )

    if response:
        on_confirm()
    else:
        on_cancel()

def monitor_unused_tasks(interval=60):
    """
    Monitor and identify unused tasks every 'interval' seconds.
    """
    while True:
        unused_tasks = get_unused_tasks()
        if unused_tasks:
            show_task_popup(unused_tasks)
        time.sleep(interval)

# ------------------------------
# 4. Start Task Monitor in Background
# ------------------------------
def start_task_monitor():
    """
    Start the unused task monitoring in the background.
    """
    threading.Thread(target=monitor_unused_tasks, daemon=True).start()

