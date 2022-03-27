from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget


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