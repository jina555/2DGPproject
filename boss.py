from pico2d import *
from monster import Monster
from state_machine import StateMachine,State
import game_framework
import game_world
import random

GRAVITY=2500
RUSH_SPEED=700
JUMP_SPEED=1000

class BossSleep(State):
    def __init__(self, boss):
        self.boss = boss
        self.timer = 0

    def enter(self, e):
        self.boss.vx = 0
        self.boss.frame = 0
        self.timer = 0.5  # 0.5초 대기
        print("BOSS: Sleeping...")

    def do(self):
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            print("BOSS: WAKE UP!")
            self.boss.state_machine.set_state(self.boss.idle_state, e=None)

    def draw(self):
        self.boss.draw_body()
class BossIdle(State):
    def __init__(self, boss):
        self.boss = boss
        self.timer = 0

    def enter(self, e):
        self.boss.vx = 0
        self.boss.frame = 0
        self.timer = 1.0

    def do(self):
        self.boss.frame = (self.boss.frame + 4 * game_framework.frame_time)
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.boss.decide_action()  # 행동 결정

    def draw(self):
        self.boss.draw_body()

class BossWalk(State):
    def __init__(self, boss):
        self.boss = boss
        self.timer = 0

    def enter(self, e):
        player = game_world.get_player()
        if player:
            self.boss.face_dir = 1 if player.x > self.boss.x else -1
        self.boss.vx = 100 * self.boss.face_dir
        self.timer = 2.0

    def do(self):
        self.boss.x += self.boss.vx * game_framework.frame_time
        self.boss.frame = (self.boss.frame + 8 * game_framework.frame_time)
        self.timer -= game_framework.frame_time
        self.boss.x = clamp(50, self.boss.x, 950)
        if self.timer <= 0:
            self.boss.decide_action()

    def draw(self):
        self.boss.draw_body()

class BossRush(State):
    def __init__(self, boss):
        self.boss = boss
        self.timer = 0

    def enter(self, e):
        print("BOSS: RUSH!")
        player = game_world.get_player()
        if player:
            self.boss.face_dir = 1 if player.x > self.boss.x else -1
        self.boss.vx = RUSH_SPEED * self.boss.face_dir
        self.timer = 1.5

    def do(self):
        self.boss.x += self.boss.vx * game_framework.frame_time
        self.boss.frame = (self.boss.frame + 16 * game_framework.frame_time)
        self.timer -= game_framework.frame_time
        self.boss.x = clamp(50, self.boss.x, 950)
        if self.timer <= 0:
            # Boss1에 저장된 'idle_state' 객체로 전환
            self.boss.state_machine.set_state(self.boss.idle_state, e=None)

    def draw(self):
        self.boss.draw_body()

class Boss1Smash(State):
    def __init__(self, boss):
        self.boss = boss

    def enter(self, e):
        print("BOSS: SMASH!")
        self.boss.vy = JUMP_SPEED
        self.boss.vx = 0
        self.boss.on_ground = False

    def do(self):
        dt = game_framework.frame_time
        self.boss.vy -= GRAVITY * dt
        self.boss.y += self.boss.vy * dt

        if self.boss.y <= 250:  # 땅에 착지
            self.boss.y = 250
            self.boss.vy = 0
            print("BOSS: BOOM!")
            self.boss.state_machine.set_state(self.boss.idle_state, e=None)

    def draw(self):
        self.boss.draw_body()

class Boss(Monster):
    def __init__(self):
        super().__init__()
        self.x,self.y=800,250
        self.images=[]
        self.animation_speed=8
        self.width,self.height=200,200
        self.state_machine = None
        self.vy = 0
        self.idle_state=None
        pass

    def update(self):
        if self.state_machine:
            self.state_machine.update()

    def draw(self):
        if self.state_machine:
            self.state_machine.draw()
        else:
            self.draw_body()
    def draw_body(self):
        if not self.images: return
        img_index = int(self.frame) % len(self.images)
        if self.face_dir == 1:
            self.images[img_index].draw(self.x, self.y, self.width, self.height)
        else:
            self.images[img_index].composite_draw(0, 'h', self.x, self.y, self.width, self.height)
        self.draw_hp_bar()

    def draw_hp_bar(self):

        screen_center_x = 500  # 화면 가로 중앙 (1000 / 2)
        bar_y = 680  # 화면 상단 (725에서 조금 아래)
        max_width = 800  # 체력바 전체 길이
        bar_height = 20  # 체력바 두께
        hp_ratio = max(0, self.hp) / self.max_hp
        current_width = int(max_width * hp_ratio)
        left_edge = screen_center_x - (max_width // 2)
        draw_x = left_edge + (current_width // 2)
        if Monster.hp_bar_image and current_width > 0:
            Monster.hp_bar_image.draw(draw_x, bar_y, current_width, bar_height)

    def get_bb(self):

        half_w = self.width // 2 - 20
        half_h = self.height // 2 - 20
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        if group == 'player_attack:monster':
            damage = other.damage if hasattr(other, 'damage') else 10
            self.hp -= damage
            print(f"BOSS HIT! HP: {self.hp}")
            game_world.remove_object(other)

            if self.hp <= 0:
                game_world.remove_object(self)
                game_world.remove_collision_objects(self)
                return

        elif group == 'player:monster':
            if isinstance(self.state_machine.current, BossSleep):
                print("BOSS: Touched & Waking up!")
                if self.idle_state:
                    self.state_machine.set_state(self.idle_state, e=None)


class Boss1(Boss):
    def __init__(self):
        super().__init__()
        self.images=[
            load_image('boss1/bigslim_01.png'),
            load_image('boss1/bigslim_02.png'),
            load_image('boss1/bigslim_03.png'),
        ]

        self.max_hp=500
        self.hp=500 #보스 체력 나중에 수정
        self.damage=30#나중에 수정
        self.width=200
        self.height=200
        self.sleep_state = BossSleep(self)
        self.idle_state = BossIdle(self)
        self.walk_state = BossWalk(self)
        self.rush_state = BossRush(self)
        self.smash_state = Boss1Smash(self)
        self.state_machine = StateMachine(start_state=self.sleep_state, transitions={})

    def decide_action(self):
        roll = random.random()
        if roll < 0.4:
            # 객체 변수(self.rush_state)를 사용해서 상태 전환
            self.state_machine.set_state(self.rush_state, e=None)
        elif roll < 0.7:
            self.state_machine.set_state(self.smash_state, e=None)
        else:
            self.state_machine.set_state(self.walk_state, e=None)
    def handle_collision(self, group, other):
        super().handle_collision(group, other)

        if not isinstance(self.state_machine.current, BossSleep):
            if group == 'player_attack:monster' and self.hp > 0:
                if random.random() < 0.2:
                    print("BOSS1: COUNTER RUSH!")
                    self.state_machine.set_state(self.rush_state,e=None)


