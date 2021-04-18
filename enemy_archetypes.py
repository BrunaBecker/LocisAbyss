import pygame
from settings import path, enemies_assets_folder
from os import listdir
from enemies import Enemy

demon_folder = path.join(enemies_assets_folder, "demon_boss")
ghost_folder = path.join(enemies_assets_folder, "ghost")
hell_beast_folder = path.join(enemies_assets_folder, "hell_beast")
hell_hound_folder = path.join(enemies_assets_folder, "hell_hound")
nightmare_folder = path.join(enemies_assets_folder, "nightmare")
skull_folder = path.join(enemies_assets_folder, "skull")


class Demon(Enemy):
    name = "demon"
    sprites = {
        "idle": (pygame.image.load(f) for f in listdir(path.join(demon_folder, "demon_idle"))),
        "attack": (pygame.image.load(f) for f in listdir(path.join(demon_folder, "demon_attack_breath")))
    }
    max_hp = 12
    hp = 12


class Ghost(Enemy):

    name= "ghost"
    sprites = {
        "spawn": (pygame.image.load(f) for f in listdir(path.join(ghost_folder, "ghost_appears"))),
        "idle": (pygame.image.load(f) for f in listdir(path.join(ghost_folder, "ghost_idle"))),
        "shriek": (pygame.image.load(f) for f in listdir(path.join(ghost_folder, "ghost_shriek"))),
        "death": (pygame.image.load(f) for f in listdir(path.join(ghost_folder, "ghost_death"))),
    }
    hp = 8

class Hell_Beast(Enemy):

    name = "hell_beast"
    sprites = {
        "idle": (pygame.image.load(f) for f in listdir(path.join(hell_beast_folder, "hell_beast_idle"))),
        "burn": (pygame.image.load(f) for f in listdir(path.join(hell_beast_folder, "hell_beast_burn"))),
    }
    
    hp = 5

class Hell_Hound(Enemy):

    name = "hell_hound"
    sprites = {
        "idle": (pygame.image.load(f) for f in listdir(path.join(hell_hound_folder, "hell_hound_idle"))),
        "jump": (pygame.image.load(f) for f in listdir(path.join(hell_hound_folder, "hell_hound_jump"))),
        "walk": (pygame.image.load(f) for f in listdir(path.join(hell_hound_folder, "hell_hound_walk"))),
        "run": (pygame.image.load(f) for f in listdir(path.join(hell_hound_folder, "hell_hound_run"))),
    }
    hp = 5

class Skull(Enemy):

    name = "skull"
    sprites = {
        "idle": (pygame.image.load(f) for f in listdir(path.join(skull_folder, "fire-skull"))),
    }
    hp = 3

class Projectile:
    sprites = (pygame.image.load(f) for f in listdir(path.join(enemies_assets_folder, "projectile")))

monster_types = {"demon": Demon, "ghost": Ghost, "hell beast": Hell_Beast, "hell hound": Hell_Hound, "skull": Skull}
