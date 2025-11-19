from pico2d import *
import game_world
from pico2d import get_time
from sdl2 import SDLK_e, SDL_KEYDOWN

CANVAS_WIDTH=1000
CANVAS_HEIGHT=725

BAG_ICON_X = 620
BAG_ICON_Y = 40
BAG_ICON_W, BAG_ICON_H=70,70
BAG_SCALE_NORMAL=1.0
BAG_SCALE_HOVER=1.1

INV_X=CANVAS_WIDTH//2
INV_Y=CANVAS_HEIGHT//2
INV_W, INV_H=250,250
SLOT_SIZE=INV_W/5
ITEM_DRAW_W, ITEM_DRAW_H = 32, 32

class UIManager:
    def __init__(self,player):
        self.player=player
        self.bag_icon_image=load_image('res/bag.png')
        self.inventory_image=load_image('res/inventory.png')

        self.image_hp_text = load_image('res2/hp_1.png')
        self.image_hp_bar = load_image('res2/hp_2.png')
        self.image_hp_bg=load_image('res2/hp_3.png')
        self.hp_base_x = 50
        self.hp_base_y = 40

        self.item_images = {
            'WEAPON1': load_image('item/무기1.png'),
            'WEAPON2': load_image('item/무기2.png'),
            'WEAPON_S': load_image('item/무기s.png'),
            'POTION1': load_image('item/potion1.png'),
        }

        self.bag_icon_scale=BAG_SCALE_NORMAL
        self.is_inventory_open=False

        self.bag_icon_rect=self.calculate_rect(BAG_ICON_X,BAG_ICON_Y,BAG_ICON_W,BAG_ICON_H)
        self.inv_panel_rect=self.calculate_rect(INV_X,INV_Y,INV_W,INV_H)

        self.last_click_time=0.0
        self.last_clicked_slot=-1
        self.DOUBLE_CLICK_TIME=0.25


        pass
    def calculate_rect(self,cx,cy,w,h):
        return(
            cx-w//2,
            cy-h//2,
            cx+w//2,
            cy+h//2
        )
    def is_mouse_in_rect(self,mx,my,rect):
        left,bottom,right,top=rect
        return left<mx<right and bottom<my<top

    def get_slot_index_from_mouse(self,mx,my):
        if not self.is_mouse_in_rect(mx,my,self.inv_panel_rect):
            return -1
        inv_left,_,_,inv_top=self.inv_panel_rect
        local_x=mx-inv_left
        local_y=inv_top - my

        col=int(local_x // SLOT_SIZE)
        row=int(local_y // SLOT_SIZE)

        if 0<= col <5 and 0<= row <5:
            slot_index=row *5 + col
            return slot_index

        return -1

    def handle_event(self,event):
       if event.type == SDL_KEYDOWN and event.key == SDLK_e:
            if self.is_inventory_open:
                self.is_inventory_open=False
                return True

       if event.type in (SDL_MOUSEMOTION, SDL_MOUSEBUTTONDOWN,SDL_MOUSEBUTTONUP):
           mx,my=event.x,CANVAS_HEIGHT-event.y
       else:
           return False

       if event.type==SDL_MOUSEMOTION:
           if self.is_mouse_in_rect(mx,my,self.bag_icon_rect):
               self.bag_icon_scale=BAG_SCALE_HOVER
           else:
               self.bag_icon_scale=BAG_SCALE_NORMAL
       elif event.type==SDL_MOUSEBUTTONDOWN:
           if self.is_mouse_in_rect(mx,my,self.bag_icon_rect):
               if event.button==SDL_BUTTON_LEFT:
                   self.is_inventory_open=not self.is_inventory_open
               return True

       if self.is_inventory_open:
           if event.type==SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT and self.is_mouse_in_rect(mx,my,self.inv_panel_rect):

               slot_index=self.get_slot_index_from_mouse(mx,my)
               if slot_index != -1:
                   current_time=get_time()
                   is_double_click=(current_time - self.last_click_time < self.DOUBLE_CLICK_TIME) and (self.last_clicked_slot == slot_index)

                   if is_double_click:
                       is_item_click=(0 <= slot_index<len(self.player.inventory))
                       if is_item_click:
                           self.player.equip_item(slot_index)
                       else:
                           self.player.unequip_item()
                   else:
                       self.last_click_time=current_time
                       self.last_clicked_slot=slot_index
               return True

           if self.is_mouse_in_rect(mx, my, self.inv_panel_rect):
               return True

           return False

    def update(self):
        pass
    def draw(self):
        self.draw_hp_bar()
        current_w=BAG_ICON_W * self.bag_icon_scale
        current_h=BAG_ICON_H * self.bag_icon_scale
        self.bag_icon_image.draw(BAG_ICON_X,BAG_ICON_Y,current_w,current_h)

        if self.is_inventory_open:
            self.inventory_image.draw(INV_X,INV_Y,INV_W,INV_H)
            self.draw_inventory_items()

    def draw_hp_bar(self):
        self.image_hp_text.draw(self.hp_base_x, self.hp_base_y, 40, 20)
        bar_max_width = 500#바 전체 길이
        bar_height = 20
        bar_start_x = self.hp_base_x + 30
        bg_center_x = bar_start_x + (bar_max_width // 2)
        self.image_hp_bg.draw(bg_center_x, self.hp_base_y, bar_max_width, bar_height)

        if self.player:
            safe_hp = max(0, self.player.hp)
            hp_ratio = safe_hp / self.player.max_hp
            current_bar_width = int(bar_max_width * hp_ratio)


            bar_start_x = self.hp_base_x + 30
            bar_center_x = bar_start_x + (current_bar_width // 2)

            if current_bar_width > 0:
                self.image_hp_bar.draw(bar_center_x, self.hp_base_y, current_bar_width, bar_height)



    def draw_inventory_items(self):

        inv_left, _, _, inv_top = self.inv_panel_rect

        slot_start_x = inv_left + SLOT_SIZE / 2
        slot_start_y = inv_top - SLOT_SIZE / 2

        for i, item_type in enumerate(self.player.inventory):
            slot_index = i

            row = slot_index // 5
            col = slot_index % 5

            if slot_index >= 25:
                break

            draw_x = slot_start_x + (col * SLOT_SIZE)
            draw_y = slot_start_y - (row * SLOT_SIZE)

            image = self.item_images.get(item_type)
            if image:
                image.draw(draw_x, draw_y, ITEM_DRAW_W, ITEM_DRAW_H)

