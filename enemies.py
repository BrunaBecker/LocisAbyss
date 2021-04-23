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
        self.damaged_timer = CLEAR
        self.current_state = initial_state
        #self.sprite_width, self.sprite_height = self.sprites[current_state][0].get_size()
        self.current_sprite_frame = CLEAR
        self.image = pygame.Surface(self.sprites[self.current_state][self.current_sprite_frame].get_size())
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.x, self.y = start_x, start_y
        self.rect.x, self.rect.y = self.x, self.y
        self.within_range = False

        self.hp = self.max_hp

        self.current_flip = choice(["right", "left"])
        self.blink = 0

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

        if self.current_flip == "right":
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.sprite_timer = CLEAR


    def update(self):
        self.sprite_timer += clock.get_time()
        if self.damaged_timer > 0:
            self.damaged_timer -= clock.get_time()


        if self.hp != self.max_hp:
            Tools.health_bar(screen, self.hp, self.max_hp, self.rect.x, self.rect.y, self.rect.width, self.rect.height)

        if self.sprite_timer >= SPRITE_RATE:
            self.parse_sprite()

        if self.damaged_timer > 0 and self.blink == 4:
            self.image.fill((0,0,0))
            self.blink = 0
        elif self.damaged_timer > 0 and self.blink < 4:
            self.parse_sprite()
            self.blink += 1
        self.image.set_colorkey((0, 0, 0))

        if self.within_range and self.current_state == "hidden":
            self.current_state = "spawn"
            

    def do_damage(self):
        self.blink = 0
        self.damaged_timer = 500
        self.hp -= 1
