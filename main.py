from modules.ai_chat import chat_with_ai
from modules.speech import listen, speak
from modules.pc_control import open_app, close_app
from modules.browser import search_google

def main():
    speak("Hello, how can I assist you today?")
    while True:
        command = listen()
        
        if "open" in command:
            app_name = command.replace("open ", "")
            open_app(app_name)

        elif "close" in command:
            app_name = command.replace("close ", "")
            close_app(app_name)

        elif "search" in command:
            query = command.replace("search ", "")
            search_google(query)

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        
        else:
            response = chat_with_ai(command)
            speak(response)

if __name__ == "__main__":
    main()