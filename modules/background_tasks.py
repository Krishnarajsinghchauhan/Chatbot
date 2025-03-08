import time
import threading
import psutil
import schedule
import requests
import speech_recognition as sr
from datetime import datetime
from modules.speech import speak, listen

# Initialize recognizer
recognizer = sr.Recognizer()

def monitor_system():
    """Monitor CPU, RAM, and battery usage periodically."""
    while True:
        cpu_usage = psutil.cpu_percent(interval=5)
        ram_usage = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        battery_percent = battery.percent if battery else "N/A"
        print(f"🔋 CPU: {cpu_usage}%, RAM: {ram_usage}%, Battery: {battery_percent}%")
        time.sleep(60)  # Check every 60 seconds


def fetch_news():
    """Fetch latest news headlines."""
    try:
        response = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=YOUR_NEWS_API_KEY")
        news_data = response.json()
        headlines = [article['title'] for article in news_data['articles'][:3]]
        speak("Here are the top news headlines:")
        for headline in headlines:
            print(f"📰 {headline}")
            speak(headline)
    except Exception as e:
        print(f"⚠️ Error fetching news: {e}")


def set_reminder(time_str, message):
    """Set a reminder at a specific time."""
    def reminder_task():
        print(f"⏰ Reminder: {message}")
        speak(f"Reminder: {message}")
    schedule.every().day.at(time_str).do(reminder_task)


def background_listen():
    """Continuously listen for a wake-up command."""
    while True:
        print("🎤 Background listening...")
        text = listen()
        if "hey ai" in text.lower():
            speak("Yes, I am here! How can I help?")
        time.sleep(2)


def auto_updates():
    """Check for updates and sync data."""
    while True:
        print("🔄 Checking for AI updates...")
        # Simulated update check
        time.sleep(3600)  # Check every hour

# Scheduling tasks
schedule.every(30).minutes.do(fetch_news)
schedule.every().hour.do(auto_updates)

def run_scheduler():
    """Run scheduled tasks in the background."""
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start all background tasks
tasks = [
    threading.Thread(target=monitor_system, daemon=True),
    threading.Thread(target=background_listen, daemon=True),
    threading.Thread(target=run_scheduler, daemon=True)
]

for task in tasks:
    task.start()

while True:
    time.sleep(1)  # Keep the script running