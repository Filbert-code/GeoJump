from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
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

    def update(self, *args):
        if self.paused:
            return
        # update player velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # player has a constant decreasing vertical velocity (negative acceleration)
        self.velocity[1] -= self.gravity
        self.horizontal_acceleration(1.5)
        self.horizontal_deceleration(1)
        self.vertical_speed_limit(40, 12)
        self.horizontal_speed_limit(10)
        self.horizontal_out_of_bounds()
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 1.)
            Rectangle(pos=self.pos, size=self.size)

    def horizontal_acceleration(self, acc):
        if self.isMovingLeft:
            self.velocity[0] -= acc
        if self.isMovingRight:
            self.velocity[0] += acc

    def horizontal_deceleration(self, acc):
        # player has a constant horizontal deceleration, will come to a stop if
        # no inputs are made
        if self.velocity[0] > 0:
            self.velocity[0] -= acc
        if self.velocity[0] < 0:
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
        self.gravity = 0.5

