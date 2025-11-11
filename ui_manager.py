from pico2d import *
import game_world

CANVAS_WIDTH=1280
CANVAS_HEIGHT=725

BAG_ICON_X = 1000
BAG_ICON_Y = 70
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

        self.item_images = {
            'WEAPON1': load_image('item/무기1.png'),
            'WEAPON2': load_image('item/무기2.png'),
            'WEAPON_S': load_image('item/무기s.png')
        }

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
            self.draw_inventory_items()

    def draw_inventory_items(self):
        # 인벤토리 패널의 좌측 상단 좌표를 기준으로 계산
        inv_left, _, _, inv_top = self.inv_panel_rect

        # 첫 번째 슬롯(0,0)의 중심 좌표 계산
        slot_start_x = inv_left + SLOT_SIZE / 2
        slot_start_y = inv_top - SLOT_SIZE / 2

        # self.player.inventory 리스트를 순회
        for i, item_type in enumerate(self.player.inventory):

            # i (인벤토리 리스트 인덱스)를
            # slot_index (화면에 그릴 슬롯 위치)로 변환

            slot_index = i
            if i >= 4:  # 4번째 아이템(i=4)부터는 (X칸 때문에) 1칸씩 밀려서 그려짐
                slot_index = i + 1

                # slot_index를 (row, col)로 변환
            row = slot_index // 5
            col = slot_index % 5

            # 총 25칸을 넘어가면 그리지 않음 (i가 23, slot_index가 24일 때가 마지막)
            if slot_index >= 25:
                break

                # 해당 슬롯의 중심 x, y 좌표 계산
            draw_x = slot_start_x + (col * SLOT_SIZE)
            draw_y = slot_start_y - (row * SLOT_SIZE)

            # 아이템 이미지가 있는지 확인하고 그리기
            image = self.item_images.get(item_type)
            if image:
                image.draw(draw_x, draw_y, ITEM_DRAW_W, ITEM_DRAW_H)

