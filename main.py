"""
AECHO - Main Entry Point
Abubakar's Enhanced Cognitive Handling Operator
Connects brain, voice, intro, and wake word modules together.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock, mainthread

import brain
import voice
import intro
from wakeword import WakeWordListener, listen_for_command

# Theme colors - black and gray
COLOR_BG = (0.05, 0.05, 0.05, 1)
COLOR_BUBBLE_AI = (0.18, 0.18, 0.18, 1)
COLOR_BUBBLE_USER = (0.28, 0.28, 0.28, 1)
COLOR_TEXT = (0.9, 0.9, 0.9, 1)
COLOR_ACCENT = (0.5, 0.5, 0.5, 1)


class ChatBubble(Label):
    def __init__(self, text, is_ai=True, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint_y = None
        self.text_size = (Window.width * 0.75, None)
        self.halign = 'left' if is_ai else 'right'
        self.valign = 'middle'
        self.color = COLOR_TEXT
        self.padding = (15, 10)
        self.bind(texture_size=self._update_height)

        bubble_color = COLOR_BUBBLE_AI if is_ai else COLOR_BUBBLE_USER
        with self.canvas.before:
            Color(*bubble_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_height(self, *args):
        self.height = self.texture_size[1] + 20

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class AechoRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        self.memory = brain.load_memory()
        self.awaiting_setup_name = False
        self.awaiting_setup_password = False
        self.pending_owner_name = None

        self.scroll = ScrollView(size_hint=(1, 0.88))
        self.chat_log = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=10
        )
        self.chat_log.bind(minimum_height=self.chat_log.setter('height'))
        self.scroll.add_widget(self.chat_log)
        self.add_widget(self.scroll)

        input_bar = BoxLayout(size_hint=(1, 0.12), padding=8, spacing=8)

        self.text_input = TextInput(
            hint_text="Talk to AECHO...",
            multiline=False,
            background_color=COLOR_BUBBLE_AI,
            foreground_color=COLOR_TEXT,
            cursor_color=COLOR_TEXT,
            padding=(10, 10)
        )
        self.text_input.bind(on_text_validate=self.on_send)

        send_btn = Button(
            text="Send",
            size_hint=(0.25, 1),
            background_color=COLOR_ACCENT,
            color=COLOR_TEXT
        )
        send_btn.bind(on_press=self.on_send)

        input_bar.add_widget(self.text_input)
        input_bar.add_widget(send_btn)
        self.add_widget(input_bar)

        # Start wake word listener in the background
        self.wake_listener = WakeWordListener(on_wake_detected=self.on_wake_detected)
        self.wake_listener.start()

        Clock.schedule_once(self.boot_sequence, 0.5)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def boot_sequence(self, dt):
        """Runs intro logic on startup - first boot or returning owner."""
        intro_text = intro.run_intro(self.memory)
        self.add_message(intro_text, is_ai=True)

        if brain.is_first_run(self.memory):
            self.awaiting_setup_name = True
            self.add_message("What is your name?", is_ai=True)

    def on_send(self, *args):
        user_text = self.text_input.text.strip()
        if not user_text:
            return
        self.add_message(user_text, is_ai=False)
        self.text_input.text = ""
        self.handle_user_input(user_text)

    def handle_user_input(self, user_text):
        """Routes input either into first-time setup flow or normal brain logic."""
        if self.awaiting_setup_name:
            self.pending_owner_name = user_text
            self.awaiting_setup_name = False
            self.awaiting_setup_password = True
            self.add_message("Set a password for me.", is_ai=True)
            return

        if self.awaiting_setup_password:
            self.awaiting_setup_password = False
            response = intro.complete_first_setup(
                self.memory, self.pending_owner_name, user_text
            )
            self.add_message(response, is_ai=True)
            return

        # Normal conversation, once setup is done
        response = brain.process_input(self.memory, user_text)
        self.add_message(response, is_ai=True)
        voice.speak(response)

    @mainthread
    def on_wake_detected(self):
        """Called from the background wake word thread when 'AECHO' is heard."""
        self.add_message("(wake word detected, listening...)", is_ai=True)
        command = listen_for_command()
        if command:
            self.add_message(command, is_ai=False)
            self.handle_user_input(command)
        else:
            self.add_message("I didn't catch that.", is_ai=True)

    def add_message(self, text, is_ai=True):
        bubble = ChatBubble(text=text, is_ai=is_ai)
        self.chat_log.add_widget(bubble)
        self.scroll.scroll_y = 0


class AechoApp(App):
    def build(self):
        Window.clearcolor = COLOR_BG
        return AechoRoot()


if __name__ == '__main__':
    AechoApp().run()
