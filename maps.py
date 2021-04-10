import pygame
from pytmx.util_pygame import load_pygame

from collision import get_map_collision
from settings import maps_folder, path, screen

# Yikes... This file is not optimized at all. Proceed with caution.

# Load Maps. To be updated with more maps. Pay dear attention to escability!!
# Note from future: We've failed escability. TODO Come back to redo this when you have more maps.
class Map():
    def __init__(self, level):
        # Loads the data from the Tiled tmx file to the pygame format
        self.current_map = load_pygame(path.join(maps_folder, f"{level}.tmx"))
        # Do we need the tile width and height to be redone every map? Could just hardcore it on the settings if it stays the same throughout the game. < just makes it look better
        self.TILEWIDTH, self.TILEHEIGHT = self.current_map.tilewidth, self.current_map.tileheight
        # Starting and finishing position for the player when he gets in a new map
        self.start_coord = {
            "start": (1 * self.TILEWIDTH, 22 * self.TILEHEIGHT),
            "end": [(25 * self.TILEWIDTH, 3 * self.TILEHEIGHT), (26 * self.TILEWIDTH, 3 * self.TILEHEIGHT)],
        }

        # This creates the group that holds every single collision rectangle for walls and obstructing object
        # Should be done only once with every map load/change of level
        self.collision_group = pygame.sprite.Group()
        get_map_collision(screen, self.current_map, self.collision_group)
        self.collision_group.update()

    # This draws every tile from the current active map on the screen. Called every frame.
    def blit_all_tiles(self):
        # Get the index for every visible tile layer from the map data
        for i in self.current_map.visible_tile_layers:
            # For every single tile on this layer...
            for x, y, image in self.current_map.layers[i].tiles():
                # ...Draw it. The values of x and y here are also indexes, so we need to multiply them by the tile sizes.
                screen.blit(image, (x * self.TILEWIDTH, y * self.TILEHEIGHT))

active_map = Map("level_one")
