from pico2d import *
import game_world

CANVAS_WIDTH=1280
CANVAS_HEIGHT=725

BAG_ICON_X = 60
BAG_ICON_Y = 60
BAG_ICON_W, BAG_ICON_H=70,70
BAG_SCALE_NORMAL=1.0
BAG_SCALE_HOVER=1.1

INV_X=CANVAS_WIDTH//2
INV_Y=CANVAS_HEIGHT//2
INV_W, INV_H=250,250
SLOT_SIZE=INV_W/5

class UIManager:
    def __init__(self):
        self.bag_icon_image=load_image('가방.png')
        self.inventory_image=load_image('inventory.png')

        self.bag_icon_scale=BAG_SCALE_NORMAL
        self.is_inventory_open=False

        self.bag_icon_rect=self.calculate_rect(BAG_ICON_X,BAG_ICON_Y,BAG_ICON_W,BAG_ICON_H)
        self.inv_panel_rect=self.calculate_rect(INV_X,INV_Y,INV_W,INV_H)
        inv_left,_,_,inv_top=self.inv_panel_rect

        close_btn_left=inv_left+(SLOT_SIZE *4)
        close_btn_top=inv_top

        self.close_button_rect=(close_btn_left,close_btn_top-SLOT_SIZE,close_btn_left + SLOT_SIZE,close_btn_top)


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

    def handle_event(self,event):
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
           if event.button ==SDL_BUTTON_LEFT and self.is_mouse_in_rect(mx,my,self.close_button_rect):
               self.is_inventory_open=False
               return True
           if self.is_mouse_in_rect(mx,my,self.inv_panel_rect):
               return True
       return False


    def update(self):
        pass
    def draw(self):
        current_w=BAG_ICON_W * self.bag_icon_scale
        current_h=BAG_ICON_H * self.bag_icon_scale
        self.bag_icon_image.draw(BAG_ICON_X,BAG_ICON_Y,current_w,current_h)

        if self.is_inventory_open:
            self.inventory_image.draw(INV_X,INV_Y,INV_W,INV_H)
        pass
