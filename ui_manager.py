from pico2d import *
import game_world

CANVAS_WIDTH=1280
CANVAS_HEIGHT=725

BAG_ICON_X = 60
BAG_ICON_Y = 60
BAG_ICON_W, BAG_ICON_H=70,70
BAG_SCALE_NORMAL=1.0
BAG_SCALE_HOVER=1.1

class UIManager:
    def __init__(self):
        self.bag_icon_image=load_image('가방.png')
        self.inventory_image=load_image('inventory.png')

        self.bag_icon_scale=BAG_SCALE_NORMAL

        pass
    def calculate_rect(self):
        pass
    def update(self):
        pass
    def draw(self):
        current_w=BAG_ICON_W * self.bag_icon_scale
        current_h=BAG_ICON_H * self.bag_icon_scale
        self.bag_icon_image.draw(BAG_ICON_X,BAG_ICON_Y,current_w,current_h)
        pass
