import pygame
from settings import screen

# This creates a new standard Collision rectangle
class Collision_Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, width, height)

# Defines every collision rectangle for the active map
def get_map_collision(screen, level, collision_group):
    for group in level.objectgroups:
        for obj in group:
            collision_group.add(Collision_Block(obj.x, obj.y, obj.width, obj.height))

