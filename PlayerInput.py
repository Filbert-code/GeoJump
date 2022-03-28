from kivy.core.window import Window


class PlayerInput:
    def __init__(self, player):
        self.player = player
        self.keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self._on_keyboard_down)
        self.keyboard.bind(on_key_up=self._on_keyboard_up)

    def _keyboard_closed(self):
        print('My keyboard have been closed!')
        self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.player.isMovingLeft = True
        elif keycode[1] == 'right':
            self.player.isMovingRight = True
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'left':
            self.player.isMovingLeft = False
        elif keycode[1] == 'right':
            self.player.isMovingRight = False