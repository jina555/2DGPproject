from pico2d import *
from character import Character
from map import Map
import game_framework
running=True
world = []
player= None


def init():
    global world,player
    world = []
    game_map = Map()
    world.append(game_map)
    player = Character()
    world.append(player)
    pass
def finish():
    global world,player
    world.clear()
    player=None


def handle_events():
    global player

    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)
    pass


def update():
    for o in world:
        o.update()

    pass


def draw():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()
    pass

def pause():
    pass
def resume():
    pass



