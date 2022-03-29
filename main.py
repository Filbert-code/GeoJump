# make two circles that collide into each other and bounce around in the screen
from random import random
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, NoTransition, CardTransition
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, ReferenceListProperty
from MovingPlatform import MovingPlatform
from Platform import Platform
from Player import Player

# Make Sure This Is Always the last import
from kivy import Config
Config.set('graphics', 'multisamples', '0')
Window.top = 100
Window.left = 1000
Window.size = (600, 1200)


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
        self.player_boost_active = False
        self.player_boost_slowdown = False
        self.platform_boost_vel = 0

        # user keyboard input setup
        self.keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self.keyboard.bind(on_key_down=self._on_keyboard_down)
        self.keyboard.bind(on_key_up=self._on_keyboard_up)

        # platform setup
        p1 = Platform(isBooster=False, pos=(0, -20), size=(1500, 10))
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

        # TODO: REFACTOR THIS!!!
        if self.player_boost_active:
            self.update_player_boost_velocity()
        # collision detections
        for platform in self.platform_group:
            self.platform_player_collision(platform)
            if self.player_boost_active:
                self.boost_platform(platform)
            else:
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
        booster_plat_chance = 0.25
        for i in range(numOfPlatforms):
            isBooster = random() < booster_plat_chance
            if random() <= moving_plat_chance:
                # using the position of the last platform added to create the new platform
                p = MovingPlatform(isBooster=isBooster,
                                   pos=(random()*800, self.platform_group[-1].pos[1] + separation),
                                   size=(150, 10))
            else:
                # static platforms
                p = Platform(isBooster=isBooster,
                             pos=(random()*800, self.platform_group[-1].pos[1] + separation),
                             size=(150, 10))
            Clock.schedule_interval(p.update, 1 / 60.)
            self.add_widget(p)
            self.platform_group.append(p)

    def platform_player_collision(self, platform):
        # check player collision with platforms
        if self.player.collide_widget(platform):
            if self.player.velocity[1] < -2.5 and self.player.pos[1] > platform.pos[1] - platform.height / 2:
                if platform.isBooster:
                    self.player_boost_active = True
                    Clock.schedule_once(self.reset_player_booster, 1)
                    self.bounce_value = 40
                    self.player.gravity /= 2.0
                self.player.velocity[1] = self.bounce_value

    def reset_player_booster(self, dt):
        self.player_boost_active = False
        self.player_boost_slowdown = False
        self.bounce_value = 15
        self.player.gravity *= 2.0

    def update_player_boost_velocity(self):
        if self.player_boost_slowdown:
            self.platform_boost_vel += 0.6
        else:
            self.platform_boost_vel -= 0.6

    def boost_platform(self, platform):
        platform.velocity[1] = self.platform_boost_vel
        if platform.velocity[1] < -20:
            self.player_boost_slowdown = True

    def move_platform(self, platform):
        # update height of platforms
        if self.player.pos[1] > 280 and not self.player_boost_active:
            platform.velocity[1] -= 2
            if platform.velocity[1] < self.background_movement_speed:
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
        self.parent.parent.manager.transition = NoTransition()
        self.parent.parent.manager.current = 'game_over'
        self.reset_game_widgets()

    def reset_game_widgets(self):
        self.score = 0
        # delete all current children widgets
        for child in self.children:
            self.remove_widget(child)
        self.canvas.clear()
        # unschedule all updates
        for platform in self.platform_group:
            Clock.unschedule(platform.update)
        self.platform_group = []
        Clock.unschedule(self.player.update)

        # player setup
        self.player = Player(pos=(0, 200), size=(60, 60))
        self.add_widget(self.player)
        self.bounce_value = 0
        self.player.velocity[1] = 0
        self.player.gravity = 0

        # platform setup
        p1 = Platform(isBooster=False, pos=(0, -20), size=(1500, 10))
        self.add_widget(p1)
        self.platform_group = [p1]
        self.create_platforms(20, 50)
        self.background_movement_speed = 5

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
        screen_manager = ScreenManager(transition=CardTransition())
        screen_manager.add_widget(MenuScreen(name='menu'))
        screen_manager.add_widget(GameScreen(name='game'))
        screen_manager.add_widget(GameOverScreen(name='game_over'))
        return screen_manager


if __name__ == '__main__':
    GeoJumpApp().run()