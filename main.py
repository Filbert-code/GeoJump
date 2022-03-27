# make two circles that collide into each other and bounce around in the screen
from random import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from Platform import Platform
from Player import Player
from PlayerInput import PlayerInput

# Make Sure This Is Always the last import
from kivy import Config
Config.set('graphics', 'multisamples', '0')


class GameView(Widget):
    def __init__(self, **kwargs):
        super(GameView, self).__init__(**kwargs)

        # player setup
        self.player = Player(pos=(0, 100), size=(60, 60))
        self.add_widget(self.player)
        self.bounce_value = 15
        self.player.gravity = 0.4

        # user keyboard input setup
        self._keyboard = PlayerInput(self.player)

        # platform setup
        p1 = Platform(pos=(0, 0), size=(1500, 10))
        self.add_widget(p1)
        self.platforms = [p1]
        self.platform_height = 50
        self.create_platforms(10, 50)

        # updates
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, *args):
        for platform in self.platforms:
            self.platform_player_collision(platform)
            self.move_platform(platform)
            self.discard_unseen_platforms(platform)

    def on_touch_down(self, touch):
        # clicking right side of the screen
        if touch.pos[0] > Window.width / 2:
            self.player.velocity[0] = 7.5
        else:
            self.player.velocity[0] = -7.5

    def create_platforms(self, numOfPlatforms, separation):
        for i in range(numOfPlatforms):
            p = Platform(pos=(random()*800, self.platform_height + separation), size=(150, 10))
            Clock.schedule_interval(p.update, 1 / 60.)
            self.platform_height += 50
            self.add_widget(p)
            self.platforms.append(p)

    def platform_player_collision(self, platform):
        # check player collision with platforms
        if self.player.collide_widget(platform):
            if self.player.velocity[1] < -2.5 and self.player.pos[1] > platform.pos[1] - platform.height / 2:
                self.player.velocity[1] = self.bounce_value

    def move_platform(self, platform):
        # update height of platforms
        if self.player.pos[1] > 280:
            platform.pos[1] -= 5

    def discard_unseen_platforms(self, platform):
        # delete platform objects that fall below the screen
        if platform.pos[1] < -self.player.height:
            self.remove_widget(platform)
            self.platforms.pop(0)
            self.create_platforms(1, 50)


class GeoJumpApp(App):
    def build(self):
        return GameView()


if __name__ == '__main__':
    GeoJumpApp().run()