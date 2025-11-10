from pico2d import *
from sdl2 import SDL_KEYDOWN,SDL_KEYUP,SDLK_a,SDLK_d,SDLK_LSHIFT,SDLK_SPACE,SDLK_RSHIFT,SDL_BUTTON_LEFT,SDL_MOUSEBUTTONDOWN
from state_machine import StateMachine,State
import game_framework


def a_down(e):
    return e and e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_a
def d_down(e):
    return e and e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_d
def shift_down(e):
    return e and e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and (e[1].key==SDLK_LSHIFT or e[1].key==SDLK_RSHIFT)
def space_down(e):
    return e and e[0]=='INPUT' and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_SPACE
def rmb_down(e):
    return e and e[0]=='INPUT' and e[1].type==SDL_MOUSEBUTTONDOWN and e[1].button==SDL_BUTTON_LEFT

IDLE_FRAMES_PER_ACTION=4
IDLE_TIME_PER_ACTION=1.0
IDLE_ACTION_PER_TIME=1.0/IDLE_TIME_PER_ACTION

WALK_FRAMES_PER_ACTION=4
WALK_TIME_PER_ACTION = 0.48
WALK_ACTION_PER_TIME=1.0/WALK_TIME_PER_ACTION

RUN_FRAMES_PER_ACTION =4
RUN_TIME_PER_ACTION = 0.4
RUN_ACTION_PER_TIME=1.0/RUN_TIME_PER_ACTION

MOVE_SPEED_RUN=80
MOVE_SPEED_WALK=30
JUMP_SPEED=900
W,H=32,64 #캐릭터 크기
GROUND_Y=80
ATTACK_ACTIVE=0.15 #히트박스 유지 시간
ATTACK_W=60 #공격박스 가로
ATTACK_H=40 #공격박스 세로
GRAVITY=2000

class Idle(State):
    def __init__(self,p):
        self.p=p
    def enter(self,e):
        self.p.vx=0
        self.p.frame=0
    def exit(self,e):
        pass

    def do(self):
        if self.p.a_down and not self.p.d_down:
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir=1
        self.p.frame=(self.p.frame + IDLE_FRAMES_PER_ACTION * IDLE_ACTION_PER_TIME * game_framework.frame_time)%IDLE_FRAMES_PER_ACTION
    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2


        if self.p.face_dir==1:
            self.p.img_idle.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_idle.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)
    pass


class Walk(State):
    def __init__(self,p):
        self.p=p

    def enter(self,e):
        if self.p.a_down and not self.p.d_down:
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir=1

    def exit(self,e):
        pass

    def do(self):
        if self.p.a_down and not self.p.d_down:
            self.p.vx=-MOVE_SPEED_WALK; self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.vx=MOVE_SPEED_WALK; self.p.face_dir=1
        else:
            self.p.vx=0
            self.p.state_machine.set_state(self.p.IDLE,e=None)
            return
        self.p.frame=(self.p.frame + WALK_FRAMES_PER_ACTION * WALK_ACTION_PER_TIME * game_framework.frame_time)%WALK_FRAMES_PER_ACTION



    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2

        if self.p.face_dir==1:
            self.p.img_move.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_move.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)


    pass


class Run:
    def __init__(self,p):
        self.p=p
    def enter(self,e):
        pass

    def exit(self,e):
        pass
    def do(self):
        if not self.p.shift_down:
            self.p.vx=0
            self.p.state_machine.set_state(self.p.IDLE,e=None)
            return
        if self.p.a_down and not self.p.d_down:
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir=1

        self.p.vx=MOVE_SPEED_RUN * self.p.face_dir
        self.p.frame=(self.p.frame + RUN_FRAMES_PER_ACTION * WALK_ACTION_PER_TIME * game_framework.frame_time)%RUN_FRAMES_PER_ACTION
    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2

        if self.p.face_dir==1:
            self.p.img_run.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_run.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)




    pass

