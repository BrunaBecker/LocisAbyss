import pygame
from settings import path, enemies_assets_folder, screen
from enemies import Enemy, Tools, clock, CLEAR, SPRITE_RATE, ATTACK_RATE, TILE_WIDTH, TILE_HEIGHT, randint
from projectiles import Bullet, active_projectiles
from os import listdir
from collision import Collision_Block
from tools import area_damage

demon_folder = path.join(enemies_assets_folder, "demon_boss")
ghost_folder = path.join(enemies_assets_folder, "ghost")
hell_beast_folder = path.join(enemies_assets_folder, "hell_beast")
hell_hound_folder = path.join(enemies_assets_folder, "hell_hound")
nightmare_folder = path.join(enemies_assets_folder, "nightmare")
skull_folder = path.join(enemies_assets_folder, "skull")
class Demon(Enemy):
    def __init__(self, start_x, start_y, colliders, initial_state="idle"):
        self.name = "demon"
        self.sprites = {
            "idle": list(pygame.image.load(path.join(demon_folder, "demon_idle", f)) for f in listdir(path.join(demon_folder, "demon_idle"))),
            "attack": list(pygame.image.load(path.join(demon_folder, "demon_attack_breath", f)) for f in listdir(path.join(demon_folder, "demon_attack_breath"))),
            "damaged": pygame.image.load(path.join(demon_folder, "demon_damaged.png")),
        }
        self.x_offset , self.y_offset = 0,0
        self.shoot_type = 0
        self.max_hp = 20
        self.area = area_damage.sprites()[0]
        self.shooting = False
        self.shooting_type = 0
        self.shooting_frame = 0
        self.shoothing_clock = CLEAR

        Enemy.__init__(self, start_x, start_y, colliders, initial_state="idle")

    def update(self):
        self.shoothing_clock += clock.get_time()

        if self.attack_timer >= ATTACK_RATE + 2000 and self.within_range:
            self.attack()

        if self.move_timer == 0 and self.ready_to_move:
            if self.x_distance != 0 or self.y_distance != 0:
                if self.x_distance != 0 and (abs(self.x_distance) < abs(self.y_distance) or self.y_distance == 0):
                    self.x -= self.x_distance/abs(self.x_distance) * TILE_WIDTH
                    self.ready_to_move = False
                elif self.y_distance != 0 and (abs(self.y_distance) < abs(self.x_distance) or self.x_distance == 0):
                    self.y += self.y_distance/abs(self.y_distance) * TILE_HEIGHT
                    self.ready_to_move = False

        if self.current_state == "attack":
            if self.current_flip == "east":
                self.x_offset = 0
                self.y_offset = -30
            else:
                self.x_offset = -65
                self.y_offset = -30

            if 0 < self.current_sprite_frame < 8:
                area_damage.draw(screen)
            if self.current_sprite_frame == 8:
                boss_breath.add(Collision_Block(self.area.rect.x, self.area.rect.y, self.area.rect.width, self.area.rect.height))
                self.shooting = True

            elif self.current_sprite_frame == len(self.sprites["attack"])-1:
                boss_breath.empty()
                self.current_state = "idle"
                self.current_sprite_frame = 0
                self.x_offset = 0
                self.y_offset = 0

        self.shoot()
        Enemy.update(self)

    def attack(self):
        self.current_state = "attack"
        self.current_sprite_frame = 0
        self.attack_timer = CLEAR
        if self.current_flip == "east":
            self.x_offset = 0
            self.y_offset = -30
        else:
            self.x_offset = -65
            self.y_offset = -30

        if self.current_flip == "east":
            self.area.rect.x, self.area.rect.y = self.rect.centerx - 40, self.rect.centery
        else:
            self.area.rect.x, self.area.rect.y = self.rect.centerx - self.area.rect.width + 40, self.rect.centery

    def shoot(self):
        clock = [
                    [(self.rect.centerx, self.rect.centery, "north", "", "dark")],
                    [(self.rect.centerx, self.rect.centery, "north", "east", "dark")],
                    [(self.rect.centerx, self.rect.centery, "", "east", "dark")],
                    [(self.rect.centerx, self.rect.centery, "south", "east", "dark")],
                    [(self.rect.centerx, self.rect.centery, "south", "", "dark")],
                    [(self.rect.centerx, self.rect.centery, "south", "west", "dark")],
                    [(self.rect.centerx, self.rect.centery, "", "west", "dark")],
                    [(self.rect.centerx, self.rect.centery, "north", "west", "dark")]
                ]
        star = [
            [
                (self.rect.centerx, self.rect.centery, "north", "", "dark"),
                (self.rect.centerx, self.rect.centery, "south", "", "dark"),
                (self.rect.centerx, self.rect.centery, "", "west", "dark"),
                (self.rect.centerx, self.rect.centery, "", "east", "dark")
            ],
            [
                (self.rect.centerx, self.rect.centery, "north", "west", "dark"),
                (self.rect.centerx, self.rect.centery, "north", "east", "dark"),
                (self.rect.centerx, self.rect.centery, "south", "west", "dark"),
                (self.rect.centerx, self.rect.centery, "south", "east", "dark")
            ]
        ]
        attacks = [clock, star]

        if self.shooting and self.shoothing_clock >= (40 if self.shoot_type%2 == 0 else 240):
            for bullet_stat in attacks[self.shoot_type%2][self.shooting_frame]:
                active_projectiles.add(Bullet(*bullet_stat))
            self.shoothing_clock = CLEAR
            self.shooting_frame = self.shooting_frame+1
            if self.shooting_frame == len(attacks[self.shoot_type%2]):
                self.shooting = False
                self.shooting_frame = 0
                self.shoot_type += 1

