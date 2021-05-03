import pygame
from settings import screen

# This creates a new standard Collision block
class Collision_Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)

# Defines every collision rectangle for the active map
def get_map_collision(screen, level, collision_group):
    # Gets the data from a single layer, wall colliders, on .tmx data
    group = level.get_layer_by_name('wall_colliders')
    for obj in group:
        collision_group.add(Collision_Block(obj.x, obj.y, obj.width, obj.height))

# Volatile collision are every collision of block in the map that are susceptible to change during gameplay
# An example of this is the door on the first level, that may be toggled on or off
def get_volatile_collision(level):
    collision_group = pygame.sprite.Group()
    # Visible objects layers on .tmx data
    for i in level.visible_object_groups:
        for obj in level.layers[i]:
            collision_group.add(Collision_Block(obj.x, obj.y, obj.width, obj.height))
    return collision_group

# Return an interaction that may be activate if the player is inside a interactive block
def get_interaction(level, x_player, y_player):
    # The interactive blocks are defined in the .tmx data
    group = level.get_layer_by_name('interactions')
    for obj in group:
        if obj.x == x_player and obj.y == y_player and not obj.properties["destroyed"]:
            return obj
    return None
