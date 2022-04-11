# make two circles that collide into each other and bounce around in the screen
from random import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition, CardTransition
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, ReferenceListProperty
from MovingPlatform import MovingPlatform
from Platform import Platform
from Player import Player

# Make Sure This Is Always the last import
from kivy import Config
Config.set('graphics', 'multisamples', '0')
Window.top = 120
Window.left = 1000
Window.size = (600, 1080)
Builder.load_file("GeoJump.kv")


class GameView(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super(GameView, self).__init__(**kwargs)
        # used for pausing the game
        self.game_has_started = False

        # user keyboard input setup
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self._on_keyboard_down)
        self.keyboard.bind(on_key_up=self._on_keyboard_up)

        # initialize player and platforms
        self.player = None
        self.platform_group = None
        self.clean_and_build_game_objects()

        # schedule updates
        Clock.schedule_interval(self.update, 1/60.)

    def clean_and_build_game_objects(self):
        self.score = 0
        # delete all current children widgets
        for child in self.children:
            self.remove_widget(child)
        self.canvas.clear()
        # unschedule all updates
        if self.platform_group:
            for platform in self.platform_group:
                Clock.unschedule(platform.update)
        self.platform_group = []
        if self.player:
            Clock.unschedule(self.player.update)

        # player setup
        self.player = Player(pos=(0, 200), size=(100, 100))
        self.add_widget(self.player)
        self.player.velocity[1] = 0
        self.player.gravity = 0

        # platform setup
        p1 = Platform(self.player, isBooster=False, pos=(0, 0), size=(1500, 25))
        self.add_widget(p1)
        p1.update()
        p = Platform(self.player, isBooster=False, pos=(100, 100), size=(175, 15))
        self.add_widget(p)
        self.platform_group = [p1, p]
        for i in range(10):
            p = Platform(self.player, isBooster=False, pos=(0, (75 * (i + 1)) + 200), size=(175, 15))
            self.add_widget(p)
            self.platform_group.append(p)
        # self.create_platforms(20, 70)

    def update(self, *args):
        # don't update if game hasn't started
        if not self.game_has_started:
            return
        # update the score
        if self.player.pos[1] > 200:
            self.score += 1
        # clean up off-screen platforms
        for platform in self.platform_group:
            self.discard_unseen_platforms(platform)
            platform.update()
        # check if the player died
        if self.player.pos[1] < -self.player.height:
            self.game_over()

    def on_touch_down(self, touch):
        touch.grab(self)
        # clicking right side of the screen
        if touch.pos[0] > Window.width / 2:
            self.player.isMovingRight = True
        else:
            self.player.isMovingLeft = True

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # I receive my grabbed touch, I must ungrab it!
            touch.ungrab(self)
            if touch.pos[0] > Window.width / 2:
                self.player.isMovingRight = False
            else:
                self.player.isMovingLeft = False

    def create_platforms(self, numOfPlatforms, separation=150):
        # percentage chance of spawning a moving platform
        separation += random()*100
        moving_plat_chance = 0.25
        booster_plat_chance = 0.1
        for i in range(numOfPlatforms):
            isBooster = random() < booster_plat_chance
            if random() <= moving_plat_chance:
                # using the position of the last platform added to create the new platform
                p = MovingPlatform(player=self.player,
                                   isBooster=isBooster,
                                   pos=(random()*(Window.width - 175), self.platform_group[-1].pos[1] + separation),
                                   size=(175, 25))
            else:
                # static platforms
                p = Platform(player=self.player,
                             isBooster=isBooster,
                             pos=(random()*(Window.width - 175), self.platform_group[-1].pos[1] + separation),
                             size=(175, 25))
            p.update()
            self.add_widget(p)
            self.platform_group.append(p)

    def discard_unseen_platforms(self, platform):
        # delete platform objects that fall below the screen
        if platform.pos[1] < -15:
            self.remove_widget(platform)
            self.platform_group.pop(0)
            self.create_platforms(1)

    def start_game(self):
        self.player.give_player_movement()
        self.player.paused = False
        self.game_has_started = True
        for p in self.platform_group:
            p.paused = False

    def pause_game(self):
        self.player.bounce_value = 0
        self.player.paused = True
        self.game_has_started = False
        for p in self.platform_group:
            p.paused = True

    def game_over(self):
        self.parent.parent.manager.transition = NoTransition()
        self.parent.parent.manager.current = 'game_over'
        self.clean_and_build_game_objects()

    def _keyboard_closed(self):
        self.keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if not self.game_has_started:
            return
        if keycode[1] == 'a':
            self.player.isMovingLeft = True
        elif keycode[1] == 'd':
            self.player.isMovingRight = True
        return True

    def _on_keyboard_up(self, keyboard, keycode):
        if keycode[1] == 'a':
            self.player.isMovingLeft = False
        elif keycode[1] == 'd':
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
        screen_manager = ScreenManager(transition=CardTransition())
        screen_manager.add_widget(MenuScreen(name='menu'))
        screen_manager.add_widget(GameScreen(name='game'))
        screen_manager.add_widget(GameOverScreen(name='game_over'))
        return screen_manager


if __name__ == '__main__':
    GeoJumpApp().run()