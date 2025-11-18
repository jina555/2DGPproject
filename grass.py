from pico2d import *
from character import GROUND_Y
import play_mode

class Grass:
    def __init__(self,name='res/grass.png'):
        self.image = load_image(name)
        self.h=self.image.h
        self.y=GROUND_Y
        self.w=self.image.w

    def draw(self):
        canvas_width=get_canvas_width()

        self.image.draw(canvas_width//2,self.y,canvas_width,self.h)
    def update(self):
        pass
