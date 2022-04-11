from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Scale
from kivy.properties import ListProperty
from kivy.uix.widget import Widget


class Player(Widget):
    velocity = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.pos = kwargs['pos']
        self.size = kwargs['size']
        self.gravity = 0
        self.isMovingLeft = False
        self.isMovingRight = False
        Clock.schedule_interval(self.update, 1/60.)
        self.paused = False
        self.bounce_value = 16
        self.boost_active = False
        self.boost_slowdown = False
        self.platform_boost_velocity = 0
        self.platform_velocity = 0

    def update(self, *args):
        if self.paused:
            return
        # update player velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        if self.boost_active:
            self.update_boost_velocity()
            # print(self.platform_boost_velocity)

        if self.pos[1] > Window.height/2:
            self.pos[1] = Window.height/2

        # player has a constant decreasing vertical velocity (negative acceleration)
        self.velocity[1] -= self.gravity
        self.horizontal_acceleration(1.5)
        self.horizontal_deceleration(1)
        # self.vertical_speed_limit(40, 12)
        self.horizontal_speed_limit(10)
        self.horizontal_out_of_bounds()
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Color(0, 0, 1.)
            Rectangle(pos=self.pos, size=self.size, source='boxplayer2.png', background_normal=Color(1, 1, 1))

    def horizontal_acceleration(self, acc):
        if self.isMovingLeft:
            self.velocity[0] -= acc
        if self.isMovingRight:
            self.velocity[0] += acc

    def horizontal_deceleration(self, acc):
        # player has a constant horizontal deceleration, will come to a stop if
        # no inputs are made
        if abs(self.velocity[0]) < acc:
            self.velocity[0] = 0
            return
        if self.velocity[0] > 0:
            self.velocity[0] -= acc
        else:
            self.velocity[0] += acc

    def vertical_speed_limit(self, speed_limit_down, speed_limit_up):
        # limit the player's vertical speed to avoid clipping through platforms
        if self.velocity[1] < -speed_limit_down:
            self.velocity[1] = -speed_limit_down
        elif self.velocity[1] > speed_limit_up:
            self.velocity[1] = speed_limit_up

    def horizontal_speed_limit(self, speed_limit):
        # limit the player's horizontal speed
        if self.velocity[0] > speed_limit:
            self.velocity[0] = speed_limit
        if self.velocity[0] < -speed_limit:
            self.velocity[0] = -speed_limit

    def horizontal_out_of_bounds(self):
        # teleport to the other side if the player exits the left or right screen
        if self.x < -self.width:
            self.x = Window.width
        elif self.x > Window.width:
            self.x = -self.width

    def give_player_movement(self):
        self.velocity[1] = -7.5
        self.gravity = 0.6

    def update_boost_velocity(self):
        if self.boost_slowdown:
            if self.platform_boost_velocity < -5:
                self.platform_boost_velocity += 1
            else:
                self.boost_active = False
                self.boost_slowdown = False
                self.bounce_value = 20
                self.gravity *= 2
        else:
            self.platform_boost_velocity -= 1