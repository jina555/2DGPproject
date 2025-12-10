from pico2d import *
import game_framework
import start_mode
bgm=None
def init():
    global image, logo_time,bgm
    bgm = load_music('sound/ending_bgm.mp3')
    bgm.set_volume(40)
    bgm.repeat_play()

    image=load_image('res2/game_clear.png')
    logo_time=0.0
    pass
def finish():
    global image,bgm
    del image
    if bgm:
        bgm.stop()
        bgm = None
def update():
    global logo_time
    logo_time += game_framework.frame_time

    if logo_time >= 3.0:
        logo_time=0
        game_framework.change_mode(start_mode)
    pass
def draw():
    clear_canvas()
    image.draw(500,362)
    update_canvas()
    pass
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
    pass