from pico2d import *
from character import Character
from map import Map
running=True
world = []
player= None


def reset_world():
    global world,player
    world = []
    game_map = Map()
    world.append(game_map)
    player = Character()
    world.append(player)
    pass


def handle_events():
    global running,player

    for event in get_events():
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)
    pass


def update_world():
    for o in world:
        o.update()

    pass


def render_world():
    pass


def main():
    global running
    open_canvas(1280,720)
    reset_world()

    while running:
        handle_events()
        update_world()
        render_world()
        delay(0.01)

        
    close_canvas()

if __name__ == '__main__':
    main()
