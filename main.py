from modules.ai_chat import chat_with_ai
from modules.speech import listen, speak
from modules.pc_control import open_apps
from modules.browser import search_google
from modules.background_tasks import start_background_tasks, set_reminder, load_reminders, save_reminders, start_task_monitor
from modules.brain import process_memory_input, answer_memory_query
import threading

def main():
    # Start all background tasks (system monitoring, background listening, scheduler, process monitoring)
    threading.Thread(target=start_background_tasks, daemon=True).start()

    # Start monitoring for idle or high resource processes (if implemented)
    start_task_monitor()

    speak("Hello, how can I assist you today?")
    while True:
        command = listen()
        if not command:
            continue
        command = command.lower()

        # Check if the command is meant for the brain (teaching or memory query)
        memory_response = process_memory_input(command)
        if memory_response:
            speak(memory_response)
            continue

        memory_query = answer_memory_query(command)
        if memory_query:
            speak(memory_query)
            continue

        # PC Control commands
        if "open" in command:
            app_name = command.replace("open ", "")
            open_apps(app_name)

        elif "close" in command:
            app_name = command.replace("close ", "")
            close_apps(app_name)

        # Web search command
        elif "search" in command:
            query = command.replace("search ", "")
            search_google(query)

        # Reminder commands
        elif "set reminder" in command or "remind me" in command:
            # Expecting a command like "remind me at 10:52 p.m. to call John"
            words = command.split()
            if "at" in words:
                time_index = words.index("at") + 1
                if time_index < len(words):
                    # Check if the next token is "am" or "pm" to form a full time string
                    if len(words) > time_index + 1 and words[time_index + 1] in ["am", "pm"]:
                        time_str = words[time_index] + " " + words[time_index + 1]
                        message = " ".join(words[time_index + 2:])
                    else:
                        time_str = words[time_index]
                        message = " ".join(words[time_index + 1:])
                    set_reminder(time_str, message)
                else:
                    speak("Please specify the time for the reminder.")
            else:
                speak("Please specify the time for the reminder.")

        # System usage command
       

        # Exit command
        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        # Fallback: Use AI chat to generate a response
        else:
            response = chat_with_ai(command)
            speak(response)

if __name__ == "__main__":
    main()
