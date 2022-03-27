# make two circles that collide into each other and bounce around in the screen
from random import random

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
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
        p1 = Platform(pos=(0, 0), size=(1500, 10))
        self.add_widget(p1)
        self.platforms = [p1]
        p_height = 50
        for i in range(10):
            p = Platform(pos=(random()*800, p_height), size=(150, 10))
            Clock.schedule_interval(p.update, 1 / 60.)
            p_height += 50
            self.add_widget(p)
            self.platforms.append(p)

        # updates
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, *args):
        for platform in self.platforms:
            # check player collision with platforms
            if self.player.collide_widget(platform):
                # print('player pos: ', self.player.pos)
                # print('platform pos: ', platform.pos)
                if self.player.velocity[1] <= 0 and self.player.pos[1] > platform.pos[1]:
                    self.player.velocity[1] *= -1
                    self.player.velocity[1] = + self.bounce_value

            # update height of platforms
            if self.player.pos[1] > 300:
                print('changed position')
                platform.pos[1] -= 1





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
    velocity = ListProperty([0, -7.5])

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
    def __init__(self, **kwargs):
        super(Platform, self).__init__(**kwargs)
        self.pos = kwargs['pos']
        self.size = kwargs['size']
        with self.canvas:
            Color(1., 1., 1.)
            Rectangle(pos=self.pos, size=self.size)

    def update(self, *args):
        self.draw()

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1., 1., 1.)
            Rectangle(pos=self.pos, size=self.size)


class GeoJumpApp(App):
    def build(self):
        return GameView()


if __name__ == '__main__':
    GeoJumpApp().run()