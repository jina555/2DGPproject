from pico2d import *
import game_framework
import game_world
from state_machine import StateMachine, State
W,H=20,20
class Walk(State):
    pass
class Attack(State):
    pass
class Hurt(State):
    pass
class Die(State):
    pass

class Monster:
    def __init__(self):
        self.x=800
        self.y=80+H//2 *3
        self.vx=0
        self.face_dir=-1
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
