from pico2d import *
from sdl2 import SDL_KEYDOWN,SDL_KEYUP,SDLK_a,SDLK_d,SDLK_LSHIFT,SDLK_SPACE,SDLK_RSHIFT,SDL_BUTTON_LEFT,SDL_MOUSEBUTTONDOWN
from state_machine import StateMachine,State
import game_framework
import game_world


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

ATTACK_FRAMES_PER_ACTION=4
ATTACK_TIME_PER_ACTION=0.4
ATTACK_ACTION_PER_TIME=1.0/ATTACK_TIME_PER_ACTION

JUMP_FRAMES_PER_ACTION=6
JUMP_TIME_PER_ACTION=0.6
JUMP_ACTION_PER_TIME=1.0/JUMP_TIME_PER_ACTION

MOVE_SPEED_RUN=200
MOVE_SPEED_WALK=100
JUMP_SPEED=700
W,H=32,64 #캐릭터 크기
GROUND_Y=80
ATTACK_ACTIVE=0.15 #히트박스 유지 시간
ATTACK_W=60 #공격박스 가로
ATTACK_H=40 #공격박스 세로
GRAVITY=1800

DAMAGE_BARE_HANDS=20
class PlayerAttackBox:
    def __init__(self, char_x, char_y, face_dir,damage):
        self.life_time = ATTACK_ACTIVE
        self.face_dir = face_dir
        self.damage = damage

        scale = 3
        char_half_w = (W * scale) // 2
        if self.face_dir == 1:
            self.left = char_x + char_half_w
            self.right = self.left + ATTACK_W
        else:
            self.right = char_x - char_half_w
            self.left = self.right - ATTACK_W
        monster_center_y = 191
        self.bottom = monster_center_y - (ATTACK_H // 2)
        self.top = monster_center_y + (ATTACK_H // 2)
    def update(self):
        self.life_time -= game_framework.frame_time
        if self.life_time < 0:
            game_world.remove_object(self)
    def get_bb(self):
        return self.left, self.bottom, self.right, self.top
    def handle_collision(self, group, other):
        if group == 'player_attack:monster':
            pass
    def draw(self):
        pass

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
        if self.p.shift_down:
            self.p.state_machine.set_state(self.p.RUN, e=None)
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
            self.p.vx = 0
            self.p.state_machine.set_state(self.p.IDLE, e=None)
            return


        if self.p.a_down and not self.p.d_down:
            self.p.face_dir = -1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir = 1


        self.p.vx = MOVE_SPEED_RUN * self.p.face_dir
        self.p.frame = (self.p.frame + RUN_FRAMES_PER_ACTION * RUN_ACTION_PER_TIME * game_framework.frame_time) % RUN_FRAMES_PER_ACTION

        if self.p.space_down:
            self.p.state_machine.set_state(self.p.JUMP, e=None)
            return
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

    def enter(self,e):
        if self.p.on_ground:
            self.p.vy=JUMP_SPEED
            self.p.on_ground=False

        self.p.frame=0

    def exit(self,e):
        pass
    def do(self):
        self.p.frame = self.p.frame + JUMP_FRAMES_PER_ACTION * JUMP_ACTION_PER_TIME * game_framework.frame_time
        if self.p.frame >= JUMP_FRAMES_PER_ACTION:
            self.p.frame = JUMP_FRAMES_PER_ACTION - 1


        if self.p.on_ground:
            if self.p.shift_down:
                self.p.state_machine.set_state(self.p.RUN, e=None)
            elif self.p.a_down != self.p.d_down:
                self.p.state_machine.set_state(self.p.WALK, e=None)
            else:
                self.p.state_machine.set_state(self.p.IDLE, e=None)
            return
        pass
    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2

        if self.p.face_dir==1:
            self.p.img_jump.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_jump.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)
        pass


class Attack:
    def __init__(self,p):
        self.p=p
    def enter(self,e):
        self.p.frame=0
        self.p.attack_time=ATTACK_ACTIVE
        self.update_attack_box()

    def exit(self,e):
        self.p.attack_home=(0,0,0,0)

    def do(self):
        self.p.frame=(self.p.frame + ATTACK_FRAMES_PER_ACTION * ATTACK_ACTION_PER_TIME * game_framework.frame_time)%ATTACK_FRAMES_PER_ACTION
        self.p.attack_time -= game_framework.frame_time
        if self.p.attack_time<0:
            if self.p.a_down != self.p.d_down:
                self.p.state_machine.set_state(self.p.WALK,e=None)
            else:
                self.p.state_machine.set_state(self.p.IDLE,e=None)
            return
        else:
            self.update_attack_box()
        pass
    def update_attack_box(self):
        pass
    def draw(self):
        scale=3
        offset_y=145*(scale-1)/2

        if self.p.face_dir==1:
            self.p.img_attack.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_attack.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)
        pass

class Die:
    def __init__(self,p):
        self.p=p
    def enter(self,e):
        pass
    def exit(self,e):
        pass
    def do(self):
        pass
    def draw(self):
        pass
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
        self.frame=0.0

        self.invincible_timer=0.0

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
        self.DIE=Die(self)
        
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
        attack_box = PlayerAttackBox(self.x, self.y, self.face_dir,DAMAGE_BARE_HANDS)
        game_world.add_object(attack_box, 1)
        game_world.add_collision_pair('player_attack:monster', attack_box, None)

    def get_bb(self):
        scale = 3
        draw_y = self.y + 145
        half_w = 32
        half_h = 64
        return self.x - half_w, draw_y - half_h, self.x + half_w, draw_y + half_h

    # ---

    # (신규) handle_collision() 메서드
    def handle_collision(self, group, other):
        if self.invincible_timer>0:
            return
        if group == 'player:monster':
            print("PLAYER collided with MONSTER")
            self.invincible_timer=0.5
            if self.face_dir==1:
                self.x-=10
            else:
                self.x +=10
            pass
        elif group == 'player:item':
            pass

    def update(self):
        dt= game_framework.frame_time
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            if self.invincible_timer < 0:
                self.invincible_timer = 0
                print("Invincibility finished.")

        self.x += self.vx*dt
        self.vy-= GRAVITY*dt
        self.y += self.vy*dt

        if self.y <= GROUND_Y + H // 2:
            self.y=GROUND_Y+H//2
            self.vy=0
            self.on_ground=True
        self.state_machine.update()

        w=get_canvas_width()
        half=16
        if self.x<half:
            self.x=half
        if self.x>w -half:
            self.x=w-half

    def draw(self):
        if self.invincible_timer>0:
            if int(get_time()*10)%2==0:
                pass
            else:
                return
        self.state_machine.draw()


