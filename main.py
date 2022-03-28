# make two circles that collide into each other and bounce around in the screen
from random import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, ReferenceListProperty
from MovingPlatform import MovingPlatform
from Platform import Platform
from Player import Player

# Make Sure This Is Always the last import
from kivy import Config
Config.set('graphics', 'multisamples', '0')


class GameView(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(GameView, self).__init__(**kwargs)
        # used for pausing the game
        self.game_has_started = False

        # player setup
        self.player = Player(pos=(0, 200), size=(60, 60))
        self.add_widget(self.player)
        self.bounce_value = 0
        self.player.velocity[1] = 0
        self.player.gravity = 0

        # user keyboard input setup
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self._on_keyboard_down)
        self.keyboard.bind(on_key_up=self._on_keyboard_up)

        # platform setup
        p1 = Platform(pos=(0, 0), size=(1500, 10))
        self.add_widget(p1)
        self.platform_group = [p1]
        self.create_platforms(20, 50)
        self.background_movement_speed = 5

        # updates
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, *args):
        # don't update if game hasn't started
        if not self.game_has_started:
            return
        # collision detections
        for platform in self.platform_group:
            self.platform_player_collision(platform)
            self.move_platform(platform)
            self.discard_unseen_platforms(platform)
        # check if the player died
        if self.player.pos[1] < -self.player.height:
            self.game_over()

    def on_touch_down(self, touch):
        # clicking right side of the screen
        if touch.pos[0] > Window.width / 2:
            self.player.velocity[0] = 7.5
        else:
            self.player.velocity[0] = -7.5

    def create_platforms(self, numOfPlatforms, separation):
        # percentage chance of spawning a moving platform
        moving_plat_chance = 0.25
        for i in range(numOfPlatforms):
            if random() <= moving_plat_chance:
                # using the position of the last platform added to create the new platform
                p = MovingPlatform(pos=(random()*800, self.platform_group[-1].pos[1] + separation), size=(150, 10))
            else:
                # static platforms
                p = Platform(pos=(random()*800, self.platform_group[-1].pos[1] + separation), size=(150, 10))
            Clock.schedule_interval(p.update, 1 / 60.)
            self.add_widget(p)
            self.platform_group.append(p)

    def platform_player_collision(self, platform):
        # check player collision with platforms
        if self.player.collide_widget(platform):
            if self.player.velocity[1] < -2.5 and self.player.pos[1] > platform.pos[1] - platform.height / 2:
                self.player.velocity[1] = self.bounce_value

    def move_platform(self, platform):
        # update height of platforms
        if self.player.pos[1] > 280:
            platform.velocity[1] = -self.background_movement_speed
            self.score += 1
        else:
            platform.velocity[1] = 0

    def discard_unseen_platforms(self, platform):
        # delete platform objects that fall below the screen
        platform_offscreen_distance = 50
        if platform.pos[1] < -self.player.height:
            self.remove_widget(platform)
            self.platform_group.pop(0)
            self.create_platforms(1, platform_offscreen_distance)

    def start_game(self):
        self.player.give_player_movement()
        self.player.paused = False
        self.bounce_value = 15
        self.game_has_started = True
        for p in self.platform_group:
            p.paused = False

    def pause_game(self):
        self.bounce_value = 0
        self.player.paused = True
        self.game_has_started = False
        for p in self.platform_group:
            p.paused = True

    def game_over(self):
        self.parent.parent.manager.current = 'game_over'

    def _keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not self.game_has_started:
            return
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


class GameScreen(Screen):
    def on_enter(self):
        gameView = self.ids['game']
        gameView.start_game()


class MenuScreen(Screen):
    pass


class GameOverScreen(Screen):
    pass


class GeoJumpApp(App):
    def build(self):
        screen_manager = ScreenManager(transition=FadeTransition())
        screen_manager.add_widget(MenuScreen(name='menu'))
        screen_manager.add_widget(GameScreen(name='game'))
        screen_manager.add_widget(GameOverScreen(name='game_over'))
        return screen_manager


if __name__ == '__main__':
    GeoJumpApp().run()