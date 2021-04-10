import pygame
from pygame.locals import *
from pygame.time import *
from pytmx.util_pygame import load_pygame
import json
from os import path
import sys

WIDTH, HEIGHT = 1280, 1024  # Map Size used to define Window
SPRITE_RATE = 60  # Sets the interval between sprites updates
MOVEMENT_RATE = 240  # Sets the interval between player movement
CLEAR = 0  # Used to clear clocks

### Relative Paths Shortcuts ###
loci_dir = path.dirname(__file__)
assets_folder = path.join(loci_dir, "Sprites")
player_assets_folder = path.join(assets_folder, "Knight")
pygame.display.set_caption("Loci's Tower")
# window_icon = pygame.image.load('logo.png')
# pygame.display.set_icon(window_icon)

### Initial Declarations ###
pygame.init()
clock = Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

### Load Maps ###
# Level One
level_one = load_pygame(path.join(loci_dir, "maps\\first_map.tmx"))
TILEWIDTH, TILEHEIGHT = level_one.tilewidth, level_one.tileheight
level_one_coords = {
    "start": (1 * TILEWIDTH, 22 * TILEHEIGHT),
    "end": [(25 * TILEWIDTH, 3 * TILEHEIGHT), (26 * TILEWIDTH, 3 * TILEHEIGHT)],
}


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.list_of_states = {
            "idle": {
                "sprite_sheet": pygame.image.load(path.join(player_assets_folder, "KnightIdle_strip.png")).convert(),
                "meta_data": None,
                "path_data": path.join(player_assets_folder, "KnightIdle_strip.json"),
            },
            "run": {
                # TODO: holder
                "sprite_sheet": pygame.image.load(path.join(player_assets_folder, "KnightIdle_strip.png")).convert(),
                "meta_data": None,
                "path_data": path.join(player_assets_folder, "KnightIdle_strip.json"),
            },
            "attack": {
                "sprite_sheet": pygame.image.load(path.join(player_assets_folder, "KnightAttack_strip.png")).convert(),
                "meta_data": None,
                "path_data": path.join(player_assets_folder, "KnightAttack_strip.json"),
            },
            "death": {
                # TODO: holder
                "sprite_sheet": pygame.image.load(path.join(player_assets_folder, "KnightIdle_strip.png")).convert(),
                "meta_data": None,
                "path_data": path.join(player_assets_folder, "KnightIdle_strip.json"),
            },
        }
        self.current_state = self.list_of_states["idle"]
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.x, self.y = level_one_coords["start"]
        self.rect.x, self.rect.y = self.x, self.y
        self.sprite_timer = SPRITE_RATE
        self.movement_timer = CLEAR
        self.attack_timer = CLEAR
        self.current_frame = CLEAR
        self.attack_frame = CLEAR
        self.current_flip = "right"

        for state in self.list_of_states:
            with open(self.list_of_states[state]["path_data"]) as f:
                self.list_of_states[state]["meta_data"] = json.load(f)
            f.close()

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((113, 102, 79))
        sprite.blit(self.current_state["sprite_sheet"], (0, 0), (x, y, w, h))
        return sprite

    def parse_sprite(self):
        name = self.current_state["meta_data"]["list_of_frames"][self.current_frame]
        sprite = self.current_state["meta_data"]["frames"][name]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        self.image = self.get_sprite(x, y, w, h)
        self.rect = self.image.get_rect()
        if self.current_flip == "left":
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x, self.rect.y = (
                self.x - self.current_state["meta_data"]["frames"][name]["flip_offset"][0] + 4,
                self.y - self.current_state["meta_data"]["frames"][name]["flip_offset"][1],
            )
        else:
            self.rect.x, self.rect.y = (
                self.x - self.current_state["meta_data"]["frames"][name]["offset"][0] + 4,
                self.y - self.current_state["meta_data"]["frames"][name]["offset"][1],
            )

        self.current_frame = (self.current_frame + 1) % self.current_state["meta_data"]["frame_quantity"]

        if self.current_state == self.list_of_states["attack"] and self.current_frame == 7:
            self.current_state = self.list_of_states["idle"]
            self.current_frame = CLEAR
            self.attack_frame = 7
        elif self.current_state == self.list_of_states["attack"] and self.current_frame == 12:
            self.current_state = self.list_of_states["idle"]
            self.current_frame = CLEAR
            self.attack_frame = 12
        elif self.current_state == self.list_of_states["attack"] and self.current_frame == (
            self.current_state["meta_data"]["frame_quantity"] - 1
        ):
            self.current_frame = CLEAR
            self.current_state = self.list_of_states["idle"]
            self.attack_frame = CLEAR

    def update(self):
        self.sprite_timer += clock.get_time()
        self.movement_timer += clock.get_time()
        self.attack_timer += clock.get_time()
        if self.sprite_timer >= SPRITE_RATE:
            self.parse_sprite()
            self.sprite_timer = CLEAR

        self.collision_wings = {
            "north": Collision_Block(self.x, self.y - TILEHEIGHT, TILEWIDTH, TILEHEIGHT),
            "south": Collision_Block(self.x, self.y + TILEHEIGHT, TILEWIDTH, TILEHEIGHT),
            "east": Collision_Block(self.x + TILEWIDTH, self.y, TILEWIDTH, TILEHEIGHT),
            "west": Collision_Block(self.x - TILEWIDTH, self.y, TILEWIDTH, TILEHEIGHT),
        }

        keystate = pygame.key.get_pressed()
        if self.movement_timer >= MOVEMENT_RATE:
            if (
                (keystate[pygame.K_d] or keystate[pygame.K_RIGHT])
                and self.x + TILEWIDTH < WIDTH
                and pygame.sprite.spritecollideany(self.collision_wings["east"], collision_group)
            ) == None:
                if self.current_flip == "left":
                    self.current_flip = "right"
                self.x += TILEWIDTH
                self.movement_timer = CLEAR
            if (
                (keystate[pygame.K_a] or keystate[pygame.K_LEFT])
                and self.x > 0
                and pygame.sprite.spritecollideany(self.collision_wings["west"], collision_group) == None
            ):
                if self.current_flip == "right":
                    self.current_flip = "left"
                self.x -= TILEWIDTH
                self.movement_timer = CLEAR
            if (
                (keystate[pygame.K_s] or keystate[pygame.K_DOWN])
                and self.y + TILEHEIGHT < HEIGHT
                and pygame.sprite.spritecollideany(self.collision_wings["south"], collision_group) == None
            ):
                self.y += TILEHEIGHT
                self.movement_timer = CLEAR
            if (
                (keystate[pygame.K_w] or keystate[pygame.K_UP])
                and self.y > 0
                and pygame.sprite.spritecollideany(self.collision_wings["north"], collision_group) == None
            ):
                self.y -= TILEHEIGHT
                self.movement_timer = CLEAR

        if (keystate[pygame.K_e] or keystate[pygame.K_SPACE]) and self.attack_timer >= 600:
            self.current_state = self.list_of_states["attack"]
            self.current_frame = self.attack_frame
            self.attack_timer = CLEAR


class Collision_Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)


def blit_all_tiles(screen, level):
    for i in level.visible_tile_layers:
        for x, y, image in level.layers[i].tiles():
            screen.blit(image, (x * TILEWIDTH, y * TILEHEIGHT))


def get_collision_group(screen, level, collision_group):
    # Get a new one only on start/change of maps!
    for group in level.objectgroups:
        for obj in group:
            collision_group.add(Collision_Block(obj.x, obj.y, obj.width, obj.height))


all_sprites = pygame.sprite.Group()
collision_group = pygame.sprite.Group()
player = Player()
player.parse_sprite()
all_sprites.add(player)
get_collision_group(screen, level_one, collision_group)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    collision_group.update()
    screen.fill((0, 0, 0))

    blit_all_tiles(screen, level_one)
    all_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(30)
