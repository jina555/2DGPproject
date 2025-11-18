from pico2d import *
from monster import Monster
import game_framework

class Boss(Monster):
    def __init__(self):
        super().__init__()
        self.x=800
        self.y=250
        self.images=[]
        self.width=200
        self.height=200
        self.animation_speed=8
        pass

    def update(self):
        super().update()
        self.frame=(self.frame+self.animation_speed*game_framework.frame_time)

    def draw(self):
        if not self.images:
            return

        img_index = int(self.frame) % len(self.images)

        if self.face_dir == 1:
            self.images[img_index].draw(self.x, self.y, self.width, self.height)
        else:
            self.images[img_index].composite_draw(0, 'h', self.x, self.y, self.width, self.height)

class Boss1(Boss):
    def __init__(self):
        super().__init__()
        self.images=[
            load_image('boss1/bigslim_01.png'),
            load_image('boss1/bigslim_02.png'),
            load_image('boss1/bigslim_03.png'),
        ]
