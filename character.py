from pico2d import *
from sdl2 import SDL_KEYDOWN,SDL_KEYUP,SDLK_a,SDLK_d,SDLK_LSHIFT,SDLK_SPACE,SDLK_RSHIFT,SDL_BUTTON_LEFT,SDL_MOUSEBUTTONDOWN,SDLK_w
from state_machine import StateMachine,State
from item import Item, WEAPON_DAMAGE
import game_framework
import game_world
import math
from effect import SwordEffect


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
PIXEL_PER_METER = (64.0 / 1.75)
RUN_SPEED_KMPH = 25.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

MOVE_SPEED_RUN = RUN_SPEED_PPS
MOVE_SPEED_WALK = RUN_SPEED_PPS * 0.5

JUMP_SPEED_MPS = 10.0
JUMP_SPEED = JUMP_SPEED_MPS * PIXEL_PER_METER

GRAVITY_MPS = 25.0
GRAVITY = GRAVITY_MPS * PIXEL_PER_METER

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


W,H=32,64 #캐릭터 크기
GROUND_Y=80
ATTACK_ACTIVE=0.15 #히트박스 유지 시간
ATTACK_W=20 #공격박스 가로
ATTACK_H=30 #공격박스 세로

ITEM_DRAW_W, ITEM_DRAW_H = 53, 53
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
        # draw_rectangle(*self.get_bb(),255,0,0)
        pass

def _draw_weapon(p, state_name):
    if not p.equipped_weapon:
        return

    weapon_image = p.item_images.get(p.equipped_weapon)
    if not weapon_image:
        return

    offset_list = p.weapon_offset.get(state_name, p.weapon_offset['idle'])

    frame_index = clamp(0, int(p.frame), len(offset_list) - 1)
    base_offset_x, offset_y = offset_list[frame_index]
    offset_x = base_offset_x * p.face_dir
    draw_x = p.x + offset_x
    draw_y = p.y + offset_y
    weapon_degree=-170 * p.face_dir
    if p.face_dir == 1:
        weapon_image.composite_draw(weapon_degree,'',draw_x, draw_y ,ITEM_DRAW_W, ITEM_DRAW_H)
    else:
        weapon_image.composite_draw(weapon_degree, 'h', draw_x, draw_y, ITEM_DRAW_W, ITEM_DRAW_H)

    if p.hand_overlay_image:
        hand_img = p.hand_overlay_image

        # 무기가 그려진 위치를 기준으로 손의 위치를 미세 조정
        hand_draw_x = draw_x + (p.hand_offset[0] * p.face_dir)
        hand_draw_y = draw_y + p.hand_offset[1]

        if p.face_dir == 1:
            hand_img.draw(hand_draw_x, hand_draw_y, p.hand_w, p.hand_h)
        else:
            # 왼쪽을 볼 때는 손 이미지도 좌우 반전합니다.
            hand_img.composite_draw(0, 'h', hand_draw_x, hand_draw_y, p.hand_w, p.hand_h)


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
        offset_y=145*(scale-1)//2
        if self.p.face_dir==1:
            self.p.img_idle.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_idle.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)

        _draw_weapon(self.p,'idle')
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
        self.p.vx=0
        if self.p.a_down and not self.p.d_down:
            self.p.face_dir=-1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir=1
        else:
            self.p.state_machine.set_state(self.p.IDLE,e=None)
            return
        self.p.x+=self.p.face_dir * MOVE_SPEED_WALK * game_framework.frame_time
        if self.p.shift_down:
            self.p.state_machine.set_state(self.p.RUN, e=None)
            return
        self.p.frame=(self.p.frame + WALK_FRAMES_PER_ACTION * WALK_ACTION_PER_TIME * game_framework.frame_time)%WALK_FRAMES_PER_ACTION

    def draw(self):
        scale=3
        offset_y=145*(scale-1)//2

        if self.p.face_dir==1:
            self.p.img_move.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_move.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)

        _draw_weapon(self.p,'walk')
        pass


