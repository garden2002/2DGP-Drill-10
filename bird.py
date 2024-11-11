# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
from ball import Ball
import game_world
import game_framework


PIXEL_PER_METER = (10.0 /0.7)
RUN_SPEED_KMPH = 390.0
RUN_SPEED_MPH = (RUN_SPEED_KMPH * 1000.0 /60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPH / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4


class Run:
    @staticmethod
    def enter(bird, e):
        if start_event(e):
            bird.face_dir = 1
        bird.frame = random.randint(0,3)
        bird.dir = 1
        bird.action = 2
        pass


    @staticmethod
    def exit(bird, e):
        pass


    @staticmethod
    def do(bird):
        if  bird.action == 0:
            bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if bird.frame > 4:
                bird.action = 1
                bird.frame = 0
        elif bird.action == 1:
            bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if bird.frame > 4:
                bird.action = 2
                bird.frame = 0
        elif bird.action == 2:
            bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
            if bird.frame > 3:
                bird.action = 0
                bird.frame = 0
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        if bird.face_dir == 1:
            if bird.x > 1600:
                bird.face_dir = -1
                bird.dir = -1
        elif bird.face_dir == -1:
            if bird.x < 0:
                bird.face_dir = 1
                bird.dir = 1



    @staticmethod
    def draw(bird):
        if bird.face_dir == 1:
            bird.image.clip_draw(int(bird.frame) * 183, bird.action * 169, 183, 169, bird.x, bird.y)
        elif bird.face_dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 169, 183, 169,
                                          0, 'h', bird.x, bird.y, 183, 169)




class Bird:

    def __init__(self):
        self.x, self.y = random.randint(100 , 500), 300
        self.face_dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Run)
        self.state_machine.set_transitions(
            {
                Run: {}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # 여기서 받을 수 있는 것만 걸러야 함. right left  등등..
        self.state_machine.add_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()


