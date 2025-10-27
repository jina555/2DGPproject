from pico2d import *
from sdl2 import SDL_KEYDOWN,SDL_KEYUP,SDLK_a,SDLK_d,SDLK_LSHIFT,SDLK_SPACE,SDLK_RSHIFT,SDL_BUTTON_LEFT,SDL_MOUSEBUTTONDOWN
from state_machine import StateMachine,State

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
MOVE_SPEED_RUN=300
MOVE_SPEED_WALK=150
JUMP_SPEED=900
W,H=32,64 #캐릭터 크기
GROUND_Y=80
ATTACK_ACTIVE=0.15 #히트박스 유지 시간
ATTACK_W=60 #공격박스 가로
ATTACK_H=40 #공격박스 세로


class Idle(State):
    def __init__(self,p):
        self.p=p
    def enter(self,e):
        self.p.vx=0
        self._last=get_time()
        self._acc=0
        self.p.frame=0
    def exit(self,e):
        pass

    def do(self):
        if self.p.a_down and not self.p.d_down:
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir=1

        now=get_time()
        dt=now-self._last
        self._last=now

        self._acc+=dt
        if self._acc>=0.25:
            self._acc=0
            self.p.frame=(self.p.frame+1)%4
    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2

        if self.p.face_dir==1:
            self.p.img_idle.clip_draw(self.p.frame*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_idle.clip_composite_draw(self.p.frame*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)
    pass


class Walk(State):
    def __init__(self,p):
        self.p=p
        self._last=0
        self._acc=0

    def enter(self,e):
        if self.p.a_down and not self.p.d_down:
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir=1

        self._last=get_time()
        self._acc=0

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
        if self.p.shift_down:
            self.p.state_machine.set_state(self.p.RUN,e=None)
            return

        now=get_time()
        dt=now-self._last
        self._last=now
        self._acc+=dt
        if self._acc>=0.12:
            self._acc=0
            self.p.frame=(self.p.frame+1)%4

    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2
        if self.p.face_dir==1:
            self.p.img_move.clip_draw(self.p.frame*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_move.clip_composite_draw(self.p.frame*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)


    pass


class Run:
    def __init__(self,p):
        self.p=p
    def enter(self,e):
        if self.p.a_down and not self.p.d_down:
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir=1
    def do(self):
        if self.p.shift_down:
            speed=MOVE_SPEED_RUN
        else:
            speed=MOVE_SPEED_WALK
        if self.p.a_down and not self.p.d_down:
            self.p.vx=-speed
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.vx=speed
            self.p.face_dir=1
        else:
            self.p.vx=0
            self.p.state_machine.set_state(self.p.IDLE,e=None)

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

        self.img_idle=load_image('idle.png')
        self.img_move=load_image('character_MOVE.png')

        self.a_down=False
        self.d_down=False
        self.shift_down=False
        self.pickup=False

        self.attack_time=0
        self.attack_box=(0,0,0,0)

        self.IDLE=Idle(self)
        self.WALK=Walk(self)
        self.RUN=Run(self)
        # self.Jump=Jump(self)
        # self.ATTACK=Attack(self)
        
        self.state_machine=StateMachine(
            start_state=self.IDLE,
            transitions={
                self.IDLE:{
                    a_down: self.WALK,
                    d_down: self.WALK,
                    shift_down: self.RUN,
                    # space_down: self.Jump,
                    # rmb_down: self.ATTACK,

                },
                self.WALK:{
                    shift_down: self.RUN,
                    # space_down: self.Jump,
                    # rmb_down: self.ATTACK,
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
        dt=0.01
        self.state_machine.update()
        self.x += self.vx*dt
        w=get_canvas_width()
        half=16
        if self.x<half:
            self.x=half
        if self.x>w-half:
            self.x=w-half

    def draw(self):
        self.state_machine.draw()


