from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.uix.widget import Widget


class Player(Widget):
    velocity = ListProperty([0, -7.5])

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.pos = kwargs['pos']
        self.size = kwargs['size']
        self.gravity = 0.5
        self.isMovingLeft = False
        self.isMovingRight = False
        Clock.schedule_interval(self.update, 1/60.)

    def update(self, *args):
        # print('player velocity: {}, {}'.format(self.velocity[0], self.velocity[1]))
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        # player has a constant decreasing vertical velocity (negative acceleration)
        self.velocity[1] -= self.gravity
        self.movePlayer()
        # player has a constant horizontal deceleration, will come to a stop if
        # no inputs are made
        if self.velocity[0] > 0:
            self.velocity[0] -= 0.5
        if self.velocity[0] < 0:
            self.velocity[0] += 0.5
        # limit the player's vertical speed to avoid clipping through platforms
        if self.velocity[1] < -12:
            self.velocity[1] = -12
        # limit the player's horizontal speed
        h_speed_limit = 12
        if self.velocity[0] > h_speed_limit:
            self.velocity[0] = h_speed_limit
        if self.velocity[0] < -h_speed_limit:
            self.velocity[0] = -h_speed_limit
        # teleport to the other side if the player exits the left or right screen
        if self.x < -self.width:
            self.x = Window.width
        elif self.x > Window.width:
            self.x = -self.width
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0, 0, 1.)
            Rectangle(pos=self.pos, size=self.size)

    def movePlayer(self):
        if self.isMovingLeft:
            self.velocity[0] -= 3
        if self.isMovingRight:
            self.velocity[0] += 3