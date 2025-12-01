from pico2d import *
import game_world
import game_framework

class Fireball:
    image=None
    def __init__(self,x,y,face_dir):
        if Fireball.image==None:
            Fireball.image=load_image("res2/fireball.png")
        self.x,self.y=x,y
        self.dir=face_dir
        self.velocity=800 * face_dir
        self.width,self.height=50,50
        pass
    def update(self):
        self.x += self.velocity * game_framework.frame_time

        if self.x<0 or self.x > 1600:
            game_world.remove_object(self)

        pass
    def draw(self):
        self.image.draw(self.x,self.y,self.width,self.height)
        draw_rectangle(*self.get_bb(),255,0,0)
        pass
    def get_bb(self):
        return self.x-20,self.y-20,self.x+20,self.y+20
        pass
    def handle_collision(self,group,other):
        if group=='monster_attack:player':
            game_world.remove_object(self)
        pass