class Run:
    def __init__(self,p):
        self.p=p
    def enter(self,e):
        self.p.vx=0
        pass

    def exit(self,e):
        pass
    def do(self):
        if not self.p.shift_down:
            self.p.state_machine.set_state(self.p.IDLE, e=None)
            return

        if self.p.a_down and not self.p.d_down:
            self.p.face_dir = -1
        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir = 1

        self.p.vx=0
        self.p.x += self.p.face_dir * RUN_SPEED_PPS * game_framework.frame_time
        self.p.frame = (self.p.frame + RUN_FRAMES_PER_ACTION * RUN_ACTION_PER_TIME * game_framework.frame_time) % RUN_FRAMES_PER_ACTION

        if self.p.space_down:
            self.p.state_machine.set_state(self.p.JUMP, e=None)
            return
    def draw(self):
        scale=3
        offset_y=145*(scale-1)//2

        if self.p.face_dir==1:
            self.p.img_run.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_run.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)

        _draw_weapon(self.p,'run')
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

        self.p.vx = 0
        if self.p.a_down and not self.p.d_down:
            self.p.face_dir = -1

            self.p.x -= MOVE_SPEED_RUN * game_framework.frame_time

        elif self.p.d_down and not self.p.a_down:
            self.p.face_dir = 1

            self.p.x += MOVE_SPEED_RUN * game_framework.frame_time


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
        offset_y=145*(scale-1)//2

        if self.p.face_dir==1:
            self.p.img_jump.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_jump.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)

        _draw_weapon(self.p,'jump')
        pass


class Attack:
    def __init__(self,p):
        self.p=p
    def enter(self,e):
        self.p.frame=0
        self.p.attack_time=ATTACK_TIME_PER_ACTION
        self.attacked=False

    def exit(self,e):
        pass

    def do(self):
        self.p.frame=(self.p.frame + ATTACK_FRAMES_PER_ACTION * ATTACK_ACTION_PER_TIME * game_framework.frame_time)%ATTACK_FRAMES_PER_ACTION
        self.p.attack_time -= game_framework.frame_time
        if self.p.frame >= 2.0 and not self.attacked:
            # 1) 이펙트 생성
            self.spawn_effect()

            # 2) 공격 판정(Hitbox) 생성 (칼 휘두르는 타이밍에 맞춤)
            self.p.start_attack()

            # 3) "나 공격 했음!" 표시 (중복 실행 방지)
            self.attacked = True

            # 3. 공격 종료 체크
        if self.p.attack_time < 0:
            if self.p.a_down != self.p.d_down:
                self.p.state_machine.set_state(self.p.WALK, e=None)
            else:
                self.p.state_machine.set_state(self.p.IDLE, e=None)
            return

    def spawn_effect(self):

        effect_type_to_spawn = 'normal'
        if self.p.equipped_weapon == 'WEAPON_S_2':
            effect_type_to_spawn = 'weapon_s_2_effect'
        elif self.p.equipped_weapon == 'WEAPON4':
            effect_type_to_spawn = 'weapon_4_effect'
        elif self.p.equipped_weapon == 'WEAPON3':
            effect_type_to_spawn = 'weapon_3_effect'
        elif self.p.equipped_weapon == 'WEAPON_S':
            effect_type_to_spawn = 'special_s'
        elif self.p.equipped_weapon is None:
            effect_type_to_spawn = 'bare_hand'

        offset_list = self.p.weapon_offset.get('attack', self.p.weapon_offset['idle'])

        base_offset_x, offset_y = offset_list[2]
        offset_x = base_offset_x * self.p.face_dir

        effect_x = self.p.x + offset_x
        effect_y = self.p.y + offset_y

        effect = SwordEffect(effect_x, effect_y, self.p.face_dir, effect_type_to_spawn)
        game_world.add_object(effect, 2)

    def draw(self):
        scale=3
        offset_y=145*(scale-1)//2

        if self.p.face_dir==1:
            self.p.img_attack.clip_draw(int(self.p.frame)*32,0,32,64,self.p.x,self.p.y+offset_y,32*scale,64*scale)
        else:
            self.p.img_attack.clip_composite_draw(int(self.p.frame)*32,0,32,64,0,'h',self.p.x,self.p.y+offset_y,32*scale,64*scale)

        _draw_weapon(self.p,'attack')
        pass

