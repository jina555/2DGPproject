from pico2d import *

MOVE_SPEED=300
JUMP_SPEED=900
W,H=50,70 #캐릭터 크기
GROUND_Y=80
ATTACK_ACTIVE=0.15 #히트박스 유지 시간
ATTACK_W=60 #공격박스 가로
ATTACK_H=40 #공격박스 세로

class Character:
    def __init__(self):
        self.x=400
        self.y=GROUND_Y+H//2
        self.vx=0
        self.vy=0#점프나 낙하시
        self.on_ground=True
        self.face_dir=1 #1:오른쪽, -1:왼쪽

    def handle_event(self,event):
        if event.type==SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.left_down=True
            elif event.key==SDLK_d:
                self.right_down=True
            elif event.key == SDLK_LSHIFT:
                self.shift_down=True
            elif event.key==SDLK_SPACE:
                self.jump()
            elif event.key ==SDLK_f:
                self.pickup()


        elif event.type==SDL_KEYUP:
            if event.key==SDLK_a:
                self.left_down=False
            elif event.key==SDLK_d:
                self.right_down=False
            elif event.key==SDLK_LSHIFT:
                self.shift_down=False

        elif event.type==SDL_MOUSEBUTTONDOWN and event.button==SDL_BUTTON_LEFT:
            self.start_attack()


