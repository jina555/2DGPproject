from pico2d import *
from monster import Monster
from state_machine import StateMachine,State
import game_framework
import game_world
import random
from fireball import Fireball
from monster import Skeleton

PIXEL_PER_METER = (64.0 / 1.75)

WALK_SPEED_KMPH = 5.0
WALK_SPEED_PPS = (WALK_SPEED_KMPH * 1000.0 / 60.0/60.0) * PIXEL_PER_METER

RUSH_SPEED_KMPH = 40.0
RUSH_SPEED_PPS = (RUSH_SPEED_KMPH * 1000.0 / 60.0/60.0) * PIXEL_PER_METER

JUMP_SPEED_MPS = 15.0
JUMP_SPEED = JUMP_SPEED_MPS * PIXEL_PER_METER

GRAVITY_MPS = 30.0
GRAVITY = GRAVITY_MPS * PIXEL_PER_METER

BOSS_IDLE_TIME_PER_ACTION = 1.0
BOSS_IDLE_ACTION_PER_TIME = 1.0 / BOSS_IDLE_TIME_PER_ACTION

BOSS_WALK_TIME_PER_ACTION = 1.5
BOSS_WALK_ACTION_PER_TIME = 1.0 / BOSS_WALK_TIME_PER_ACTION

BOSS_RUSH_TIME_PER_ACTION = 0.5
BOSS_RUSH_ACTION_PER_TIME = 1.0 / BOSS_RUSH_TIME_PER_ACTION

BOSS_SMASH_TIME_PER_ACTION = 0.5
BOSS_SMASH_ACTION_PER_TIME = 1.0 / BOSS_SMASH_TIME_PER_ACTION

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
        total_frames = len(self.boss.images)
        self.boss.frame = (self.boss.frame + total_frames * BOSS_IDLE_ACTION_PER_TIME * game_framework.frame_time)
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
        self.boss.vx = WALK_SPEED_PPS * self.boss.face_dir
        self.timer = 2.0

    def do(self):
        self.boss.x += self.boss.vx * game_framework.frame_time
        self.timer -= game_framework.frame_time
        self.boss.x = clamp(50, self.boss.x, 950)
        total_frames=len(self.boss.images)
        self.boss.frame=(self.boss.frame + total_frames * BOSS_WALK_ACTION_PER_TIME* game_framework.frame_time)
        self.timer -=game_framework.frame_time
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
        self.boss.vx = RUSH_SPEED_PPS * self.boss.face_dir
        self.timer = 1.5

    def do(self):
        self.boss.x += self.boss.vx * game_framework.frame_time
        self.timer -= game_framework.frame_time
        self.boss.x = clamp(50, self.boss.x, 950)
        total_frames = len(self.boss.images)
        self.boss.frame = (self.boss.frame + total_frames * BOSS_RUSH_ACTION_PER_TIME * game_framework.frame_time)
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
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
        self.frame=0

    def do(self):
        dt = game_framework.frame_time
        self.boss.vy -= GRAVITY * dt
        self.boss.y += self.boss.vy * dt
        total_frames = len(self.boss.images)
        self.boss.frame = (self.boss.frame + total_frames * BOSS_SMASH_ACTION_PER_TIME * dt)

        if self.boss.y <= 275:  # 땅에 착지
            self.boss.y = 275
            self.boss.vy = 0
            print("BOSS: BOOM!")
            self.boss.state_machine.set_state(self.boss.idle_state, e=None)

    def draw(self):
        self.boss.draw_body()

