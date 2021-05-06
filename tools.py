import pygame
import math
from settings import WIDTH, HEIGHT, clock, maps_folder, path
class Tools():

    @staticmethod
    def health_bar(screen, current_hp, max_hp, rect):
        quotient = current_hp/max_hp
        # if quotient == 1:
        #     return None

        black_bar_width = 30
        black_bar_height = 3
        red_bar_width = (current_hp/max_hp) * black_bar_width
        red_bar_height = 3

        x = rect.centerx
        y = rect.y + rect.height + 6

        black_bar = pygame.Rect(0, 0, black_bar_width, black_bar_height)
        black_bar.center = (x,y)
        red_bar = pygame.Rect(black_bar.x, black_bar.y, red_bar_width, red_bar_height)

        pygame.draw.rect(screen, (0,0,0), black_bar)  # black, background bar 
        pygame.draw.rect(screen, (255,0,0), red_bar)

    @staticmethod
    def get_distance(obj1, obj2):
        d = math.sqrt((obj2.rect.centerx - obj1.rect.centerx)**2 + (obj2.rect.centery - obj1.rect.centery)**2)
        return (True if d < 140 else False, (obj2.rect.x - obj1.rect.x), (obj2.rect.y - obj1.rect.y))

class boss_damage_area(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((160, 120))
        self.image.fill((139, 0, 0))
        self.image.set_alpha(120)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.centery = 0 ,0 
            
class Player_Collision():
    def __init__(self):
        self.rect = (0,0,0,0)

    def update(self, x, y, w, h):
        self.rect = (x, y, w, h)

class Fader():
    def __init__(self, screen, just_fadeout=False, game_over=False):
        self.screen = screen
        if just_fadeout:
            self.fadein = False
            self.fadeout = True
            self.min_opacity = 0
            self.max_opacity = 1600
            self.opacity = self.max_opacity
        else:
            self.fadein = True
            self.fadeout = False
            self.min_opacity = 0
            self.max_opacity = 1600
            self.opacity = self.min_opacity

        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill((0,0,0))
        if just_fadeout:
            self.image.set_alpha(255)
        else:
            self.image.set_alpha(0)
            

        self.ready_for_level_transition = False
        self.done = False
        self.game_over = game_over
        if game_over:
            self.max_opacity = 3000
            self.end_title = pygame.image.load(path.join(maps_folder, "end_title.png"))
            self.end_title.set_alpha(0)

    def update(self):
        if self.fadein:
            self.opacity += clock.get_time()
            if self.opacity >= self.max_opacity:
                self.opacity = self.max_opacity
                self.fadein = False
                self.ready_for_level_transition = True
            self.image.set_alpha((self.opacity/self.max_opacity)*255)
        elif self.fadeout:
            self.opacity -= clock.get_time()
            if self.opacity <= self.min_opacity:
                self.opacity = self.min_opacity
                self.done = True
            self.image.set_alpha((self.opacity/self.max_opacity)*255)

        if self.game_over:
            self.end_title.set_alpha((self.opacity/self.max_opacity)*255)

    def draw(self):
        self.screen.blit(self.image, (0,0))
        if self.game_over:
            self.screen.blit(self.end_title, (0,0))


area_damage = pygame.sprite.Group()
area_damage.add(boss_damage_area())

player_collision = Player_Collision()