import pygame
from settings import CLEAR, WIDTH, HEIGHT, clock, screen, TILE_WIDTH, TILE_HEIGHT
from random import choice, randint
from tools import Tools, player_collision
# from projectiles import Bullet, active_projectiles

SPRITE_RATE = 120
ATTACK_RATE = 1500

class Enemy(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, colliders, initial_state="idle"):
        pygame.sprite.Sprite.__init__(self)

        # Start timers
        self.sprite_timer = CLEAR
        self.movement_timer = CLEAR
        self.damaged_timer = CLEAR
        self.attack_timer = ATTACK_RATE
        self.move_timer = 120
        self.ready_to_move = False
        # Initial state is defined from data on meta_data on maps
        self.current_state = initial_state
        # Starts in a random frame to prevent synchronized enemies that look unnatural
        self.current_sprite_frame = randint(0, len(self.sprites[self.current_state])-1)
        # Creates a clean surface with the current dimensions to initialize the rect
        self.image = pygame.Surface(self.sprites[self.current_state][self.current_sprite_frame].get_size())
        self.rect = self.image.get_rect()
        self.x, self.y = start_x, start_y
        self.rect.x, self.rect.y = self.x, self.y
        # Variable that keeps track if the player is within range of an instance of an enemy
        self.within_range = False
        self.x_distance = 100
        self.y_distance = 100
        # ...And to directions the player is
        self.player_latitude = "south"
        self.current_flip = choice(["west", "east"])
        self.colliders = colliders
        # Sets health points
        self.hp = self.max_hp


    def parse_sprite(self):

        if self.hp == 0:
            self.kill()
            return 0;
        else:
            self.current_sprite_frame = (self.current_sprite_frame + 1) % len(self.sprites[self.current_state])
            self.image = self.sprites[self.current_state][self.current_sprite_frame]

        if self.current_flip == "east":
            self.image = pygame.transform.flip(self.image, True, False)
        if self.damaged_timer > 0:
            self.holder = self.image.copy()
            self.holder.fill((200, 0, 0, 100), special_flags=pygame.BLEND_ADD)
            self.image = self.holder
            # TODO: clean this?
            # self.image = self.sprites["damaged"]
            # self.current_sprite_frame = 0

        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x + self.x_offset , self.y + self.y_offset
        self.sprite_timer = CLEAR

    def update(self):
        self.sprite_timer += clock.get_time()
        self.attack_timer += clock.get_time()
        if self.move_timer > 0:
            self.move_timer -= clock.get_time()
            if self.move_timer < 0:
                self.move_timer = 0

        if self.damaged_timer > 0:
            self.damaged_timer -= clock.get_time()

        if self.hp != self.max_hp:
            Tools.health_bar(screen, self.hp, self.max_hp, self.rect)

        if self.sprite_timer >= SPRITE_RATE:
            self.parse_sprite()
            self.image.set_colorkey((0, 0, 0))
    
    def do_damage(self):
        self.damaged_timer = 500
        self.hp -= 1

    def move_east(self):
        block = pygame.Rect(self.x+TILE_WIDTH, self.y, self.rect.width, self.rect.height)
        for tile in self.colliders:
            if block.colliderect(tile):
                return
        if not block.colliderect(player_collision.rect):
            self.x += TILE_WIDTH
    def move_west(self):
        block = pygame.Rect(self.x-TILE_WIDTH, self.y, self.rect.width, self.rect.height)
        for tile in self.colliders:
            if block.colliderect(tile):
                return
        if not block.colliderect(player_collision.rect):
            self.x -= TILE_WIDTH
    def move_north(self):
        block = pygame.Rect(self.x, self.y-TILE_HEIGHT, self.rect.width, self.rect.height)
        for tile in self.colliders:
            if block.colliderect(tile):
                return
        if not block.colliderect(player_collision.rect):
            self.y -= TILE_HEIGHT
    def move_south(self):
        block = pygame.Rect(self.x, self.y+TILE_HEIGHT, self.rect.width, self.rect.height)
        for tile in self.colliders:
            if block.colliderect(tile):
                return
        if not block.colliderect(player_collision.rect):
            self.y += TILE_HEIGHT
