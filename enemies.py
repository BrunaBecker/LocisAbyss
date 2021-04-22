import pygame
from settings import CLEAR, WIDTH, HEIGHT, clock, screen
from random import choice
from tools import Tools

SPRITE_RATE = 100
class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, initial_state="idle"):
        pygame.sprite.Sprite.__init__(self)


        self.sprite_timer = CLEAR
        self.movement_timer = CLEAR
        self.current_state = initial_state
        #self.sprite_width, self.sprite_height = self.sprites[current_state][0].get_size()
        self.curret_sprite_frame = CLEAR
        self.image = pygame.Surface(self.sprites[self.current_state][self.curret_sprite_frame].get_size())
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = start_x
        self.rect.y = start_y

        self.hp = self.max_hp

        self.current_flip = choice(["right", "left"])


    def parse_sprite(self):
        # if sprite changed set this to 0
        self.curret_sprite_frame = (self.curret_sprite_frame + 1) % len(self.sprites[self.current_state])
        frame = self.sprites[self.current_state][self.curret_sprite_frame]
        w, h = self.sprites[self.current_state][self.curret_sprite_frame].get_size()
        sprite = pygame.Surface((w, h))
        sprite.blit(frame, (0,0))
        sprite.set_colorkey((0, 0, 0))
        if self.current_flip == "right":
            self.image = pygame.transform.flip(sprite, True, False)
        else:
            self.image = sprite
        self.mask = pygame.mask.from_surface(self.image)
        self.sprite_timer = CLEAR

    def update(self):
        self.sprite_timer += clock.get_time()

        if self.sprite_timer >= SPRITE_RATE:
            self.parse_sprite()

        if self.hp != self.max_hp:
            Tools.health_bar(screen, self.hp, self.max_hp, self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def do_damage(self):
        self.hp -= 1
        if self.hp == 0:
            self.kill()
