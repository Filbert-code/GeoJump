from kivy.core.window import Window


class PlayerInput:
    def __init__(self, player):
        self.player = player
        self._keyboard = Window.request_keyboard(
            self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.player.isMovingLeft = True
        elif keycode[1] == 'right':
            self.player.isMovingRight = True

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'left':
            self.player.isMovingLeft = False
        elif keycode[1] == 'right':
            self.player.isMovingRight = False