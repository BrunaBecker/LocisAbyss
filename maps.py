import pygame
from pytmx.util_pygame import load_pygame
import json
from collision import get_map_collision
from settings import maps_folder, path, screen
from enemy_archetypes import monster_types

# Load Maps. To be updated with more maps. Pay dear attention to escability!!
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

        self.interactions = {
            "level_one": {
                "lever": self.lever,
                "exit": None,
            }
        }

        self.enemies = pygame.sprite.Group()
        # TODO: clean previous group
        self.load_enemies_group()

    def lever(self):
        self.current_map.get_layer_by_name("doorlocked_object").visible = not self.current_map.get_layer_by_name("doorlocked_object").visible
        self.current_map.get_layer_by_name("doorlocked").visible = not self.current_map.get_layer_by_name("doorlocked").visible
        self.current_map.get_layer_by_name("doorunlocked").visible = not self.current_map.get_layer_by_name("doorunlocked").visible
        self.current_map.get_layer_by_name("leverlocked").visible = not self.current_map.get_layer_by_name("leverlocked").visible
        self.current_map.get_layer_by_name("leverunlocked").visible = not self.current_map.get_layer_by_name("leverunlocked").visible

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
        for enemy in self.enemies_load:
            self.enemies.add(monster_types[enemy["type"]](enemy["x"]*self.TILEWIDTH, enemy["y"]*self.TILEHEIGHT, enemy["initial_state"]))



active_map = Tmx_Map("level_one")

