import pygame
from settings import projectiles_assets_folder, WIDTH, HEIGHT, CLEAR, clock, path
from os import listdir

SPRITE_RATE = 120
class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, latitude, longitude, color):
        pygame.sprite.Sprite.__init__(self)
        self.latitude = latitude
        self.longitude = longitude
        self.projectile_color = color
        
        self.sprites = {
            "red": list(pygame.image.load(path.join(projectiles_assets_folder, "red", f)) for f in listdir(path.join(projectiles_assets_folder, "red"))),
            "blue": list(pygame.image.load(path.join(projectiles_assets_folder, "blue", f)) for f in listdir(path.join(projectiles_assets_folder, "blue"))),
            "dark": list(pygame.image.load(path.join(projectiles_assets_folder, "dark", f)) for f in listdir(path.join(projectiles_assets_folder, "dark"))),
        }

        self.current_sprite_frame = 0
        self.sprite_timer = SPRITE_RATE

        self.get_rotated_image()
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = start_x, start_y


    def update(self):

        self.sprite_timer += clock.get_time()

        if self.latitude == "north":
            self.rect.y -= clock.get_time()/4
        elif self.latitude == "south":
            self.rect.y += clock.get_time()/4
        if self.longitude == "west":
            self.rect.x -= clock.get_time()/4
        elif self.longitude == "east":
            self.rect.x += clock.get_time()/4

        self.movement_timer = CLEAR

        if self.sprite_timer >= SPRITE_RATE:
            self.current_sprite_frame = (self.current_sprite_frame + 1) % len(self.sprites[self.projectile_color])
            self.get_rotated_image()
            self.sprite_timer = CLEAR

        # for proj in active_projectiles:
        if self.rect.x < 0 or self.rect.x >= WIDTH or self.rect.y < 0 or self.rect.y >= HEIGHT:
            self.kill()

    def get_rotated_image(self):
        unchanged_image = self.sprites[self.projectile_color][self.current_sprite_frame]
        directions = {"west": 0, "southwest": 45, "south": 90, "southeast": 135, "east": 180, "northeast": 225, "north": 270, "northwest": 315}
        self.image = pygame.transform.rotate(unchanged_image, directions.get(self.latitude+self.longitude))

active_projectiles = pygame.sprite.Group()