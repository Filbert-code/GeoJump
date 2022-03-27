# make two circles that collide into each other and bounce around in the screen

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ListProperty


class GameView(Widget):
    def __init__(self, **kwargs):
        super(GameView, self).__init__(**kwargs)

        # keyboard setup
        self._keyboard = Window.request_keyboard(
            self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # player setup
        self.bounce_value = 12
        self.player = self.ids['player1']

        # platform setup
        self.platforms = [self.ids['plat1'],
                          self.ids['plat2'],
                          self.ids['plat3'],
                          self.ids['plat4']]

        # updates
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, *args):

        for platform in self.platforms:
            if self.player.collide_widget(platform):
                print('player pos: ', self.player.pos)
                print('platform pos: ', platform.pos)
                if self.player.velocity[1] <= 0 and self.player.pos[1] > platform.pos[1]:
                    self.player.velocity[1] *= -1
                    self.player.velocity[1] = + self.bounce_value


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            if self.player.velocity[0] > 0:
                self.player.velocity[0] -= 0.5
            self.player.velocity[0] -= 0.8
        elif keycode[1] == 'right':
            if self.player.velocity[0] < 0:
                self.player.velocity[0] += 0.5
            self.player.velocity[0] += 0.8

    def on_touch_down(self, touch):
        # clicking right side of the screen
        if touch.pos[0] > Window.width / 2:
            self.player.velocity[0] = 7.5
        else:
            self.player.velocity[0] = -7.5


class Player(Widget):
    velocity = ListProperty([0, -4])

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, *args):
        # print('player velocity: {}, {}'.format(self.velocity[0], self.velocity[1]))
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        # player has a constant decreasing vertical velocity (negative acceleration)
        self.velocity[1] -= 0.5
        # teleport to the other side if the player exits the left or right screen
        if self.x < -self.width:
            self.x = Window.width
        elif self.x > Window.width:
            self.x = -self.width


class Platform(Widget):
    pass



class GeoJumpApp(App):
    def build(self):
        return GameView()


if __name__ == '__main__':
    GeoJumpApp().run()