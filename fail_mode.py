from pico2d import *
import game_framework
import game_world
import play_mode
import start_mode

class FailEffect:
    def __init__(self,x,y):
        self.x,self.y=x,y
        self.image=load_image('res2/result_fail.png')
        self.w,self.h=64,64
    def update(self):
        pass
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)

class GameOverMessage:
    def __init__(self):
        self.image=load_image('res2/game_over.png')
        self.w,self.h=500,200
        self.x,self.y=get_canvas_width()//2,get_canvas_height()//2
    def update(self):
        pass
    def draw(self):
        self.image.draw(self.x,self.y,self.w,self.h)


GAME_OVER_TIME=3.0
char_last_x,char_last_y=0,0
timer=0.0
fail_effect=None
game_over_message=None

def init():
    global timer,fail_effect,game_over_message
    timer=GAME_OVER_TIME
    fail_effect=FailEffect(char_last_x,char_last_y+100)
    game_world.add_object(fail_effect,1)
    game_over_message=GameOverMessage()
    game_world.add_object(game_over_message,2)
def finish():
    global fail_effect,game_over_message
    if fail_effect:
        game_world.remove_object(fail_effect)
    if game_over_message:
        game_world.remove_object(game_over_message)
def update():
    global timer
    timer -= game_framework.frame_time
    if timer <=0:
        game_framework.change_mode(start_mode)
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
def handle_events():
    pass
