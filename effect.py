from pico2d import *
import game_world
import game_framework

EFFECT_DURATION=0.2
EFFECT_W, EFFECT_H = 100, 100

class SwordEffect:
    image=None
    def __init__(self,x,y,face_dir=1,effect_type='normal'):
        if SwordEffect.image is None:
            SwordEffect.image={
                'bare_hand':load_image('effect/01.png'),
                'normal':load_image('effect/03.png'),
                'special_s':load_image('effect/04.png')
            }

        self.x, self.y = x, y
        self.face_dir = face_dir
        self.life_time = EFFECT_DURATION
        self.effect_type = effect_type
        pass
    def update(self):
        self.life_time -= game_framework.frame_time

        if self.life_time <= 0:
            game_world.remove_object(self)
        pass
    def draw(self):
        image_to_draw = self.image[self.effect_type]

        if self.face_dir == 1:
            image_to_draw.draw(self.x, self.y, EFFECT_W, EFFECT_H)
        else:
            image_to_draw.composite_draw(0, 'h', self.x, self.y, EFFECT_W, EFFECT_H)
        pass