from pico2d import *
import game_world
import game_framework

item_images=None
ITEM_W,ITEM_H=35,35

class Item:
    def __init__(self,x,y,item_type):
        global item_images

        self.x,self.y=x,y
        self.item_type=item_type
        print(f"Item created at ({self.x}, {self.y}) of type {self.item_type}")

        if item_images is None:
            item_images={
                'WEAPON1': load_image('item/무기1.png'),
                'WEAPON2': load_image('item/무기2.png'),
                'WEAPON_S': load_image('item/무기s.png')
            }
    def update(self):
        pass
    def get_bb(self):
        return self.x-ITEM_W//2, self.y-ITEM_H//2, self.x+ITEM_W//2, self.y+ITEM_H//2
    def draw(self):
        image=item_images[self.item_type]
        image.draw(self.x,self.y,ITEM_W,ITEM_H)
    def handle_collision(self,group,other):
        if group =='player:item':
            print(f"Player picked up item of type {self.item_type}")
            pass


