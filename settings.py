import pygame
from pygame.time import Clock
from os import path

clock = Clock()

WIDTH, HEIGHT = 1280, 1024  # Map Size used to define Window
CLEAR = 0  # Used to clear clocks

# Relative Paths Shortcuts
loci_dir = path.dirname(__file__)
assets_folder = path.join(loci_dir, "assets")
player_assets_folder = path.join(assets_folder, "Knight")
maps_folder = path.join(loci_dir, "maps")
pygame.display.set_caption("Loci's Tower")
# window_icon = pygame.image.load('logo.png')
# pygame.display.set_icon(window_icon)

# Initialize a window or screen for display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
