import speech_recognition as sr
import pyttsx3
from deep_translator import GoogleTranslator  
from langdetect import detect
import threading

recognizer = sr.Recognizer()
tts = pyttsx3.init()

def transliterate_hindi_to_roman(hindi_text):
    """Convert Hindi (Devanagari) text to Roman script using translation (as a workaround)."""
    return GoogleTranslator(source="auto", target="en").translate(hindi_text)

def listen():
    """
    Continuously listen for speech until a valid phrase is recognized.
    Uses phrase_time_limit to allow for longer phrases.
    Returns the recognized text (translated to Romanized Hindi if needed).
    """
    while True:
        with sr.Microphone() as source:
            print("\n🎤 Listening for speech...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, phrase_time_limit=10)
            print("✅ Audio captured.")
        try:
            text = recognizer.recognize_google(audio, language="en-IN").strip()
            if text:
                print(f"📝 Speech recognized: {text}")
                detected_lang = detect(text)
                print(f"🌍 Detected language: {detected_lang}")
                if detected_lang == "hi":
                    romanized_text = transliterate_hindi_to_roman(text)
                    print(f"🔄 Transliterated Hindi Text: {romanized_text}")
                    return romanized_text
                return text
            else:
                print("⚠️ No text detected, retrying...")
        except sr.UnknownValueError:
            print("❌ Could not understand speech, retrying...")
        except sr.RequestError:
            print("⚠️ Speech recognition service is unavailable, retrying...")
        except Exception as e:
            print(f"🔥 Error: {str(e)}, retrying...")

def speak(text):
    """
    Convert text to speech.
    If the text is in Hindi (detected by langdetect), it is transliterated to Romanized Hindi.
    """
    try:
        if detect(text) == "hi":
            text = transliterate_hindi_to_roman(text)
        print(f"🗣️ AI is speaking: {text}")
        tts.say(text)
        tts.runAndWait()
        print("✅ Speech output completed.")
    except Exception as e:
        print(f"🔥 Error in speak: {str(e)}")
