from pico2d import *
import game_world
import game_framework
from sdl2 import SDL_KEYDOWN,SDLK_f

class Friend: # 구출 대상
    def __init__(self,x,y,image_name):
        self.x, self.y=x,y
        self.image=load_image(image_name)
        pass
    def update(self):
        pass
    def draw(self):
        scale=3
        self.image.composite_draw(0,'h',self.x, self.y,self.image.w * scale,self.image.h * scale)
        pass
    def handle_event(self,event):
        if event.type==SDL_KEYDOWN  and event.key == SDLK_f:
            player=game_world.get_player()
            distance=((self.x-player.x)**2+(self.y-player.y)**2)**0.5

            if distance < 100:
                game_world.remove_object(self)

        pass
