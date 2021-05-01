import pygame
import json
from settings import player_assets_folder, CLEAR, WIDTH, HEIGHT, path, clock, fool_font, screen, interact_text_width
from maps import active_map
from collision import Collision_Block, get_interaction
from tools import Tools
from projectiles import active_projectiles
from enemy_archetypes import demon_burn_column

SPRITE_RATE = 60  # Sets the interval between sprites updates
MOVEMENT_RATE = 220  # Sets the interval between player movement

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # All options of animations for the Player depending on his state
        self.list_of_states = {
            "idle": {
                "sprite_sheet": pygame.image.load(path.join(player_assets_folder, "KnightIdle_strip.png")).convert(),
                "meta_data": None,
                "path_data": path.join(player_assets_folder, "KnightIdle_strip.json"),
            },
            "run": {
                # TODO: holder
                "sprite_sheet": pygame.image.load(path.join(player_assets_folder, "KnightIdle_strip.png")).convert(),
                "meta_data": None,
                "path_data": path.join(player_assets_folder, "KnightIdle_strip.json"),
            },
            "attack": {
                "sprite_sheet": pygame.image.load(path.join(player_assets_folder, "KnightAttack_strip.png")).convert(),
                "meta_data": None,
                "path_data": path.join(player_assets_folder, "KnightAttack_strip.json"),
            },
            "death": {
                # TODO: holder
                "sprite_sheet": pygame.image.load(path.join(player_assets_folder, "KnightIdle_strip.png")).convert(),
                "meta_data": None,
                "path_data": path.join(player_assets_folder, "KnightIdle_strip.json"),
            },
        }
        # Sets the starting state
        self.current_state = self.list_of_states["idle"]
        # This creates a empty/placeholder surface and rect to be filled with the first call to the sprite
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        # Defines starting position of the player to the start position of the map
        self.x, self.y = active_map.start_coord
        # Rect.x and Rect.y are the variable that  sets the player position, but we need to keep self.x and self.y separate because it's the one we are actually going to update
        self.rect.x, self.rect.y = self.x, self.y

        self.max_hp = 10
        self.hp = self.max_hp

        # Start clocks and cooldowns
        self.sprite_timer = SPRITE_RATE
        self.movement_timer = CLEAR
        self.attack_timer = CLEAR
        self.current_frame = CLEAR
        self.attack_frame = CLEAR
        self.interact_timer = CLEAR
        self.damaged_timer = CLEAR
        # Sets the starting player horizontal orientation. Needed to flip its sprites when it change directions.
        self.current_flip = "right"


        # Initialize the meta data for each state's spritesheet
        for state in self.list_of_states:
            with open(self.list_of_states[state]["path_data"]) as f:
                self.list_of_states[state]["meta_data"] = json.load(f)
            f.close()

    # Use the meta data for the spritesheet to get the current frame for the animation
    def get_sprite(self, x, y, w, h):
        # Creates a surface of the right size
        sprite = pygame.Surface((w, h))
        # Defines what color is the background to be cut out of the frame
        # Draw the defined piece of the spritesheet onto the sprite to be drawn
        sprite.blit(self.current_state["sprite_sheet"], (0, 0), (x, y, w, h))
        sprite.set_colorkey((113, 102, 79))
        return sprite

    # Analyzes and updates the sprite to be drawn this frame
    def parse_sprite(self):
        # Gets the name of the current frame of this sprite
        name = self.current_state["meta_data"]["list_of_frames"][self.current_frame]
        # Uses the name of the current frame of this sprite to get its data
        sprite = self.current_state["meta_data"]["frames"][name]["frame"]
        x, y, w, h = sprite["x"], sprite["y"], sprite["w"], sprite["h"]
        # Defines the image to be drawn according to the meta data
        self.image = self.get_sprite(x, y, w, h)
        self.rect = self.image.get_rect()

        # Draw the flipped sprite if the player is turning left
        if self.current_flip == "left":
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.x, self.rect.y = (
                self.x - self.current_state["meta_data"]["frames"][name]["flip_offset"][0] + 4,
                self.y - self.current_state["meta_data"]["frames"][name]["flip_offset"][1],
            )
        # Draw the normal version if the player is turning right
        else:
            self.rect.x, self.rect.y = (
                self.x - self.current_state["meta_data"]["frames"][name]["offset"][0] + 4,
                self.y - self.current_state["meta_data"]["frames"][name]["offset"][1],
            )

        # This makes the frame of the sprite reset back to 0 after reaching the last one
        self.current_frame = (self.current_frame + 1) % self.current_state["meta_data"]["frame_quantity"]

        # This is the logic for the 3 separated attack animations
        # Sets animation back to 'idle' if it reaches the end of the animation
        if self.current_state == self.list_of_states["attack"] and self.current_frame == 7:
            # First attack is composed of frames 0 to 7
            self.current_state = self.list_of_states["idle"]
            # Makes the idle animations starts from the start
            self.current_frame = CLEAR
            # Sets the next attack animation starting frame
            self.attack_frame = 7
        elif self.current_state == self.list_of_states["attack"] and self.current_frame == 12:
            # First attack is composed of frames 7 to 12
            self.current_state = self.list_of_states["idle"]
            # Makes the idle animations starts from the start
            self.current_frame = CLEAR
            # Sets the next attack animation starting frame
            self.attack_frame = 12
        elif self.current_state == self.list_of_states["attack"] and self.current_frame == (
            # First attack is composed of frames 12 to 21
            self.current_state["meta_data"]["frame_quantity"] - 1
        ):
            # Makes the idle animations starts from the start
            self.current_frame = CLEAR
            self.current_state = self.list_of_states["idle"]
            # Sets the next attack animation starting frame
            self.attack_frame = CLEAR

        self.sprite_timer = CLEAR

    def not_colliding(self, direction):
        return (pygame.sprite.spritecollideany(self.collision_wings[direction], active_map.collision_group) is None
                and pygame.sprite.spritecollideany(self.collision_wings[direction], active_map.volatile_collision) is None
                and pygame.sprite.spritecollideany(self.collision_wings[direction], active_map.enemies) is None)

    def attack_enemy(self):
        if self.current_flip == "right":
            enemy_hit = pygame.sprite.spritecollideany(self.collision_wings["east"], active_map.enemies)
            if enemy_hit:
                enemy_hit.do_damage()
                return
        elif self.current_flip == "left":
            enemy_hit = pygame.sprite.spritecollideany(self.collision_wings["west"], active_map.enemies)
            if enemy_hit:
                enemy_hit.do_damage()
                return

        enemy_hit = pygame.sprite.spritecollideany(self.collision_wings["north"], active_map.enemies)
        if enemy_hit:
            enemy_hit.do_damage()
            return
        enemy_hit = pygame.sprite.spritecollideany(self.collision_wings["south"], active_map.enemies)
        if enemy_hit:
            enemy_hit.do_damage()
            return



    def update_enemy_distance(self):
        for enemy in active_map.enemies:
            enemy.within_range = True if Tools.get_distance(self, enemy) else False

            if enemy.within_range and self.x < enemy.x:
                enemy.current_flip = "west"
            elif enemy.within_range and self.x > enemy.x:
                enemy.current_flip = "east"
            elif enemy.within_range and self.x == enemy.x:
                enemy.current_flip = ""

            if enemy.within_range and self.y < enemy.y:
                enemy.player_latitude = "north"
            elif enemy.within_range and self.y > enemy.y:
                enemy.player_latitude = "south"
            elif enemy.within_range and self.y == enemy.y: 
                enemy.player_latitude = ""


    def player_hit_by_projectile(self):
        if (pygame.sprite.spritecollideany(self, demon_burn_column)) != None:
            self.hp -= 0.1
        if any(pygame.sprite.groupcollide(player, active_projectiles, False, True)):
            self.hp -= 1


    def update(self):

        # Updates clocks and cooldowns
        self.sprite_timer += clock.get_time()
        self.movement_timer += clock.get_time()
        self.attack_timer += clock.get_time()
        self.interact_timer += clock.get_time()

        # Only updates sprite if it's off cooldown
        if self.sprite_timer >= SPRITE_RATE:
            self.parse_sprite()
            

        if self.hp != self.max_hp:
            Tools.health_bar(screen, self.hp, self.max_hp, self.rect)

        # Gets the key pressed by the player this frame
        keystate = pygame.key.get_pressed()

        interaction = get_interaction(active_map.current_map, self.x, self.y)
        if interaction:
            interact_hover_text = fool_font.render("Press F to interact", True, (255,255,255))
            screen.blit(interact_hover_text, (self.x - interact_text_width/3, self.y - 30))
            if self.interact_timer >= 400 and keystate[pygame.K_f]:
                self.interact_timer = CLEAR
                active_map.interactions[active_map.name][interaction]()

        # Only moves if movement is off cooldown
        if self.movement_timer >= MOVEMENT_RATE:

            # Updates the collision blocks to make collision tests with the map
            self.collision_wings = {
            "north": Collision_Block(self.x, self.y - active_map.TILEHEIGHT, active_map.TILEWIDTH, active_map.TILEHEIGHT),
            "south": Collision_Block(self.x, self.y + active_map.TILEHEIGHT, active_map.TILEWIDTH, active_map.TILEHEIGHT),
            "east": Collision_Block(self.x + active_map.TILEWIDTH, self.y, active_map.TILEWIDTH, active_map.TILEHEIGHT),
            "west": Collision_Block(self.x - active_map.TILEWIDTH, self.y, active_map.TILEWIDTH, active_map.TILEHEIGHT),
            }

            # The keys D and Right Arrow move the character to the right if it's not colliding with anything and it's not at the edge of screen
            if (keystate[pygame.K_d] or keystate[pygame.K_RIGHT]):
                # Flips the character to the right if he was previously looking left
                if self.current_flip == "left":
                    self.current_flip = "right"
                if self.not_colliding("east") and self.x + active_map.TILEWIDTH < WIDTH:
                    self.x += active_map.TILEWIDTH
                    self.movement_timer = CLEAR
            # The keys A and Left Arrow move the character to the right if it's not colliding with anything and it's not at the edge of screen
            elif (keystate[pygame.K_a] or keystate[pygame.K_LEFT]):
                # Flips the character to the left if he was previously looking right
                if self.current_flip == "right":
                    self.current_flip = "left"
                if self.not_colliding("west") and self.x > 0:
                    self.x -= active_map.TILEWIDTH
                    self.movement_timer = CLEAR
            # The keys S and Down Arrow move the character downwards if it's not colliding with anything and it's not at the edge of screen
            elif (keystate[pygame.K_s] or keystate[pygame.K_DOWN]) and self.y + active_map.TILEHEIGHT < HEIGHT and self.not_colliding("south"):
                self.y += active_map.TILEHEIGHT
                self.movement_timer = CLEAR
            # The keys W and Up Arrow move the character downwards if it's not colliding with anything and it's not at the edge of screen
            elif (keystate[pygame.K_w] or keystate[pygame.K_UP]) and self.y > 0 and self.not_colliding("north"):
                self.y -= active_map.TILEHEIGHT
                self.movement_timer = CLEAR

        # The keys E and Space will start the attack animation if attack is off cooldown
        if (keystate[pygame.K_e] or keystate[pygame.K_SPACE]) and self.attack_timer >= 600:
            self.current_state = self.list_of_states["attack"]
            self.current_frame = self.attack_frame
            self.attack_timer = CLEAR
            self.attack_enemy()

        self.update_enemy_distance()
        self.player_hit_by_projectile()


player = pygame.sprite.Group()
player.add(Player())
