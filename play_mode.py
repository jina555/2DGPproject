from pico2d import *
from character import Character
from map import Map
from grass import Grass
import game_framework
import game_world
from ui_manager import UIManager

CANVAS_WIDTH=1280
CANVAS_HEIGHT=725



player= None
grass_map=None
grass=None
ui_manager=None


def init():
    global player, game_map, grass,ui_manager

    game_map = Map()
    player = Character()
    grass=Grass()
    ui_manager=UIManager()

    game_world.add_object(game_map,0)
    game_world.add_object(grass,1)
    game_world.add_object(player,1)
    game_world.add_object(ui_manager,2)

    pass
def finish():
    global player,game_map,grass,ui_manager
    game_world.clear()
    player=None
    game_map=None
    grass=None
    ui_manager=None


def handle_events():
    global player

    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        if ui_manager.handle_event(event):
            continue
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



