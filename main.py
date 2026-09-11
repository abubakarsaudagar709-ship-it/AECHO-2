"""
AECHO - Main Entry Point
Abubakar's Enhanced Cognitive Handling Operator
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock

# Theme colors - black and gray
COLOR_BG = (0.05, 0.05, 0.05, 1)        # near-black background
COLOR_BUBBLE_AI = (0.18, 0.18, 0.18, 1)  # dark gray for AECHO's messages
COLOR_BUBBLE_USER = (0.28, 0.28, 0.28, 1)  # lighter gray for user messages
COLOR_TEXT = (0.9, 0.9, 0.9, 1)          # off-white text
COLOR_ACCENT = (0.5, 0.5, 0.5, 1)        # mid gray accent


class ChatBubble(Label):
    """A single chat message bubble, styled based on sender."""

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
    """Root layout: chat history + input bar."""

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_bg, size=self._update_bg)

        # Scrollable chat area
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

        # Input bar
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

        # First-boot intro will hook in here later (intro.py)
        Clock.schedule_once(self.boot_sequence, 0.5)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def boot_sequence(self, dt):
        """Placeholder - intro.py will handle real first-boot logic."""
        self.add_message("Hello world, I just born.", is_ai=True)

    def on_send(self, *args):
        user_text = self.text_input.text.strip()
        if not user_text:
            return
        self.add_message(user_text, is_ai=False)
        self.text_input.text = ""
        # brain.py will handle actual response logic later
        self.add_message("[brain.py not connected yet]", is_ai=True)

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