class Boss(Monster):
    def __init__(self):
        super().__init__()
        self.x,self.y=800,275
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
        draw_rectangle(*self.get_bb(), 255, 0, 0)
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
        bar_height = 20 # 체력바 두께
        if Monster.hp_bg_image:
            Monster.hp_bg_image.draw(screen_center_x, bar_y, max_width, bar_height)

        hp_ratio = max(0, self.hp) / self.max_hp
        current_width = int(max_width * hp_ratio)
        left_edge = screen_center_x - (max_width // 2)
        draw_x = left_edge + (current_width // 2)
        if Monster.hp_bar_image and current_width > 0:
            Monster.hp_bar_image.draw(draw_x, bar_y, current_width, bar_height)

    def get_bb(self):

        half_w = self.width // 2 - 20

        return self.x - half_w, self.y - 105, self.x + half_w, self.y + 55

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

        self.max_hp=100
        self.hp=100 #보스 체력 나중에 수정
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


class Boss2Appear:
    def __init__(self, boss):
        self.boss = boss
        self.move_speed = 100.0  # 등장 속도

    def enter(self, e):
        print("BOSS2: Appear from right...")
        self.boss.frame = 0
        self.boss.x = 1200
        self.boss.vx = -self.move_speed  # 왼쪽으로 이동

    def do(self):
        dt = game_framework.frame_time
        self.boss.x += self.boss.vx * dt

        total_frames = len(self.boss.images)
        self.boss.frame = (self.boss.frame + total_frames * BOSS_WALK_ACTION_PER_TIME * dt)

        if self.boss.x <= 900:
            self.boss.x = 900
            self.boss.vx = 0
            print("BOSS2: Arrival Complete. Idle Mode.")
            self.boss.state_machine.set_state(self.boss.idle_state, e=None)

    def draw(self):
        self.boss.draw_body()
    pass


class Boss2Idle:
    def __init__(self, boss):
        self.boss = boss
        self.timer=0

    def enter(self, e):
        self.boss.vx = 0
        self.timer=2.0


    def do(self):
        dt = game_framework.frame_time
        self.timer -= dt

        total_frames = len(self.boss.images)
        self.boss.frame = (self.boss.frame + total_frames * BOSS_IDLE_ACTION_PER_TIME * dt)

        if self.timer <= 0:
            self.boss.decide_action()

    def draw(self):
        self.boss.draw_body()
    pass

class Boss2Attack:
    def __init__(self, boss, x_off=100, y_off=-100, w=100, h=100, damage=30):
        self.boss = boss
        self.x_off = x_off
        self.y_off = y_off
        self.w = w
        self.h = h
        self.damage = damage
        self.timer = 0
        self.fired = False
        pass
    def enter(self, e):
        self.boss.vx=0
        self.timer=1.0
        self.fired=False

        player = game_world.get_player()
        if player:
            self.boss.face_dir = 1 if player.x > self.boss.x else -1
        pass
    def do(self):
        dt=game_framework.frame_time
        self.timer-=dt

        if self.timer <= 0.5 and not self.fired:
            self.fire()
            self.fired=True
        total_frames = len(self.boss.images)
        self.boss.frame=(self.boss.frame + total_frames * dt)

        if self.timer <= 0:
            self.boss.state_machine.set_state(self.boss.idle_state, e=None)
        pass
    def fire(self):
        fire_x = self.boss.x + (self.x_off * self.boss.face_dir)
        fire_y = self.boss.y + self.y_off

        fireball=Fireball(fire_x, fire_y,self.boss.face_dir,self.w,self.h,self.damage)
        game_world.add_object(fireball,1)

        game_world.add_collision_pair('monster_attack:player',fireball,None)
        pass
    def draw(self):
        self.boss.draw_body()
        pass

class Boss2(Boss):
    def __init__(self):
        super().__init__()
        self.name='cobra'

        self.images = [
            load_image('boss2/cobra1.png'),
            load_image('boss2/cobra2.png'),
            load_image('boss2/cobra3.png'),
        ]
        self.width = 400
        self.height = 400
        self.x = 1200
        self.y = 380
        self.max_hp = 200 #보스2 체력 수정 예정
        self.hp = 200
        self.face_dir = -1

        self.appear_state = Boss2Appear(self)
        self.idle_state = Boss2Idle(self)
        self.attack_state=Boss2Attack(self)

        self.state_machine = StateMachine(start_state=self.appear_state, transitions={})
        pass
    def get_bb(self):
        return self.x-160,self.y-200,self.x+140,self.y+120
    def decide_action(self):
        roll=random.random()

        if roll < 0.7:
            self.state_machine.set_state(self.attack_state, e=None)
        else:
            self.state_machine.set_state(self.idle_state, e=None)

        pass
    def handle_collision(self, group, other):
        super().handle_collision(group,other)
        pass


class Boss3Spawn:
    pass


class Boss3(Boss):
    def __init__(self):
        super().__init__()
        self.name='queen'
        self.images = [
            load_image('boss3/queen.png'),
            load_image('boss3/queen2.png'),
            load_image('boss3/queen3.png'),
        ]
        self.y=270
        self.max_hp = 100
        self.hp = 100  # 보스 체력 나중에 수정
        self.damage = 30  # 나중에 수정
        self.width = 200
        self.height = 200
        self.sleep_state = BossSleep(self)
        self.idle_state = BossIdle(self)
        self.walk_state = BossWalk(self)
        self.rush_state=BossRush(self)
        self.attack_state = Boss2Attack(self, x_off=80, y_off=-20, w=100, h=100, damage=20)
        self.spawn_state = Boss3Spawn(self)
        self.state_machine = StateMachine(start_state=self.sleep_state, transitions={})
        pass
    def get_bb(self):
        return self.x - 70, self.y - 100, self.x + 90, self.y + 80

        pass
    def decide_action(self):
        roll = random.random()
        if self.hp > 70:
            if roll < 0.3:
                self.state_machine.set_state(self.idle_state, e=None)
            elif roll < 0.7:
                self.state_machine.set_state(self.walk_state, e=None)
            else:
                self.state_machine.set_state(self.rush_state, e=None)

        elif self.hp > 40:
            if roll < 0.6:
                self.state_machine.set_state(self.attack_state, e=None)
            else:
                self.state_machine.set_state(self.rush_state, e=None)

        else:
            if roll < 0.4:
                self.state_machine.set_state(self.spawn_state, e=None)
            elif roll < 0.7:
                self.state_machine.set_state(self.attack_state, e=None)
            else:  
                self.state_machine.set_state(self.rush_state, e=None)


    def handle_collision(self, group, other):
        super().handle_collision(group, other)
        pass