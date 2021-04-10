import pygame

from settings import clock, screen
from maps import active_map
from player import player

# Initialize all imported pygame modules
pygame.init()

# Main loop of the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Right now we don't need this to clean the screen, but we might in the future? Leaving here just in case
    # screen.fill((0, 0, 0)) 

    # Draw the entirety of the current map
    active_map.blit_all_tiles()
    # Updates and draws the player
    player.update()
    player.draw(screen)

    # Update the full display Surface to the screen. Necessary to draw anything at all.
    pygame.display.flip()
    # Limits the FPS to 30
    clock.tick(30)
