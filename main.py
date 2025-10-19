from pico2d import *
from character import Character
from map import Map
running=True
world = []
player= None


def reset_world():
    pass


def handle_events():
    pass


def update_world():
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
