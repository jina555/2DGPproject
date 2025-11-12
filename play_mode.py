from pico2d import *
from character import Character
from map import Map
from grass import Grass
from monster import Monster
import game_framework
import game_world
from ui_manager import UIManager

CANVAS_WIDTH=1280
CANVAS_HEIGHT=725
RESPAWN_DELAY=7.0

player= None
grass_map=None
grass=None
ui_manager=None
monsters=[]
respawn_timer=0.0


def init():
    global player, game_map, grass,ui_manager,monsters,respawn_timer

    game_map = Map()
    player = Character()
    grass=Grass()
    ui_manager=UIManager(player)
    monsters=[Monster() for _ in range(5)]

    game_world.add_object(game_map,0)
    game_world.add_object(grass,1)
    game_world.add_object(player,1)
    game_world.add_objects(monsters,1)
    game_world.add_object(ui_manager,2)

    game_world.add_collision_pair('player:monster',player,None)
    game_world.add_collision_pair('player_attack:monster',None,None)

    # game_world.add_collision_pair('player:item',player,None)



    for m in monsters:
        game_world.add_collision_pair('player:monster',None,m)
        game_world.add_collision_pair('player_attack:monster',None,m)

    respawn_timer=0.0


    pass
def finish():
    global player,game_map,grass,ui_manager,monsters,respawn_timer
    game_world.clear()
    player=None
    game_map=None
    grass=None
    ui_manager=None
    monsters=[]
    respawn_timer=0.0


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
    global respawn_timer
    game_world.update()
    game_world.handle_collisions()

    monster_count = 0

    for o in game_world.world[1]:
        if isinstance(o, Monster):
            monster_count += 1

    if monster_count < 5:
        respawn_timer -= game_framework.frame_time  # 딜레이 타이머 감소

        # 타이머가 0 이하가 되면 몬스터 생성
        if respawn_timer <= 0:
            print("Respawning monster...")
            new_monster = Monster()
            game_world.add_object(new_monster, 1)

            game_world.add_collision_pair('player:monster', player, new_monster)
            game_world.add_collision_pair('player_attack:monster', None, new_monster)

            respawn_timer = RESPAWN_DELAY
    else:
        respawn_timer = 0.0

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