class Ghost(Enemy):

    def __init__(self, start_x, start_y, colliders, initial_state="idle"):
        self.name= "ghost"
        self.sprites = {
            "spawn": list(pygame.image.load(path.join(ghost_folder, "ghost_appears", f)) for f in listdir(path.join(ghost_folder, "ghost_appears"))),
            "idle": list(pygame.image.load(path.join(ghost_folder, "ghost_idle", f)) for f in listdir(path.join(ghost_folder, "ghost_idle"))),
            "shriek": list(pygame.image.load(path.join(ghost_folder, "ghost_shriek", f)) for f in listdir(path.join(ghost_folder, "ghost_shriek"))),
            "death": list(pygame.image.load(path.join(ghost_folder, "ghost_death", f)) for f in listdir(path.join(ghost_folder, "ghost_death"))),
            "damaged": pygame.image.load(path.join(ghost_folder, "ghost_damaged.png")),
            "hidden": [pygame.Surface((32,32))]
        }
        self.movement_pattern = [self.move_east, self.move_east, self.move_east, self.move_west, self.move_west, self.move_west]
        self.movement_count = randint(0, len(self.movement_pattern)-1)

        self.x_offset , self.y_offset = 0,0
        self.sprite_counters = {}
        self.max_hp = 5
        Enemy.__init__(self, start_x, start_y, colliders, initial_state)

    def update(self):
        if self.within_range and self.current_state == "hidden":
            self.current_state = "spawn"
            self.current_sprite_frame = 0
            self.sprite_counters["spawn_counter"] = len(self.sprites["spawn"])

        if self.sprite_timer + clock.get_time() >= SPRITE_RATE:
            self.decrease_counters()

        if self.attack_timer >= ATTACK_RATE and self.within_range:
            self.attack()

        if self.move_timer == 0:
            self.movement_pattern[self.movement_count]()
            self.movement_count = (self.movement_count+1)%len(self.movement_pattern)
            self.move_timer = 1600

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
    def __init__(self, start_x, start_y, colliders, initial_state="idle"):
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
        Enemy.__init__(self, start_x, start_y, colliders, initial_state="idle")

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

        if self.current_sprite_frame == len(self.sprites["after_burn"])-1 and self.current_state == "after_burn":
            self.current_state = "idle"
            self.current_sprite_frame = 0
            self.x_offset = 0
            self.y_offset = 0
            self.move_timer = 120
            self.ready_to_move = True

        if self.move_timer == 0 and self.ready_to_move:
            if self.x_distance != 0 or self.y_distance != 0:
                if self.x_distance != 0 and (abs(self.x_distance) < abs(self.y_distance) or self.y_distance == 0):
                    self.x -= self.x_distance/abs(self.x_distance) * TILE_WIDTH
                    self.ready_to_move = False
                elif self.y_distance != 0 and (abs(self.y_distance) < abs(self.x_distance) or self.x_distance == 0):
                    self.y += self.y_distance/abs(self.y_distance) * TILE_HEIGHT
                    self.ready_to_move = False

        if self.current_sprite_frame == 2 and self.current_state == "burn":
            demon_burn_column.add(Collision_Block(self.x, self.y, self.rect.width, self.rect.height))
        elif self.current_sprite_frame == len(self.sprites["burn"])-1 and self.current_state == "burn":
            demon_burn_column.empty()
            self.current_state = "after_burn"
            self.current_sprite_frame = 0

        Enemy.update(self)

    def attack(self):
        self.current_state = "pre_burn"
        self.current_sprite_frame = 0
        self.x_offset = -3
        self.y_offset = 2
        self.attack_timer = CLEAR
class Hell_Hound(Enemy):
    def __init__(self, start_x, start_y, colliders, initial_state="idle"):
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
        Enemy.__init__(self, start_x, start_y, colliders, initial_state="idle")
        self.movement_pattern = [self.move_south, self.move_east, self.move_north, self.move_west]
        self.movement_count = randint(0, len(self.movement_pattern)-1)

    def update(self):
        if self.attack_timer >= ATTACK_RATE and self.within_range:
            self.attack()

        if self.move_timer == 0:
            self.movement_pattern[self.movement_count]()
            self.movement_count = (self.movement_count+1)%len(self.movement_pattern)
            self.move_timer = 1600

        Enemy.update(self)

    def attack(self):
        active_projectiles.add(Bullet(self.rect.centerx, self.rect.centery, self.player_latitude, self.current_flip, "blue"))
        self.attack_timer = CLEAR
class Skull(Enemy):
    def __init__(self, start_x, start_y, colliders, initial_state="idle"):
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
        self.movement_pattern = [self.move_south, self.move_south, self.move_east, self.move_north, self.move_north, self.move_west]
        self.movement_count = randint(0, len(self.movement_pattern)-1)

        Enemy.__init__(self, start_x, start_y, colliders, initial_state="idle")

    def update(self):
        if self.attack_timer >= ATTACK_RATE and self.within_range:
            self.attack()

        if self.move_timer == 0:
            self.movement_pattern[self.movement_count]()
            self.movement_count = (self.movement_count+1)%len(self.movement_pattern)
            self.move_timer = 1600

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
boss_breath = pygame.sprite.GroupSingle()
