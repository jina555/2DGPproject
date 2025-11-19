from pico2d import *

class Portal:
    def __init__(self,x,y):
        self.image=load_image('res2/portal.png')
        self.x,self.y=x,y
        self.w=self.image.w
        self.h=self.image.h

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x,self.y,114,117)

    def get_bb(self):
        return self.x-65,self.y-65,self.x+65,self.y+65
