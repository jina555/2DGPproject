from pico2d import *
from monster import Monster
import game_framework

class Boss(Monster):
    def __init__(self):
        super().__init__()
        self.x=800
        self.y=250
        self.images=[]
        self.animation_speed=8
        self.width=200
        self.height=200
        pass

    def update(self):
        super().update()
        self.frame=(self.frame+self.animation_speed*game_framework.frame_time)

    def draw(self):
        if not self.images:
            return

        img_index = int(self.frame) % len(self.images)

        if self.face_dir == 1:
            self.images[img_index].draw(self.x, self.y)
        else:
            self.images[img_index].composite_draw(0, 'h', self.x, self.y)

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
            print(f"=== BOSS HIT! HP: {self.hp} / {self.max_hp} ===")

            if self.hp <= 0:
                self.state_machine.set_state(self.DIE, e=None)
            else:

                self.state_machine.set_state(self.ATTACK, e=None)

        elif group == 'player:monster':
            print("boss attack")
            self.state_machine.set_state(self.ATTACK, e=None)

            pass

class Boss1(Boss):
    def __init__(self):
        super().__init__()
        self.images=[
            load_image('boss1/bigslim_01.png'),
            load_image('boss1/bigslim_02.png'),
            load_image('boss1/bigslim_03.png'),
        ]

        self.max_hp=20
        self.hp=20 #보스 체력 나중에 수정

        self.damage=30
        self.width=200
        self.height=200

