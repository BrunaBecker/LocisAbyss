from settings import clock, screen, pygame
from maps import active_map
from player import player
from projectiles import active_projectiles

# Initialize all imported pygame modules
pygame.init()

# Main loop of the game
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        pygame.quit()

    # Right now we don't need this to clean the screen, but we might in the future? Leaving here just in case
    # screen.fill((0, 0, 0)) 

    # Draw the entirety of the current map
    active_map.blit_lower_layers()
    # Updates and draws the player
    player.update()
    player.draw(screen)

    active_projectiles.update()
    active_projectiles.draw(screen)

    active_map.enemies.update()
    active_map.enemies.draw(screen)

    active_map.blit_higher_layers()
    # Update the full display Surface to the screen. Necessary to draw anything at all.
    pygame.display.flip()
    # Limits the FPS to 30
    clock.tick(30)

