import pygame
from settings import path, enemies_assets_folder
from enemies import Enemy, Tools, SPRITE_RATE, clock
from os import listdir

demon_folder = path.join(enemies_assets_folder, "demon_boss")
ghost_folder = path.join(enemies_assets_folder, "ghost")
hell_beast_folder = path.join(enemies_assets_folder, "hell_beast")
hell_hound_folder = path.join(enemies_assets_folder, "hell_hound")
nightmare_folder = path.join(enemies_assets_folder, "nightmare")
skull_folder = path.join(enemies_assets_folder, "skull")
class Demon(Enemy):
    def __init__(self, start_x, start_y, initial_state="idle"):
        self.name = "demon"
        self.sprites = {
            "idle": list(pygame.image.load(path.join(demon_folder, "demon_idle", f)) for f in listdir(path.join(demon_folder, "demon_idle"))),
            "attack": list(pygame.image.load(path.join(demon_folder, "demon_attack_breath", f)) for f in listdir(path.join(demon_folder, "demon_attack_breath"))),
            "damaged": pygame.image.load(path.join(demon_folder, "demon_damaged.png")),
        }


        self.max_hp = 12
        Enemy.__init__(self, start_x, start_y, initial_state)


class Ghost(Enemy):
    def __init__(self, start_x, start_y, initial_state="idle"):
        self.name= "ghost"
        self.sprites = {
            "spawn": list(pygame.image.load(path.join(ghost_folder, "ghost_appears", f)) for f in listdir(path.join(ghost_folder, "ghost_appears"))),
            "idle": list(pygame.image.load(path.join(ghost_folder, "ghost_idle", f)) for f in listdir(path.join(ghost_folder, "ghost_idle"))),
            "shriek": list(pygame.image.load(path.join(ghost_folder, "ghost_shriek", f)) for f in listdir(path.join(ghost_folder, "ghost_shriek"))),
            "death": list(pygame.image.load(path.join(ghost_folder, "ghost_death", f)) for f in listdir(path.join(ghost_folder, "ghost_death"))),
            "damaged": pygame.image.load(path.join(ghost_folder, "ghost_damaged.png")),
            "hidden": [pygame.Surface((32,32))]
        }
        self.max_hp = 5
        self.sprite_counters = {}
        Enemy.__init__(self, start_x, start_y, initial_state)

    def update(self):
        if self.within_range and self.current_state == "hidden":
            self.current_state = "spawn"
            self.current_sprite_frame = 0
            self.sprite_counters["spawn_counter"] = len(self.sprites["spawn"])

        if self.sprite_timer + clock.get_time() >= SPRITE_RATE:
            self.decrease_counters()

        Enemy.update(self)
    
    def decrease_counters(self):
        for counter in self.sprite_counters:
            self.sprite_counters[counter] -= 1

        if self.sprite_counters.get("spawn_counter") == 0:
            self.current_state = "idle"
            del self.sprite_counters["spawn_counter"]


class Hell_Beast(Enemy):
    def __init__(self, start_x, start_y, initial_state="idle"):
        self.name = "hell_beast"
        self.sprites = {
            "idle": list(pygame.image.load(path.join(hell_beast_folder, "hell_beast_idle", f)) for f in listdir(path.join(hell_beast_folder, "hell_beast_idle"))),
            "burn": list(pygame.image.load(path.join(hell_beast_folder, "hell_beast_burn", f)) for f in listdir(path.join(hell_beast_folder, "hell_beast_burn"))),
            "damaged": pygame.image.load(path.join(hell_beast_folder, "hell-beast-damaged.png")),
        }

        self.max_hp = 8
        Enemy.__init__(self, start_x, start_y, initial_state)

class Hell_Hound(Enemy):
    def __init__(self, start_x, start_y, initial_state="idle"):
        self.name = "hell_hound"
        self.sprites = {
            "idle": list(pygame.image.load(path.join(hell_hound_folder, "hell_hound_idle", f)) for f in listdir(path.join(hell_hound_folder, "hell_hound_idle"))),
            "jump": list(pygame.image.load(path.join(hell_hound_folder, "hell_hound_jump", f)) for f in listdir(path.join(hell_hound_folder, "hell_hound_jump"))),
            "walk": list(pygame.image.load(path.join(hell_hound_folder, "hell_hound_walk", f)) for f in listdir(path.join(hell_hound_folder, "hell_hound_walk"))),
            "run": list(pygame.image.load(path.join(hell_hound_folder, "hell_hound_run", f)) for f in listdir(path.join(hell_hound_folder, "hell_hound_run"))),
            "damaged": pygame.image.load(path.join(hell_hound_folder, "hell_hound_damaged.png")),
        }

        self.max_hp = 3
        Enemy.__init__(self, start_x, start_y, initial_state)

class Skull(Enemy):
    def __init__(self, start_x, start_y, initial_state="idle"):
        self.name = "skull"
        sprites_before = {
            "idle": list(pygame.image.load(path.join(skull_folder, "fire-skull", f)) for f in listdir(path.join(skull_folder, "fire-skull"))),
            "damaged": pygame.image.load(path.join(skull_folder, "skull_damaged.png")),
        }
        self.sprites = {
            "idle": list(pygame.transform.smoothscale(f,(48,56)) for f in sprites_before["idle"]),
            "damaged": pygame.transform.smoothscale(sprites_before["damaged"],(48,56)),
        }

        self.max_hp = 3
        Enemy.__init__(self, start_x, start_y, initial_state)

class Projectile:
    sprites = (pygame.image.load(f) for f in listdir(path.join(enemies_assets_folder, "projectile")))

monster_types = {"demon": Demon, "ghost": Ghost, "hell beast": Hell_Beast, "hell hound": Hell_Hound, "skull": Skull}
