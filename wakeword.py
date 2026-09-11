"""
AECHO - Wake Word Module
Listens continuously for "AECHO" and triggers the island popup + activates listening.
NOTE: For true home-screen (background) detection on Android, this loop must run
inside a foreground Service (handled via buildozer.spec service entry) so Android
doesn't kill it when the app isn't in front. This file contains the detection logic;
service wiring happens in buildozer.spec (added when we do the final build file).
"""

import speech_recognition as sr
import threading
import time

WAKE_WORD = "aecho"
LISTEN_TIMEOUT = 5          # seconds to wait for phrase to start
PHRASE_TIME_LIMIT = 4       # max seconds for a single phrase


class WakeWordListener:
    """Continuously listens in the background for the wake word."""

    def __init__(self, on_wake_detected):
        """
        on_wake_detected: callback function called with no args
        when 'AECHO' is heard. Used to trigger island popup + start
        active listening for the actual command.
        """
        self.on_wake_detected = on_wake_detected
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self._running = False
        self._thread = None

        # Calibrate for background noise once at startup
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def start(self):
        """Start the background listening loop in a separate thread."""
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the background listening loop."""
        self._running = False

    def _listen_loop(self):
        while self._running:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(
                        source,
                        timeout=LISTEN_TIMEOUT,
                        phrase_time_limit=PHRASE_TIME_LIMIT
                    )
                heard_text = self.recognizer.recognize_google(audio).lower()

                if WAKE_WORD in heard_text:
                    self.on_wake_detected()

            except sr.WaitTimeoutError:
                # No speech detected in timeout window, just keep looping
                continue
            except sr.UnknownValueError:
                # Speech was unintelligible, ignore and keep listening
                continue
            except sr.RequestError:
                # Network/recognition service issue, back off briefly
                time.sleep(2)
                continue


def listen_for_command():
    """
    Called right after wake word is detected.
    Captures the actual command/question that follows.
    Returns the recognized text, or None if nothing understood.
    """
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    try:
        with microphone as source:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
        return recognizer.recognize_google(audio)
    except (sr.WaitTimeoutError, sr.UnknownValueError, sr.RequestError):
        return None
