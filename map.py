from pico2d import *

GROUND_Y=80

class Map:
    def __init__(self):
        pass

    def draw(self):
        w=get_canvas_width()
        draw_rectangle(0,GROUND_Y-15,w,GROUND_Y-15)

    def update(self):
        pass

