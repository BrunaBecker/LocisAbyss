import pygame
import math
class Tools():
    @staticmethod
    # def health_bar(screen, current_hp, max_hp, cx, cy, sprite_width, sprite_height):
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
        
