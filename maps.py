import pygame
from pytmx.util_pygame import load_pygame
import json
from collision import get_map_collision, get_volatile_collision
from settings import maps_folder, path, screen, clock, audio_folder
from enemy_archetypes import monster_types
from projectiles import active_projectiles
from tools import Fader

class Tmx_Map():
    def __init__(self, level):
        self.name = level
        # Loads the data from the Tiled tmx file to the pygame format
        self.current_map = load_pygame(path.join(maps_folder, f"{level}.tmx"))
        # Do we need the tile width and height to be redone every map? Could just hardcore it on the settings if it stays the same throughout the game. < just makes it look better
        self.TILEWIDTH, self.TILEHEIGHT = self.current_map.tilewidth, self.current_map.tileheight
        # Starting and finishing position for the player when he gets in a new map
        with open(path.join(maps_folder, "maps_meta.json")) as f:
            map_meta = json.load(f)[self.name]
        self.enemies_load = map_meta["enemies"]
        self.start_coord = [map_meta["player_x"]*self.TILEWIDTH, map_meta["player_y"]*self.TILEHEIGHT]
        # This creates the group that holds every single collision rectangle for walls and obstructing object
        # Should be done only once with every map load/change of level
        self.collision_group = pygame.sprite.Group()
        get_map_collision(screen, self.current_map, self.collision_group)
        self.collision_group.update()
        self.volatile_collision = get_volatile_collision(self.current_map)
        self.map_loaded = True
        self.map_transition = Fader(screen, just_fadeout=True)
        self.game_over = False
        self.level_three_counter = 0

        self.interactions = {
            "level_one": {
                "break": self.break_fence_level_one,
                "lever": self.lever_level_one,
                "exit": self.fade_screen,
            },
            "level_two": {
                "break": self.break_fence_level_two,
                "lever": self.lever_level_two,
                "exit": self.fade_screen,
            }  ,
            "level_three": {
                "lever_r": self.lever_r,
                "lever_l": self.lever_l
            }          
        }

        self.enemies = pygame.sprite.Group()
        self.load_enemies_group()

    def break_fence_level_one(self):
        self.current_map.get_layer_by_name("fence_corridor").visible = False
        self.current_map.get_layer_by_name("fence_corridor_object").visible = False
        for obj in self.current_map.get_layer_by_name("interactions"):
            if obj.name == "break":
                obj.properties["destroyed"] = True

    def lever_level_one(self):
        self.current_map.get_layer_by_name("doorlocked_object").visible = not self.current_map.get_layer_by_name("doorlocked_object").visible
        self.current_map.get_layer_by_name("doorlocked").visible = not self.current_map.get_layer_by_name("doorlocked").visible
        self.current_map.get_layer_by_name("doorunlocked").visible = not self.current_map.get_layer_by_name("doorunlocked").visible
        self.current_map.get_layer_by_name("leverlocked").visible = not self.current_map.get_layer_by_name("leverlocked").visible
        self.current_map.get_layer_by_name("leverunlocked").visible = not self.current_map.get_layer_by_name("leverunlocked").visible

    def break_fence_level_two(self):
        self.current_map.get_layer_by_name("fence_treasureroom").visible = False
        self.current_map.get_layer_by_name("fence_treasureroom_object").visible = False
        for obj in self.current_map.get_layer_by_name("interactions"):
            if obj.name == "break":
                obj.properties["destroyed"] = True

    def lever_level_two(self):
        self.current_map.get_layer_by_name("room_torch_toggled_off").visible = not self.current_map.get_layer_by_name("room_torch_toggled_off").visible
        self.current_map.get_layer_by_name("room_torch_toggled_on").visible = not self.current_map.get_layer_by_name("room_torch_toggled_off").visible
        self.current_map.get_layer_by_name("darkroom").visible = not self.current_map.get_layer_by_name("darkroom").visible
        self.current_map.get_layer_by_name("leverlocked").visible = not self.current_map.get_layer_by_name("leverlocked").visible
        self.current_map.get_layer_by_name("leverunlocked").visible = not self.current_map.get_layer_by_name("leverunlocked").visible
        self.current_map.get_layer_by_name("fence_darkroom").visible = False
        self.current_map.get_layer_by_name("fence_darkroom_object").visible = False

    def lever_r(self):
        self.current_map.get_layer_by_name("leverrightunlocked").visible = not self.current_map.get_layer_by_name("leverrightunlocked").visible
        self.current_map.get_layer_by_name("leverrightlocked").visible = not self.current_map.get_layer_by_name("leverrightlocked").visible

    def lever_l(self):
        self.current_map.get_layer_by_name("leverleftunlocked").visible = not self.current_map.get_layer_by_name("leverleftunlocked").visible
        self.current_map.get_layer_by_name("leverleftlocked").visible = not self.current_map.get_layer_by_name("leverleftlocked").visible


    # This draws every tile from the current active map on the screen. Called every frame.
    def blit_lower_layers(self):
            for i in self.current_map.visible_tile_layers:
                layer = self.current_map.layers[i]
                # For every single tile on this layer...
                if not layer.properties.get('layer_above_player'):
                    for x, y, image in layer.tiles():
                        # ...Draw it. The values of x and y here are also indexes, so we need to multiply them by the tile sizes.
                        screen.blit(image, (x * self.TILEWIDTH, y * self.TILEHEIGHT))

    # This draws every tile from the current active map on the screen. Called every frame.
    def blit_higher_layers(self):
            for i in self.current_map.visible_tile_layers:
                layer = self.current_map.layers[i]
                # For every single tile on this layer...
                if layer.properties.get('layer_above_player'):
                    for x, y, image in layer.tiles():
                        # ...Draw it. The values of x and y here are also indexes, so we need to multiply them by the tile sizes.
                        screen.blit(image, (x * self.TILEWIDTH, y * self.TILEHEIGHT))

    def load_enemies_group(self):
        colliders_rect = list()
        for tile in self.collision_group:
            colliders_rect.append(pygame.Rect(tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height))
        for tile in self.volatile_collision:
            colliders_rect.append(pygame.Rect(tile.rect.x, tile.rect.y, tile.rect.width, tile.rect.height))

        for enemy in self.enemies_load:
            self.enemies.add(monster_types[enemy["type"]](enemy["x"]*self.TILEWIDTH, enemy["y"]*self.TILEHEIGHT, colliders_rect, initial_state=enemy["initial_state"]))

    def next_level(self, restart=False):
        if restart:
            active_projectiles.empty()
            self.__init__(self.name)

        elif self.name == "level_one":
            active_projectiles.empty()
            self.__init__("level_two")
        elif self.name == "level_two":
            active_projectiles.empty()
            self.level_three_counter = 0
            pygame.mixer.music.fadeout(2000)
            pygame.mixer.music.load(path.join(audio_folder, "DragonCastle.ogg"))
            pygame.mixer.music.play(-1, 0.0, 500)
            self.__init__("level_three")

    def fade_screen(self):
        self.map_transition = Fader(screen)


    def update(self):
        self.volatile_collision = get_volatile_collision(active_map.current_map)

        if self.map_transition:
            self.map_transition.update()
            if self.map_transition.ready_for_level_transition:
                self.map_transition.ready_for_level_transition = False
                self.next_level()
            if self.map_transition.done:
                self.map_transition = None

        if self.name == "level_two" and not any(self.enemies):
            self.current_map.get_layer_by_name("doorlocked_object").visible = False
            self.current_map.get_layer_by_name("doorlocked").visible = False
            self.current_map.get_layer_by_name("doorunlocked").visible = True
        elif self.name == "level_three":
            if self.current_map.get_layer_by_name("leverrightunlocked").visible and self.current_map.get_layer_by_name("leverleftunlocked").visible:
                self.current_map.get_layer_by_name("barrier").visible = False
                self.current_map.get_layer_by_name("fence_collider").visible = False
            if not any(self.enemies):
                self.level_three_counter += clock.get_time()
                if self.level_three_counter >= 3500:
                    if not self.map_transition:
                        self.map_transition = Fader(screen, game_over=True)

active_map = Tmx_Map("level_one")
