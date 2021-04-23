import pygame
from settings import projectiles_assets_folder, WIDTH, HEIGHT, CLEAR, clock, path

MOVEMENT_RATE = 220
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, latitude, longitude):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = self.get_rotated_image(latitude, longitude)
        self.rect = self.image.get_rect()

        self.rect.centerx, self.rect.centery = start_x, start_y
        self.latitude = latitude
        self.longitude = longitude

    def update(self):
        if self.latitude == "north":
            self.rect.y -= clock.get_time()/4
        elif self.latitude == "south":
            self.rect.y += clock.get_time()/4
        if self.longitude == "west":
            self.rect.x -= clock.get_time()/4
        elif self.longitude == "east":
            self.rect.x += clock.get_time()/4

        self.movement_timer = CLEAR

        for proj in active_projectiles:
            if proj.rect.x < 0 or proj.rect.x >= WIDTH or proj.rect.y < 0 or proj.rect.y >= HEIGHT:
                proj.kill()

    def get_rotated_image(self, latitude, longitude):
        image = pygame.image.load(path.join(projectiles_assets_folder, "blue-fireball.png"))
        directions = {"west": 0, "southwest": 45, "south": 90, "southeast": 135, "east": 180, "northeast": 225, "north": 270, "northwest": 315}
        return pygame.transform.rotate(image, directions.get(latitude+longitude))

active_projectiles = pygame.sprite.Group()