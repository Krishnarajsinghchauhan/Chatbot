import json
import time
import threading
import psutil
import schedule
from datetime import datetime, timedelta
from modules.speech import speak, listen
import os

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
