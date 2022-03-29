from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.uix.widget import Widget


class Platform(Widget):
    velocity = ListProperty([0, 0])

    def __init__(self, player, isBooster, **kwargs):
        super(Platform, self).__init__(**kwargs)
        self.pos = kwargs['pos']
        self.size = kwargs['size']
        self.player = player
        self.isBooster = isBooster
        self.paused = False
        self.background_movement_speed = 5

    def update(self, *args):
        if self.paused:
            return

        self.platform_player_collision()
        if self.player.boost_active:
            self.boost_platform()
        else:
            self.move_platform()

        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.draw()

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            if not self.isBooster:
                Color(1., 1., 1.)
            else:
                Color(0., 1., 0.)
            Rectangle(pos=self.pos, size=self.size)

    def platform_player_collision(self):
        # check player collision with platforms
        if self.player.collide_widget(self):
            if self.player.velocity[1] < -2.5 and self.player.pos[1] > self.pos[1] - self.height / 2:
                if self.isBooster:
                    self.player.boost_active = True
                    Clock.schedule_once(self.reset_player_booster, 1)
                    self.player.bounce_value = 40
                    self.player.gravity /= 2.0
                self.player.velocity[1] = self.player.bounce_value

    def reset_player_booster(self, dt):
        self.player.boost_active = False
        self.player.boost_slowdown = False
        self.player.bounce_value = 20
        self.player.gravity *= 2.0

    def boost_platform(self):
        self.velocity[1] = self.player.platform_boost_velocity
        if self.velocity[1] < -20:
            self.player.boost_slowdown = True

    def move_platform(self):
        # update height of platforms
        if self.player.pos[1] > 200 and not self.player.boost_active:
            self.velocity[1] -= 2
            if self.velocity[1] < self.background_movement_speed:
                self.velocity[1] = -self.background_movement_speed
        else:
            self.velocity[1] = 0

