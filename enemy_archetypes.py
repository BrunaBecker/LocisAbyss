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
    def __init__(self, start_x, start_y):
        self.name = "demon"
        self.sprites = {
            "idle": list(pygame.image.load(path.join(demon_folder, "demon_idle", f)) for f in listdir(path.join(demon_folder, "demon_idle"))),
            "attack": list(pygame.image.load(path.join(demon_folder, "demon_attack_breath", f)) for f in listdir(path.join(demon_folder, "demon_attack_breath")))
        }


        self.max_hp = 12
        Enemy.__init__(self, start_x, start_y)


class Ghost(Enemy):
    def __init__(self, start_x, start_y):
        self.name= "ghost"
        self.sprites = {
            "spawn": list(pygame.image.load(path.join(ghost_folder, "ghost_appears", f)) for f in listdir(path.join(ghost_folder, "ghost_appears"))),
            "idle": list(pygame.image.load(path.join(ghost_folder, "ghost_idle", f)) for f in listdir(path.join(ghost_folder, "ghost_idle"))),
            "shriek": list(pygame.image.load(path.join(ghost_folder, "ghost_shriek", f)) for f in listdir(path.join(ghost_folder, "ghost_shriek"))),
            "death": list(pygame.image.load(path.join(ghost_folder, "ghost_death", f)) for f in listdir(path.join(ghost_folder, "ghost_death"))),
        }

        self.max_hp = 5
        Enemy.__init__(self, start_x, start_y)


class Hell_Beast(Enemy):
    def __init__(self, start_x, start_y):
        self.name = "hell_beast"
        self.sprites = {
            "idle": list(pygame.image.load(path.join(hell_beast_folder, "hell_beast_idle", f)) for f in listdir(path.join(hell_beast_folder, "hell_beast_idle"))),
            "burn": list(pygame.image.load(path.join(hell_beast_folder, "hell_beast_burn", f)) for f in listdir(path.join(hell_beast_folder, "hell_beast_burn"))),
        }

        self.max_hp = 8
        Enemy.__init__(self, start_x, start_y)

class Hell_Hound(Enemy):
    def __init__(self, start_x, start_y):
        self.name = "hell_hound"
        self.sprites = {
            "idle": list(pygame.image.load(path.join(hell_hound_folder, "hell_hound_idle", f)) for f in listdir(path.join(hell_hound_folder, "hell_hound_idle"))),
            "jump": list(pygame.image.load(path.join(hell_hound_folder, "hell_hound_jump", f)) for f in listdir(path.join(hell_hound_folder, "hell_hound_jump"))),
            "walk": list(pygame.image.load(path.join(hell_hound_folder, "hell_hound_walk", f)) for f in listdir(path.join(hell_hound_folder, "hell_hound_walk"))),
            "run": list(pygame.image.load(path.join(hell_hound_folder, "hell_hound_run", f)) for f in listdir(path.join(hell_hound_folder, "hell_hound_run"))),
        }

        self.max_hp = 3
        Enemy.__init__(self, start_x, start_y)

class Skull(Enemy):
    def __init__(self, start_x, start_y):
        self.name = "skull"
        sprites_before = {
            "idle": list(pygame.image.load(path.join(skull_folder, "fire-skull", f)) for f in listdir(path.join(skull_folder, "fire-skull"))),
        }
        self.sprites = {
            "idle": list(pygame.transform.smoothscale(f,(48,56)) for f in sprites_before["idle"])
        }

        self.max_hp = 3
        Enemy.__init__(self, start_x, start_y)

class Projectile:
    sprites = (pygame.image.load(f) for f in listdir(path.join(enemies_assets_folder, "projectile")))

monster_types = {"demon": Demon, "ghost": Ghost, "hell beast": Hell_Beast, "hell hound": Hell_Hound, "skull": Skull}
