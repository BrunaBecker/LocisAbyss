import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, archetype, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        self.enemy_type = archetype
        