from pico2d import *
import game_framework
import play_mode
import random

CANVAS_WIDTH=1280
CANVAS_HEIGHT=800


background=None
start_button=None
start_button_rect=None

def init():
    global background,title,start_button,start_button_rect

    background=load_image('background.png')
    title=load_image('타이틀.png')
    start_button=load_image('타이틀_start.png')

    btn_x=CANVAS_WIDTH//2
    btn_y=120
    start_scale=3
    btn_w=start_button.w*start_scale
    btn_h=start_button.h*start_scale

    left=btn_x-btn_w/2
    bottom=btn_y-btn_h/2
    right=btn_x+btn_w/2
    top=btn_y+btn_h/2
    start_button_rect=(left,bottom,right,top)
    print("start mode initialized")


    pass
def finish():
    global background,title,start_button
    if background:del background
    if title:del title
    if start_button:del start_button
    print("start mode finished")
    pass
def handle_events():
    global start_button_rect
    events=get_events()
    for event in events:
        if event.type==SDL_QUIT:
            game_framework.quit()
        elif event.type==SDL_KEYDOWN and event.key==SDLK_ESCAPE:
            game_framework.quit()
        elif event.type==SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mx,my=event.x,CANVAS_HEIGHT-event.y
            left,bottom,right,top=start_button_rect
            game_framework.change_mode(play_mode)



    pass
def update():
    pass
def draw():
    global background, title, start_button, start_button_rect
    clear_canvas()

    background.draw(CANVAS_WIDTH//2,CANVAS_HEIGHT//2,CANVAS_WIDTH,CANVAS_HEIGHT)
    title_scale=3
    title.draw(CANVAS_WIDTH//2,CANVAS_HEIGHT-200,title.w*title_scale, title.h*title_scale)

    (left, bottom,right,top) = start_button_rect
    btn_x=(left+right)/2
    btn_y=(bottom+top)/2
    start_button.draw(btn_x, btn_y,(right-left),(top-bottom))
    update_canvas()
    pass
def pause():
    pass
def resume():
    pass
