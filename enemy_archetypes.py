import pygame
from settings import path, enemies_assets_folder
from enemies import Enemy, Tools, clock, CLEAR, SPRITE_RATE, ATTACK_RATE
from projectiles import Bullet, active_projectiles
from os import listdir
from collision import Collision_Block

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
        self.x_offset , self.y_offset = 0,0


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
        self.x_offset , self.y_offset = 0,0
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

        if self.attack_timer >= ATTACK_RATE and self.within_range:
            self.attack()

        Enemy.update(self)
    
    def attack(self):
        active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, "", "west", "dark"))
        active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, "", "east", "dark"))
        active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, "north", "", "dark"))
        active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, "south", "", "dark"))
        self.attack_timer = CLEAR

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
            "pre_burn": list(pygame.image.load(path.join(hell_beast_folder, "hell_beast_nobreath", f)) for f in listdir(path.join(hell_beast_folder, "hell_beast_nobreath"))),
            "burn": list(pygame.image.load(path.join(hell_beast_folder, "hell_beast_burn", f)) for f in listdir(path.join(hell_beast_folder, "hell_beast_burn"))),
            "after_burn": list(pygame.image.load(path.join(hell_beast_folder, "after_burn", f)) for f in listdir(path.join(hell_beast_folder, "after_burn"))),
            "damaged": pygame.image.load(path.join(hell_beast_folder, "hell_beast_damaged.png")),
        }
        self.x_offset , self.y_offset = 0,0
        self.max_hp = 8
        Enemy.__init__(self, start_x, start_y, initial_state)

    def update(self):
        if self.attack_timer >= ATTACK_RATE + 1000 and self.within_range:
            self.attack()
        
        if self.current_sprite_frame == len(self.sprites["pre_burn"])-1 and self.current_state == "pre_burn":
            if not self.within_range:
                self.current_state = "idle"
                self.current_sprite_frame = 0
                self.x_offset = 0
                self.y_offset = 0
            else:
                self.current_state = "burn"
                self.current_sprite_frame = 0
                if self.current_flip == "east":
                    self.x_offset = -10
                else: 
                    self.x_offset = -6
                self.y_offset = -92

        if self.current_sprite_frame == 2 and self.current_state == "burn":
            demon_burn_column.add(Collision_Block(self.rect.x, self.rect.y, self.rect.width, self.rect.height))
        elif self.current_sprite_frame == len(self.sprites["burn"])-1 and self.current_state == "burn":
            demon_burn_column.empty()
            self.current_state = "after_burn"
            self.current_sprite_frame = 0
        
        if self.current_sprite_frame == len(self.sprites["after_burn"])-1 and self.current_state == "after_burn":
            self.current_state = "idle"
            self.current_sprite_frame = 0
            self.x_offset = 0
            self.y_offset = 0

        Enemy.update(self)
    
    def attack(self):
        self.current_state = "pre_burn"
        self.current_sprite_frame = 0
        self.x_offset = -3
        self.y_offset = 2
        self.attack_timer = CLEAR
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
        self.x_offset , self.y_offset = 0,0
        self.max_hp = 3
        Enemy.__init__(self, start_x, start_y, initial_state)

    def update(self):
        if self.attack_timer >= ATTACK_RATE and self.within_range:
            self.attack()

        Enemy.update(self)
    
    def attack(self):
        active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, self.player_latitude, self.current_flip, "blue"))
        self.attack_timer = CLEAR
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
        self.x_offset , self.y_offset = 0,0
        self.max_hp = 3
        Enemy.__init__(self, start_x, start_y, initial_state)
    
    def update(self):
        if self.attack_timer >= ATTACK_RATE and self.within_range:
            self.attack()

        Enemy.update(self)
    
    def attack(self):
        if self.current_flip == "":
            active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, self.player_latitude, "", "red"))
            active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, self.player_latitude, "west", "red"))
            active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, self.player_latitude, "east", "red"))
        else:
            active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, "", self.current_flip, "red"))
            active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, "south", self.current_flip, "red"))
            active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, "north", self.current_flip, "red"))
        self.attack_timer = CLEAR

monster_types = {"demon": Demon, "ghost": Ghost, "hell beast": Hell_Beast, "hell hound": Hell_Hound, "skull": Skull}
demon_burn_column = pygame.sprite.GroupSingle()
