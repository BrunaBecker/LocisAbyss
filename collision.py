import pygame
from settings import screen

# This creates a new standard Collision rectangle
class Collision_Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)

# Defines every collision rectangle for the active map
def get_map_collision(screen, level, collision_group):
    group = level.get_layer_by_name('wall_colliders')
    for obj in group:
        collision_group.add(Collision_Block(obj.x, obj.y, obj.width, obj.height))

def get_volatile_collision(level):
    collision_group = pygame.sprite.Group()
    for i in level.visible_object_groups:
        for obj in level.layers[i]:
            collision_group.add(Collision_Block(obj.x, obj.y, obj.width, obj.height))
    return collision_group

def get_interaction(level, x_player, y_player):
    group = level.get_layer_by_name('interactions')
    for obj in group:
        if obj.x == x_player and obj.y == y_player:
            return obj.name
    return None
