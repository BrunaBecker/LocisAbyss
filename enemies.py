import pygame
from settings import CLEAR, WIDTH, HEIGHT, clock, screen
from random import choice
from tools import Tools
from math import sin, pi
from projectiles import Bullet, active_projectiles

SPRITE_RATE = 100
ATTACK_RATE = 1500
class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, initial_state="idle"):
        pygame.sprite.Sprite.__init__(self)


        self.sprite_timer = CLEAR
        self.movement_timer = CLEAR
        self.damaged_timer = CLEAR
        self.attack_timer = ATTACK_RATE
        self.current_state = initial_state
        #self.sprite_width, self.sprite_height = self.sprites[current_state][0].get_size()
        self.current_sprite_frame = CLEAR
        self.image = pygame.Surface(self.sprites[self.current_state][self.current_sprite_frame].get_size())
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = start_x, start_y
        self.rect.x, self.rect.y = self.x, self.y
        self.within_range = False
        self.player_latitude = "south"

        self.hp = self.max_hp

        self.current_flip = choice(["west", "east"])

    def parse_sprite(self):

        if self.damaged_timer > 0:
            self.image = self.sprites["damaged"]
            self.current_sprite_frame = 0
        elif self.hp == 0:
            self.kill()
            return 0;
        else:
            self.current_sprite_frame = (self.current_sprite_frame + 1) % len(self.sprites[self.current_state])
            self.image = self.sprites[self.current_state][self.current_sprite_frame]

        if self.current_flip == "east":
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.sprite_timer = CLEAR

    def attack(self):
        active_projectiles.add(Bullet(self.rect.x, self.rect.y, self.player_latitude, self.current_flip))
        self.attack_timer = CLEAR

    def update(self):
        self.sprite_timer += clock.get_time()
        self.attack_timer += clock.get_time()

        if self.damaged_timer > 0:
            self.damaged_timer -= clock.get_time()

        if self.hp != self.max_hp:
            Tools.health_bar(screen, self.hp, self.max_hp, self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        if self.sprite_timer >= SPRITE_RATE:
            self.parse_sprite()
            self.image.set_colorkey((0, 0, 0))

        if self.attack_timer >= ATTACK_RATE and self.within_range:
            self.attack()


            

    def do_damage(self):
        self.damaged_timer = 500
        self.hp -= 1
