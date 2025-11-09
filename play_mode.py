from pico2d import *
from character import Character
from map import Map
from grass import Grass
import game_framework
import game_world


player= None
grass_map=None
grass=None


def init():
    global player, game_map, grass

    game_map = Map()
    player = Character()
    grass=Grass()
    game_world.add_object(game_map,0)
    game_world.add_object(grass,1)
    game_world.add_object(player,1)
    pass
def finish():
    global player,game_map,grass
    game_world.clear()
    player=None
    game_map=None
    grass=None


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
    game_world.update()

    pass


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass

def pause():
    pass
def resume():
    pass