class Jump:
    def __init__(self,p):
        self.p=p
        self._last=0
        self._acc=0
        self.jump_frames=6

        pass
    def enter(self,e):
        if self.p.on_ground:
            self.p.vy=JUMP_SPEED
            self.p.on_ground=False

        self.p.frame=0
        self._last=get_time()
        self._acc=0
        pass
    def exit(self,e):
        pass
    def do(self):
        if self.p.on_ground:
            if self.p.a_down != self.p.d_down:
                self.p.state_machine.set_state(self.p.WALK,e=None)
            else:
                self.p.state_machine.set_state(self.p.IDLE,e=None)
            return

        if self.p.a_down and not self.p.d_down:
            self.p.vx=-MOVE_SPEED_WALK
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.vx=MOVE_SPEED_WALK
            self.p.face_dir=1

        pass
    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2

        if self.p.face_dir==1:
            self.p.img_jump.clip_draw(self.p.frame*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_jump.clip_composite_draw(self.p.frame*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)
        pass


class Attack:
    def __init__(self,p):
        self.p=p
        self._last=0
        self._acc=0
        self.frame_count=4
        self.frame_time=0.1

        pass

    def enter(self,e):
        self.p.frame=0
        self._last=get_time()
        self._acc=0
        self.p.attack_time=ATTACK_ACTIVE
        self.update_attack_box()

        pass
    def exit(self,e):
        self.p.attack_home=(0,0,0,0)
        pass
    def do(self):
        now=get_time()
        dt=now-self._last
        self._last=now

        self._acc += dt
        if self._acc >= self.frame_time:
            self._acc=0
            self.p.frame=(self.p.frame+1)%self.frame_count
        self.p.attack_time-=dt
        if self.p.attack_time>0:
            self.update_attack_box()
        else:
            if self.p.a_down != self.p.a_down:
                self.p.state_machine.set_state(self.p.WALK,e=None)
            else:
                self.p.state_machine.set_state(self.p.IDLE,e=None)
            return

        pass
    def update_attack_box(self):
        pass
    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2

        if self.p.face_dir==1:
            self.p.img_attack.clip_draw(self.p.frame*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_attack.clip_composite_draw(self.p.frame*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)
        pass



class Character:
    def __init__(self):
        self.x=400
        self.y=GROUND_Y+H//2
        self.vx=0
        self.vy=0#점프나 낙하시
        self.on_ground=True
        self.face_dir=1 #1:오른쪽, -1:왼쪽
        self.last_imput_time=get_time()

        self.img_idle=load_image('res/idle.png')
        self.img_move=load_image('res/character_MOVE.png')
        self.img_run=load_image('res/character_MOVE.png')
        self.img_jump=load_image('res/character_JUMP.png')
        self.img_attack=load_image('res/character_ATTACK.png')

        self.a_down=False
        self.d_down=False
        self.shift_down=False
        self.pickup=False

        self.attack_time=0
        self.attack_box=(0,0,0,0)

        self.IDLE=Idle(self)
        self.WALK=Walk(self)
        self.RUN=Run(self)
        self.JUMP=Jump(self)
        self.ATTACK=Attack(self)
        
        self.state_machine=StateMachine(
            start_state=self.IDLE,
            transitions={
                self.IDLE:{
                    a_down: self.WALK,
                    d_down: self.WALK,
                    shift_down: self.RUN,
                    space_down: self.JUMP,
                    rmb_down: self.ATTACK,

                },
                self.WALK:{
                    shift_down: self.RUN,
                    space_down: self.JUMP,
                    rmb_down: self.ATTACK,
                },
                self.RUN:{
                    space_down: self.JUMP,
                    rmb_down:self.ATTACK
                },
                self.JUMP:{
                    rmb_down:self.ATTACK
                }


            }
            
        )

    def handle_event(self,event):
        if event.type==SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.a_down=True
            elif event.key==SDLK_d:
                self.d_down=True
            elif event.key == SDLK_LSHIFT:
                self.shift_down=True
            elif event.key==SDLK_SPACE:
                self.jump()
            elif event.key ==SDLK_f:
                self.pickup=True


        elif event.type==SDL_KEYUP:
            if event.key==SDLK_a:
                self.a_down=False
            elif event.key==SDLK_d:
                self.d_down=False
            elif event.key==SDLK_LSHIFT:
                self.shift_down=False

        elif event.type==SDL_MOUSEBUTTONDOWN and event.button==SDL_BUTTON_LEFT:
            self.start_attack()

        if event.type in (SDL_KEYDOWN, SDL_KEYUP,SDL_MOUSEBUTTONDOWN,SDL_MOUSEBUTTONUP):
            self.last_input_time=get_time()

        self.state_machine.handle_state_event(('INPUT',event))


    def jump(self):
        if self.on_ground:
            self.vy=JUMP_SPEED
            self.on_ground=False

    def start_attack(self):
        self.attack_time=ATTACK_ACTIVE
        print("attack!")

    def update(self):
        dt=1/60
        self.state_machine.update()
        self.x += self.vx*dt

        self.vy-= GRAVITY*dt
        self.y += self.vy*dt

        if self.y <= GROUND_Y + H // 2:
            self.y=GROUND_Y+H//2
            self.vy=0
            self.on_ground=True


        w=get_canvas_width()
        half=16
        if self.x<half:
            self.x=half
        if self.x>w -half:
            self.x=w-half

    def draw(self):
        self.state_machine.draw()


