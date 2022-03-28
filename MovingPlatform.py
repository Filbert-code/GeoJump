from random import random

from Platform import Platform


# Subclass of Platform. These platforms can move around. Impressive isn't it?
class MovingPlatform(Platform):
    def __init__(self, **kwargs):
        super(MovingPlatform, self).__init__(**kwargs)
        # at least the distance will be 300, can be up to 700 pixels
        self.moving_distance = random() * 400 + 300
        # at least speed of 1, can be up to 4
        self.velocity[0] = random() * 3 + 1
        self.starting_pos_x = self.pos[0]

    def update(self, *args):
        # platform is traveling right
        if self.velocity[0] > 0:
            # change directions when reached the end of the distance to travel
            if self.x + self.width/2 > self.starting_pos_x + self.moving_distance:
                self.velocity[0] *= -1
        # moving to the left
        else:
            # change directions
            if self.x + self.width/2 < self.starting_pos_x:
                self.velocity[0] *= -1
        super().update()
