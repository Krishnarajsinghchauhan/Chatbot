from modules.ai_chat import chat_with_ai
from modules.speech import listen, speak
from modules.pc_control import open_app, close_app
from modules.browser import search_google
from modules.background_tasks import start_background_tasks, set_reminder, get_system_usage, load_reminders, save_reminders
from datetime import datetime
from modules.brain import process_memory_command, answer_memory_query
import threading

def main():
    # Start background tasks in a daemon thread
    threading.Thread(target=start_background_tasks, daemon=True).start()

    speak("Hello, how can I assist you today?")
    while True:
        command = listen()
        if not command:
            continue
        command = command.lower()

        # Check if it's a memory-teaching command
        memory_response = process_memory_command(command)
        if memory_response:
            speak(memory_response)
            continue

        # Check if it's a memory query
        memory_query = answer_memory_query(command)
        if memory_query:
            speak(memory_query)
            continue

        if "open" in command:
            app_name = command.replace("open ", "")
            open_app(app_name)

        elif "close" in command:
            app_name = command.replace("close ", "")
            close_app(app_name)

        elif "search" in command:
            query = command.replace("search ", "")
            search_google(query)

        elif "set reminder" in command or "remind me" in command:
            # Expecting command like "remind me at 10:52 p.m. to call John"
            words = command.split()
            if "at" in words:
                time_index = words.index("at") + 1
                if time_index < len(words):
                    # Capture time as two tokens (e.g., "10:52 p.m." may come as two tokens)
                    if len(words) > time_index + 1 and words[time_index+1] in ["am", "pm"]:
                        time_str = words[time_index] + " " + words[time_index+1]
                        message = " ".join(words[time_index+2:])
                    else:
                        time_str = words[time_index]
                        message = " ".join(words[time_index+1:])
                    set_reminder(time_str, message)
                else:
                    speak("Please specify the time for the reminder.")
            else:
                speak("Please specify the time for the reminder.")

        elif "usage" in command or "system status" in command:
            speak(f"Current system usage is: {get_system_usage()}")

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        else:
            response = chat_with_ai(command)
            speak(response)

if __name__ == "__main__":
    main()
