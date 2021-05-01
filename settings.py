import pygame
from pygame.time import Clock
from os import path

# Initialize all imported pygame modules
pygame.init()
clock = Clock()


WIDTH, HEIGHT = 1280, 1024  # Map Size used to define Window
CLEAR = 0  # Used to clear clocks

# Relative Paths Shortcuts
loci_dir = path.dirname(__file__)
maps_folder = path.join(loci_dir, "maps")
assets_folder = path.join(loci_dir, "assets")
start_screen_folder = path.join(assets_folder, "Start_Screen")
audio_folder = path.join(assets_folder, "Audio")
player_assets_folder = path.join(assets_folder, "Knight")
enemies_assets_folder = path.join(assets_folder, "Enemies")
projectiles_assets_folder = path.join(enemies_assets_folder, "projectiles")


pygame.display.set_caption("Loci's Abyss")
window_icon = pygame.image.load(path.join(assets_folder, 'locilogo.png'))
pygame.display.set_icon(window_icon)

# Initialize a window or screen for display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

fool_font = pygame.font.Font(path.join(assets_folder, "fool.ttf"), 20)
interact_text_width = fool_font.size("Press F to interact")[0]
