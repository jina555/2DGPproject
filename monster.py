from pico2d import *
import game_framework
import game_world
from state_machine import StateMachine, State
import random
from item import Item

WALK_FRAMES_PER_ACTION=5
WALK_TIME_PER_ACTION=1.0
WALK_ACTION_PER_TIME=1.0/WALK_TIME_PER_ACTION

ATTACK_FRAMES_PER_ACTION=4
ATTACK_TIME_PER_ACTION=0.8
ATTACK_ACTION_PER_TIME=1.0/ATTACK_TIME_PER_ACTION

HURT_FRAMES_PER_ACTION = 4
HURT_TIME_PER_ACTION = 0.5 # 0.5초간 아파함
HURT_ACTION_PER_TIME = 1.0 / HURT_TIME_PER_ACTION

W,H=32,32
MOVE_SPEED=150
HP_BAR_MAX_WIDTH = 50
HP_BAR_HEIGHT = 5
HP_BAR_Y_OFFSET = 5

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
        self.p=p
        pass
    def enter(self,e):
        print("monster:attack")
        self.p.vx=0
        self.p.attack_timer=ATTACK_TIME_PER_ACTION*1.0
        self.p.frame=0
        pass
    def exit(self,e):
        print("monster:attack exit")
        pass
    def do(self):
        self.p.frame=self.p.frame + ATTACK_FRAMES_PER_ACTION * ATTACK_ACTION_PER_TIME * game_framework.frame_time
        self.p.attack_timer -=game_framework.frame_time
        if self.p.attack_timer <0:
            self.p.state_machine.set_state(self.p.WALK, e=None)

        pass
    def draw(self):
        frame_to_draw=min(int(self.p.frame), ATTACK_FRAMES_PER_ACTION-1)
        if self.p.face_dir==1:
            self.p.img_attack.clip_composite_draw(frame_to_draw*W,0,W,H,0,'h',self.p.x,self.p.y,W*3,H*3)
        else:
            self.p.img_attack.clip_draw(frame_to_draw*W,0,W,H,self.p.x,self.p.y,W*3,H*3)
        pass
    pass
class Hurt(State):
    def __init__(self,p):
        self.p=p
        pass
    def enter(self,e):
        print('monster:hurt')
        self.p.vx=0
        self.p.frame=0
        self.p.hurt_timer=HURT_TIME_PER_ACTION*1.0
        pass
    def exit(self,e):
        print('monster:hurt exit')
        pass
    def do(self):
        self.p.frame = self.p.frame + HURT_FRAMES_PER_ACTION * HURT_ACTION_PER_TIME * game_framework.frame_time
        self.p.hurt_timer -= game_framework.frame_time
        if self.p.hurt_timer < 0:
            if self.p.hp <= 0:
                self.p.state_machine.set_state(self.p.DIE, e=None)
            else:
                self.p.state_machine.set_state(self.p.WALK, e=None)
            pass
    def draw(self):
        frame_to_draw = min(int(self.p.frame), HURT_FRAMES_PER_ACTION - 1)
        if self.p.face_dir == 1:
            self.p.img_hurt.clip_composite_draw(frame_to_draw * W, 0, W, H, 0, 'h', self.p.x, self.p.y, W * 3, H * 3)
        else:
            self.p.img_hurt.clip_draw(frame_to_draw * W, 0, W, H, self.p.x, self.p.y, W * 3, H * 3)

    pass

class Die(State):
    def __init__(self,p):
        self.p=p
        pass
    def enter(self,e):
        print('monster:die')
        game_world.remove_collision_objects(self.p)
        self.p.drop_item()
        game_world.remove_object(self.p)
        pass
    def exit(self,e):pass
    def do(self):pass
    def draw(self):pass
    pass

class Monster:
    hp_bar_image=None
    def __init__(self):
        self.x=random.randint(300,1000)
        self.face_dir=random.choice([-1,1])
        self.vx=MOVE_SPEED * self.face_dir
        monster_half_h = (H * 3) // 2
        self.y = 161 + monster_half_h
        self.frame=0.0

        self.max_hp=100
        self.hp=100


        self.img_walk=load_image('res/monster1_walk.png')
        self.img_attack=load_image('res/monster1_attack.png')
        self.img_hurt=load_image('res/monster1_hurt.png')

        if Monster.hp_bar_image is None:
            Monster.hp_bar_image=load_image('res/hp_bar.png')

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
        if self.state_machine.current != self.DIE:
            _, _, _, top = self.get_bb()
            bar_y = top + HP_BAR_Y_OFFSET
            current_hp_width = int((self.hp / self.max_hp) * HP_BAR_MAX_WIDTH)
            if current_hp_width < 0:
                current_hp_width = 0
            Monster.hp_bar_image.draw(self.x, bar_y, current_hp_width, HP_BAR_HEIGHT)



        pass
    def get_bb(self):
        half_w=30
        half_h=30
        return self.x-half_w,self.y-half_h,self.x+half_w,self.y+half_h
        pass
    def handle_collision(self,group,other):
        if self.state_machine.current in (self.HURT, self.ATTACK, self.DIE):
            return

            # 2. (수정) 우선순위 1: 'player:monster' (몸통) 먼저 검사
        if group == 'player:monster':
            print("MONSTER: Collided with PLAYER, changing to ATTACK")
            self.state_machine.set_state(self.ATTACK, e=None)

            # 3. (수정) 우선순위 2: 'player_attack' (맞았을 때) 나중에 검사
        elif group == 'player_attack:monster':
            print("MONSTER: Collided with PLAYER_ATTACK, changing to HURT")
            damage = 0
            if hasattr(other, 'damage'):
                damage = other.damage
            else:
                damage = 20

            self.hp -= damage
            print(f"MONSTER HP: {self.hp}")

            # (수정) HP와 상관없이 HURT로 가고, HURT.do()가 DIE를 결정
            self.state_machine.set_state(self.HURT, e=None)

        pass
    def drop_item(self):
        roll=random.random()
        item_to_drop=None

        if roll < 0.10:
            item_to_drop='WEAPON_S'
        elif roll < 0.60:
            if random.random() < 0.5:
                item_to_drop='WEAPON1'
            else:
                item_to_drop='WEAPON2'

        if item_to_drop:  # 아이템을 드랍하기로 결정됐다면
            print(f"Dropping {item_to_drop}")
            new_item = Item(self.x, self.y, item_to_drop)
            game_world.add_object(new_item, 1)

            # (수정) game_world에서 player 객체를 가져와서 충돌 페어에 등록
            player = game_world.get_player()
            if player:
                game_world.add_collision_pair('player:item', player, new_item)
            else:
                # 혹시 모르니 player가 없을 경우의 처리
                game_world.add_collision_pair('player:item', None, new_item)




    def remove_self(self):
        pass
