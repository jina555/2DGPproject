from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass1.png')
        self.y=120
        self.h=80

    def draw(self):
        self.image.draw(get_canvas_width()//2,self.y,get_canvas_width(),self.h)
    def update(self):
        pass
