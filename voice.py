"""
AECHO - Voice Module
Handles text-to-speech (using Android's built-in TTS engine for now)
and speech-to-text (converting user's spoken words to text).
"""

from plyer import tts
import speech_recognition as sr


def speak(text):
    """
    Converts text to speech using Android's built-in TTS engine.
    This is a placeholder voice - will be swapped for AECHO's personal
    cloned voice (ElevenLabs) later once that's set up.
    """
    try:
        tts.speak(message=text)
    except NotImplementedError:
        # Happens when testing on non-Android (e.g. plain PC/Termux)
        print(f"[AECHO]: {text}")
    except Exception as e:
        print(f"[AECHO voice error]: {e}")
        print(f"[AECHO - fallback text]: {text}")


def listen():
    """
    Captures spoken input from the microphone and converts it to text.
    Returns the recognized text, or None if nothing understood.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
            return recognizer.recognize_google(audio)
        except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
            return None
