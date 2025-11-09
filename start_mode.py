from pico2d import *
import game_framework
import play_mode
import random

CANVAS_WIDTH=1280
CANVAS_HEIGHT=725
GROUND_Y=300 # 캐릭터들이 걸어갈 위치
TRIGGER_X=CANVAS_WIDTH *(2/3)
SHADOW_DURATION=0.5


background=None
start_button=None
start_button=None
start_button_rect=None
is_mouse_over_button=False

character=[]
shadow_img=None
shadow_locations=[]
shadow_timer=0.0
last_update_time=0.0

class StartCharacter:
    def __init__(self,img,start_x,speed):
        self.img=img
        self.start_x=start_x
        self.x=start_x
        self.y=GROUND_Y
        self.speed=speed

        self.frame=random.randint(0,3)
        self.frame_timer=0.0
        self.anim_speed=0.15
    def update_animation(self,dt):
        self.frame_timer += dt
        if self.frame_timer > self.anim_speed:
            self.frame=(self.frame +1)%4
            self.frame_timer=0.0
    def draw(self):
        frame_w=32
        frame_h=64
        scale=2
        self.img.clip_draw(self.frame*frame_w,0,frame_w,frame_h,self.x,self.y,frame_w*scale,frame_h*scale)
    def reset(self):
        self.x=self.start_x
        self.frame=random.randint(0,3)


def init():
    global background,title,start_button,start_button_rect,is_mouse_over_button
    global characters,shadow_img,shadow_timer, last_update_time

    background=load_image('res/background.png')
    title=load_image('res/title.png')
    start_button=load_image('res/타이틀_start.png')

    shadow_img=load_image('res/shadow.png')
    characters=[
        StartCharacter(img=load_image('res/character_MOVE.png'),start_x=-60,speed=1.8),
        StartCharacter(img=load_image('res/캐릭터2.png'),start_x=-20,speed=2.0),
        StartCharacter(img=load_image('res/캐릭터3.png'),start_x=-100,speed=2.2),
        StartCharacter(img=load_image('res/캐릭터4.png'),start_x=-40,speed=1.9),
    ]

    btn_x=CANVAS_WIDTH//2
    btn_y=120
    start_scale=2
    btn_w=start_button.w*start_scale
    btn_h=start_button.h*start_scale

    left=btn_x-btn_w/2
    bottom=btn_y-btn_h/2
    right=btn_x+btn_w/2
    top=btn_y+btn_h/2
    start_button_rect=(left,bottom,right,top)
    is_mouse_over_button=False

    shadow_timer=0.0
    last_update_time=get_time()
    print("start mode initialized")


    pass
def finish():
    global background,title,start_button,characters,shadow_img
    if background:del background
    if title:del title
    if start_button:del start_button
    if shadow_img:del shadow_img
    for char in characters:
        if char.img:del char.img
    characters.clear()

    print("start mode finished")
    pass
def handle_events():
    global start_button_rect,is_mouse_over_button
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            game_framework.quit()
        elif event.type==SDL_MOUSEMOTION:
            mx,my=event.x,CANVAS_HEIGHT-event.y
            (left, bottom,right,top) = start_button_rect
            if left < mx<right and bottom < my<top:
                is_mouse_over_button=True
            else:
                is_mouse_over_button=False
        elif event.type==SDL_MOUSEBUTTONDOWN and event.button==SDL_BUTTON_LEFT:
            if is_mouse_over_button:
                game_framework.change_mode(play_mode)




    pass
def update():
    global shadow_timer, last_update_time, characters, shadow_locations, TRIGGER_X

    now = get_time()
    dt = now - last_update_time
    last_update_time = now

    if shadow_timer > 0:

        shadow_timer -= dt
        if shadow_timer <= 0:

            shadow_locations.clear()
            for char in characters:
                char.reset()

    else:

        all_past_trigger = True

        for char in characters:

            char.x += char.speed * dt * 100

            char.update_animation(dt)

            if char.x < TRIGGER_X:
                all_past_trigger = False


        if all_past_trigger:
            shadow_timer = SHADOW_DURATION
            shadow_locations.clear()

            for char in characters:
                shadow_locations.append((char.x, char.y))


    pass
def draw():
    global background, title, start_button, start_button_rect,is_mouse_over_button
    global characters, shadow_img,shadow_locations, shadow_timer
    clear_canvas()

    background.draw(CANVAS_WIDTH//2,CANVAS_HEIGHT//2,CANVAS_WIDTH,CANVAS_HEIGHT)

    if shadow_timer>0:
        for x,y in shadow_locations:
            shadow_img.draw(x,y-60)
    else:
        for char in characters:
            char.draw()
    title.scale=1.8

    title.draw(CANVAS_WIDTH//2-70,CANVAS_HEIGHT-200,title.w*title.scale, title.h*title.scale)

    (left, bottom,right,top) = start_button_rect
    btn_x=(left+right)/2
    btn_y=(bottom+top)/2
    btn_w=(right-left)
    btn_h=(top-bottom)
    if is_mouse_over_button:
        start_button.draw(btn_x,btn_y,btn_w*1.1, btn_h*1.1)
    else:
        start_button.draw(btn_x,btn_y,btn_w, btn_h)


    update_canvas()
    pass
def pause():
    pass
def resume():
    pass
