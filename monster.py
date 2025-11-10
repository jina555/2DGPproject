from pico2d import *
import game_framework
import game_world
from state_machine import StateMachine, State
import random

WALK_FRAMES_PER_ACTION=5
WALK_TIME_PER_ACTION=1.0
WALK_ACTION_PER_TIME=1.0/WALK_FRAMES_PER_ACTION

W,H=32,32
MOVE_SPEED=150
class Walk(State):
    def __init__(self,p):
        self.p=p
        pass
    def enter(self,e):
        self.p.vx= MOVE_SPEED * self.p.face_dir
        pass
    def exit(self,e):
        pass
    def do(self):
        self.p.x +=self.p.vx*game_framework.frame_time
        self.p.frame=(self.p.frame+WALK_FRAMES_PER_ACTION * WALK_ACTION_PER_TIME *game_framework.frame_time) % WALK_FRAMES_PER_ACTION

        if self.p.x < 50:
            self.p.vx=MOVE_SPEED
            self.p.face_dir=1
        elif self.p.x > 1280-50:
            self.p.vx=-MOVE_SPEED
            self.p.face_dir=-1
        pass
    def draw(self):
        if self.p.face_dir==1:
            self.p.img_walk.clip_composite_draw(int(self.p.frame)*W,0,W,H,0,'h',self.p.x,self.p.y,W*3,H*3)
        else:
            self.p.img_walk.clip_draw(int(self.p.frame)*W,0,W,H,self.p.x,self.p.y,W*3,H*3)

        pass
    pass
class Attack(State):
    def __init__(self,p):
        pass
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass
    pass
class Hurt(State):
    def __init__(self,p):
        pass
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass
    pass
class Die(State):
    def __init__(self,p):
        pass
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass
    pass

class Monster:
    def __init__(self):
        self.x=random.randint(300,1000)
        self.face_dir=random.choice([-1,1])
        self.vx=MOVE_SPEED * self.face_dir
        monster_half_h = (H * 3) // 2
        self.y = 161 + monster_half_h
        self.frame=0.0

        self.img_walk=load_image('res/monster1_walk.png')
        self.img_attack=load_image('res/stage1monster_attack.png')
        self.img_hurt=load_image('res/stage1monster_hurt.png')

        self.WALK=Walk(self)
        self.ATTACK=Attack(self)
        self.HURT=Hurt(self)
        self.DIE=Die(self)

        self.state_machine=StateMachine(start_state=self.WALK,transitions={})

        pass

    def update(self):
        self.state_machine.update()
        pass
    def draw(self):
        self.state_machine.draw()
        pass
    def get_bb(self):
        pass
    def handle_collision(self,group,other):
        pass
    def remove_self(self):
        pass
