import pygame

class Tools():
    @staticmethod
    def health_bar(screen, current_hp, max_hp, cx, cy, sprite_width, sprite_height):
        quotient = current_hp/max_hp
        if quotient == 1:
            return None

        black_bar_width = 30
        black_bar_height = 3
        red_bar_width = (current_hp/max_hp) * black_bar_width
        red_bar_height = 3

        x = cx + 1
        y = cy - 10

        pygame.draw.rect(screen, (0,0,0), pygame.Rect(x, y, black_bar_width, black_bar_height))  # black, background bar 
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(x, y, red_bar_width, red_bar_height))
        
