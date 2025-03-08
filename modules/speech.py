import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator
from langdetect import detect

recognizer = sr.Recognizer()
tts = pyttsx3.init()

def transliterate_hindi_to_roman(hindi_text):
    """Ensure Hindi is always output in Roman script (not Devanagari)."""
    return GoogleTranslator(source="auto", target="en").translate(hindi_text)

def listen():
    """Capture audio, recognize speech, and translate to English if needed."""
    with sr.Microphone() as source:
        print("\n🎤 Listening for speech...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  
        audio = recognizer.listen(source)
        print("✅ Audio captured.")

    try:
        text = recognizer.recognize_google(audio, language="en-IN").strip()
        print(f"📝 Speech recognized: {text}")

        # If recognition yields an empty response, return an error message
        if not text:
            print("⚠️ No text detected.")
            return "Sorry, I couldn't understand."

        # Detect language
        detected_lang = detect(text)
        print(f"🌍 Detected language: {detected_lang}")

        # If the detected language is not English, translate it
        if detected_lang == "hi":
            romanized_text = transliterate_hindi_to_roman(text)
            print(f"🔄 Transliterated Hindi Text: {romanized_text}")
            return romanized_text  # Return Romanized Hindi
        
        return text  # If already in English, return as is

    except sr.UnknownValueError:
        print("❌ Could not understand speech.")
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        print("⚠️ Speech recognition service is unavailable.")
        return "Speech recognition service is unavailable."
    except Exception as e:
        print(f"🔥 Error: {str(e)}")
        return f"Error: {str(e)}"

def speak(text):
    """Convert text to speech and ensure Hindi is in Romanized format."""
    if detect(text) == "hi":
        text = transliterate_hindi_to_roman(text)  # Ensure Romanized Hindi

    print(f"🗣️ AI is speaking: {text}")
    tts.say(text)
    tts.runAndWait()
    print("✅ Speech output completed.")
