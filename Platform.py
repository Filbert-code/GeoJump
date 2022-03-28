from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.uix.widget import Widget


class Platform(Widget):
    velocity = ListProperty([0, 0])
    def __init__(self, **kwargs):
        super(Platform, self).__init__(**kwargs)
        self.pos = kwargs['pos']
        self.size = kwargs['size']
        # self.isBooster = False
        with self.canvas:
            Color(1., 1., 1.)
            Rectangle(pos=self.pos, size=self.size)
        self.paused = False

    def update(self, *args):
        if self.paused:
            return

        self.x += self.velocity[0]
        self.y += self.velocity[1]

        self.draw()

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(1., 1., 1.)
            Rectangle(pos=self.pos, size=self.size)