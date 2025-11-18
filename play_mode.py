from pico2d import *
from character import Character
from map import Map
from grass import Grass
from monster import Monster
import game_framework
import game_world
from ui_manager import UIManager
from portal import Portal
from boss import Boss1

STAGE={
    1:{
        'type':'normal',
        'map':'res/map1.png',
        'grass':'res/grass.png',
        'portal':(950,185),
        'next_stage':2
    },
    2:{
        'type':'boss',
        'boss_class':Boss1,
        'map':'res2/bg2.png',
        'grass':'res/grass.png',
        'portal':(950,185),
        'next_stage':3
    }


}

CANVAS_WIDTH=1000
CANVAS_HEIGHT=725
RESPAWN_DELAY=5.0

player= None
game_map=None
grass_map=None
grass=None
ui_manager=None
portal=None
monsters=[]
respawn_timer=0.0
current_stage_index=1


def init():
    global player, game_map, grass,ui_manager,monsters,respawn_timer

    player = Character()
    grass=Grass()
    ui_manager=UIManager(player)
    monsters=[]

    game_world.add_object(grass,1)
    game_world.add_object(player,1)
    game_world.add_object(ui_manager,2)

    game_world.add_collision_pair('player:monster',player,None)
    game_world.add_collision_pair('player_attack:monster',None,None)

    load_stage(1)

    respawn_timer=0.0


def load_stage(stage_index):
    global game_map, portal, current_stage_index, monsters, player, ui_manager

    for o in list(game_world.world[1]):
        game_world.remove_object(o)

    monsters.clear()

    if game_map:
        game_world.remove_object(game_map)

    if portal:
        game_world.remove_object(portal)
        portal = None

    if stage_index not in STAGE:
        return
    info = STAGE[stage_index]
    current_stage_index = stage_index

    game_map = Map(info['map'])
    game_world.add_object(game_map, 0)

    grass_image = info.get('grass', 'res/grass.png')
    grass = Grass(grass_image)
    game_world.add_object(grass, 1)

    player.x = 50
    game_world.add_object(player, 1)

    if info['type'] == 'boss':
        portal = None
    elif info['portal']:
        portal = Portal(*info['portal'])
        game_world.add_object(portal, 1)
    else:
        portal = None

    if info['type'] == 'normal':
        monsters = [Monster() for _ in range(5)]
        game_world.add_objects(monsters, 1)

    elif info['type'] == 'boss':
        BossClass = info['boss_class']
        boss = BossClass()
        monsters = [boss]
        game_world.add_object(boss, 1)

    game_world.add_collision_pair('player:monster', player, None)
    game_world.add_collision_pair('player_attack:monster', None, None)

    game_world.add_collision_pair('player:item', player, None)

    for m in monsters:
        game_world.add_collision_pair('player:monster', None, m)
        game_world.add_collision_pair('player_attack:monster', None, m)

    print(f"Stage {stage_index} Loaded! Items cleaned.")


def finish():
    global player,game_map,grass,ui_manager,monsters,respawn_timer,portal
    game_world.clear()
    player=None
    game_map=None
    grass=None
    ui_manager=None
    monsters=[]
    respawn_timer=0.0

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


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
    global respawn_timer,portal
    game_world.update()
    game_world.handle_collisions()
    current_info=STAGE[current_stage_index]

    if current_info['type']=='boss':
        if portal is None:
            if monsters and monsters[0].hp <=0:
                print('boss defeated, portal open')
                if current_info['portal']:
                    portal=Portal(*current_info['portal'])
                    game_world.add_object(portal,1)

    if portal and collide(player, portal) and player.w_down:
        next_idx = current_info['next_stage']
        if next_idx:
            load_stage(next_idx)
            return

    if current_info['type']=='normal':
        monster_count=0
        for o in game_world.world[1]:
            if type(o)== Monster:
                monster_count+=1

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