# class Die:
#     def __init__(self,p):
#         self.p=p
#     def enter(self,e):
#
#         pass
#     def exit(self,e):
#         pass
#     def do(self):
#         pass
#     def draw(self):
#         pass
#     pass

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
        self.invincible=False
        self.invincible_timer=0.0
        self.scale=1.0

        self.max_hp=300
        self.hp=300

        self.img_idle=load_image('res/idle.png')
        self.img_move=load_image('res/character_MOVE.png')
        self.img_run=load_image('res/character_MOVE.png')
        self.img_jump=load_image('res/character_JUMP.png')
        self.img_attack=load_image('res/character_ATTACK.png')

        self.item_images = {
            'WEAPON1': load_image('item/무기1.png'),
            'WEAPON2': load_image('item/무기2.png'),
            'WEAPON_S': load_image('item/무기s.png'),

            'WEAPON3': load_image('item/weapon3.png'),
            'WEAPON4': load_image('item/weapon4.png'),
            'WEAPON_S_2': load_image('item/weapons_2.png'),

            'WEAPON5': load_image('item/무기_22.png'),
            'WEAPON6': load_image('item/무기_23.png'),
            'WEAPON_S_3': load_image('item/무기_24.png'),
        }

        self.weapon_offset = {
            'idle': [(7, 85),(7,82),(7,85),(7,82)],
            'walk': [(7, 85),(6,80),(7,85),(7,85)],
            'run': [(7,85),(6,80),(7,85),(7,85)],
            'jump': [(5,80),(0,90),(3,110),(2,100),(2,90),(5,80)],
            'attack': [(5,85), (-20, 120), (45,90), (25,85)]
        }

        self.a_down=False
        self.d_down=False
        self.shift_down=False
        self.w_down=False

        self.attack_time=0
        self.attack_box=(0,0,0,0)

        self.colliding_item_list=[]
        self.inventory=[]
        self.max_inventory_slots=25
        self.equipped_weapon=None

        self.hand_overlay_image = load_image('res/hand.png')

        self.hand_w, self.hand_h = 120, 120

        self.hand_offset = (-5, 33)

        self.IDLE=Idle(self)
        self.WALK=Walk(self)
        self.RUN=Run(self)
        self.JUMP=Jump(self)
        self.ATTACK=Attack(self)
        # self.DIE=Die(self)
        
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
                self.try_pickup()
            elif event.key ==SDLK_w:
                self.w_down=True


        elif event.type==SDL_KEYUP:
            if event.key==SDLK_a:
                self.a_down=False
            elif event.key==SDLK_d:
                self.d_down=False
            elif event.key==SDLK_LSHIFT:
                self.shift_down=False
            elif event.key==SDLK_w:
                self.w_down=False

        # elif event.type==SDL_MOUSEBUTTONDOWN and event.button==SDL_BUTTON_LEFT:
        #     self.start_attack()

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
        current_damage = WEAPON_DAMAGE.get(self.equipped_weapon, DAMAGE_BARE_HANDS)
        print(f"Attack damage: {current_damage} ({self.equipped_weapon})")
        attack_box = PlayerAttackBox(self.x, self.y, self.face_dir,current_damage)
        game_world.add_object(attack_box, 1)
        game_world.add_collision_pair('player_attack:monster', attack_box, None)

    def get_bb(self):

        return self.x -32,self.y+50,self.x+32,self.y+164

    def handle_collision(self, group, other):
        if self.invincible_timer>0:
            return
        if group == 'player:monster':
            print("PLAYER collided with MONSTER")
            self.hp-=5
            if self.hp<0:self.hp=0
            print(f"Player Hp:{self.hp}")
            self.invincible_timer=0.5
            if self.face_dir==1:
                self.x-=10
            else:
                self.x +=10
            pass
        elif group == 'player:item':
            if other not in self.colliding_item_list:
                self.colliding_item_list.append(other)
            pass

    def try_pickup(self):
        for item in self.colliding_item_list:
            if self.add_to_inventory(item):
                game_world.remove_object(item)

                self.colliding_item_list.remove(item)

                return
    def add_to_inventory(self, item):
        if item.item_type.startswith('WEAPON'):

            if self.equipped_weapon == item.item_type:
                print(f"Already equipped {item.item_type}.")
                return False

            if item.item_type in self.inventory:
                print(f"Already have {item.item_type} in bag.")
                return False

        if len(self.inventory) < self.max_inventory_slots:
            self.inventory.append(item.item_type)
            print(f"Inventory: {self.inventory}")
            return True
        print("inventory is full")
        return False

    def equip_item(self, inventory_index):

        if not (0 <= inventory_index < len(self.inventory)):
            print("Invalid inventory index")
            return

        item_type=self.inventory[inventory_index]

        if item_type in ['POTION1', 'POTION2','POTION3']:
            heal_amount = 0
            if item_type == 'POTION1':
                heal_amount = 30  # 포션1 회복량
            elif item_type == 'POTION2':
                heal_amount = 50  # 포션2 회복량
            else:
                heal_amount=60
            self.hp += heal_amount
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            self.inventory.pop(inventory_index)
            return
        item_to_equip = self.inventory[inventory_index]
        old_equipped_weapon=self.equipped_weapon
        self.equipped_weapon=item_to_equip

        if old_equipped_weapon :
            self.inventory[inventory_index]=old_equipped_weapon
        else:
            self.inventory.pop(inventory_index)
    def increase_max_hp(self,amount):
        self.max_hp += amount
        self.hp+=amount

    def update(self):
        self.colliding_item_list=[]

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
       self.state_machine.draw()

        # draw_rectangle(*self.get_bb(), 255, 0, 0)



