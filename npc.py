from pico2d import *
import game_world
import game_framework
from sdl2 import SDL_KEYDOWN,SDLK_f,SDLK_r,SDLK_t

class Friend: # 구출 대상
    def __init__(self,x,y,image_name,reward_value):
        self.x, self.y=x,y
        self.image=load_image(image_name)
        self.reward_value=reward_value
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

            if distance < 200:
                if self.reward_value is None:
                    game_world.remove_object(self)
                    return
                if self.reward_value <= 100:
                    inv_icon=InvincibleIcon(790,45)
                    game_world.add_object(inv_icon,2)
                    pass
                else:
                    hp_icon = HpIcon(710, 45, self.reward_value)
                    game_world.add_object(hp_icon, 2)
                game_world.remove_object(self)

        pass
class InvincibleIcon:
    def __init__(self,x,y):
        self.image=load_image('res2/invincible.png')
        self.x,self.y=x,y
        self.width,self.height=50,50
        pass
    def update(self):
        pass
    def draw(self):
        scale=3
        self.image.draw(self.x,self.y,self.image.w *scale,self.image.h*scale)
        pass
    def handle_event(self,event):
        if event.type==SDL_KEYDOWN and event.key==SDLK_t:
            player=game_world.get_player()
            if player:
                player.invincible=True
                player.invincible_timer=5.0
                player.scale=2.0
            game_world.remove_object(self)
        pass

class HpIcon:
    def __init__(self,x,y,value):
        self.image=load_image('res2/hp_up.png')
        self.x,self.y=x,y
        self.value=value
        self.width,self.height=50,50
        pass
    def update(self):
        pass
    def draw(self):
        scale=3
        self.image.draw(self.x,self.y,self.image.w*scale,self.image.h*scale)
        pass
    def handle_event(self,event):
        if event.type == SDL_KEYDOWN and event.key == SDLK_r:
            self.use_item()
            return
        pass
    def use_item(self):
        player = game_world.get_player()
        if player:
            player.max_hp += self.value
            player.hp += self.value
            player.hp = player.max_hp
        game_world.remove_object(self)
        pass

