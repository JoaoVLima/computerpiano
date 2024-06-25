from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window


class KeyDown(App):
    def build(self):
        self.pressed_keys = {}  # Dictionary to keep track of pressed keys
        Window.bind(on_key_down=self.key_down_action)
        Window.bind(on_key_up=self.key_up_action)
        return Widget()

    def key_down_action(self, window, key, scancode, codepoint, modifier):
        # Add the key to the dictionary
        self.pressed_keys[key] = (window, key, scancode, codepoint, modifier)
        print(len(self.pressed_keys), self.pressed_keys)

    def key_up_action(self, window, key, scancode):
        # Remove the key from the dictionary
        if key in self.pressed_keys:
            del self.pressed_keys[key]
        print(len(self.pressed_keys), self.pressed_keys)


if __name__ == '__main__':
    KeyDown().run()
