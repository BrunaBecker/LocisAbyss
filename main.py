import pygame
from settings import clock, screen, pygame
from maps import active_map
from player import player
from projectiles import active_projectiles
from start_screen import current_start_screen

class GameState():
    def __init__(self):
        self.state = "start_screen"
        self.start_screen = current_start_screen

    def ingame(self):
        # Draw the entirety of the current map
        active_map.update()
        active_map.blit_lower_layers()

        # Updates every current projectile on map and deletes if it collides with something
        active_projectiles.update()
        pygame.sprite.groupcollide(active_map.collision_group, active_projectiles, False, True)
        pygame.sprite.groupcollide(active_map.volatile_collision, active_projectiles, False, True)

        # Updates and draws the player
        player.update()
        player.draw(screen)


        # Updates and draws the enemies that are alive
        active_map.enemies.update()
        active_map.enemies.draw(screen)

        # Draws the projectiles, then the higher layers of the map
        active_projectiles.draw(screen)
        active_map.blit_higher_layers()


# Main loop of the game
running = True
game = GameState()
pygame.mixer.music.play()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Esc keys closes the game
    keystate = pygame.key.get_pressed()
    if keystate[pygame.K_ESCAPE]:
        pygame.quit()

    # Start Screen to InGame transition
    if game.state == "start_screen":
        game.start_screen.draw_menu()
        if keystate[pygame.K_RETURN]:
            game.state = "fading"
            pygame.mixer.music.fadeout(3500)
            game.start_screen.confirm_sound.play()
        clock.tick(10)

    elif game.state == "fading":
        if game.start_screen.opacity_bg > 4000:
            game.state = "ingame"
            del game.start_screen
        else: 
            game.start_screen.draw_menu()
            game.start_screen.fade_out()
        clock.tick(10)
    elif game.state == "ingame":
        game.ingame()
        if active_map.map_transition:
            active_map.map_transition.draw()
            
        clock.tick(30)


    # Update the full display Surface to the screen. Necessary to draw anything at all.
    pygame.display.flip()
    