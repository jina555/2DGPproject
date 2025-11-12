from pico2d import *


GROUND_Y=80

class Map:
    def __init__(self):
        self.image=load_image('res/map1.png')
        self.w=self.image.w
        self.h=self.image.h

    def draw(self):
        cw=get_canvas_width()
        ch=get_canvas_height()

        self.image.clip_draw(0,0,self.w,self.h,cw//2,ch//2,cw,ch)

    def update(self):
        pass

