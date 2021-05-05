import pygame
from settings import clock, path, audio_folder, start_screen_folder, audio_folder, screen, WIDTH, HEIGHT
from os import listdir

pygame.mixer.music.load(path.join(audio_folder, "Soliloquy.ogg"))

class StartScreen():
    def __init__(self):
        self.velocity_changed = False
        self.opacity = 1
        self.images = [
            {"image": pygame.image.load(path.join(start_screen_folder, "parallax-demon-woods-bg.png")),                                            "x": 0,      "y": 0,   "movement":  0},
            {"image": pygame.image.load(path.join(start_screen_folder, "parallax-demon-woods-far-trees.png")),                                     "x": 0,      "y": 0,   "movement": 2},
            {"image": pygame.image.load(path.join(start_screen_folder, "parallax-demon-woods-mid-trees.png")),                                     "x": 0,      "y": 0,   "movement": 12},
            {"image": list(pygame.image.load(path.join(start_screen_folder, "hero", f)) for f in listdir(path.join(start_screen_folder, "hero"))), "x": -300,   "y": 635, "movement":  0},
            {"image": pygame.image.load(path.join(start_screen_folder, "parallax-demon-woods-close-trees.png")),                                   "x": 0,      "y": 0,   "movement": 22},
        ]
        self.menu_title_str = pygame.image.load(path.join(start_screen_folder, "menu_title.png"))
        self.menu_subtitle_str = pygame.image.load(path.join(start_screen_folder, "subtitle_menu.png"))
        self.start_str = pygame.image.load(path.join(start_screen_folder, "start_menu.png"))

        self.curtain = pygame.Surface((WIDTH, HEIGHT))
        self.curtain.fill((0,0,0))

        self.current_sprite = 0


        self.opacity_bg = 6000
        self.title_opacity_bg = 0
        self.subtitle_opacity_bg = 0

        self.confirm_sound = pygame.mixer.Sound(path.join(audio_folder, "menu_confirm.wav"))

    def draw_menu(self):
        for layer in self.images:
            if type(layer["image"]) is list:
                screen.blit(layer["image"][self.current_sprite], (layer["x"], layer["y"]))
                self.current_sprite = (self.current_sprite+1) % 7
            else:
                screen.blit(layer["image"], (layer["x"], layer["y"]))
                screen.blit(layer["image"], (layer["x"]-2229, layer["y"]))
                layer['x'] = (layer['x']-layer["movement"])%2229
            
        if pygame.time.get_ticks() >= 6000 and self.images[3]["x"] < 160:
                self.images[3]["x"] += 8

        if self.images[3]["x"] >= 160 and not self.velocity_changed:
            self.images[1]["movement"] += 8
            self.images[2]["movement"] += 8
            self.images[4]["movement"] += 8
            self.velocity_changed = True

        if pygame.time.get_ticks() < 2000:
            screen.blit(self.curtain, (0,0))
        elif pygame.time.get_ticks() < 8000:
            self.curtain.set_alpha((self.opacity_bg/6000)*255)
            screen.blit(self.curtain, (0,0))
            self.opacity_bg -= clock.get_time()

        if pygame.time.get_ticks() >= 8000:
            screen.blit(self.menu_title_str, (0,0))
        elif pygame.time.get_ticks() >= 6000:
            self.menu_title_str.set_alpha((self.title_opacity_bg/2000)*255, pygame.RLEACCEL)
            screen.blit(self.menu_title_str, (0,0))
            if self.title_opacity_bg < 4000:
                self.title_opacity_bg += clock.get_time()
            elif self.title_opacity_bg > 4000:
                self.title_opacity_bg = 4000

        if pygame.time.get_ticks() >= 11000:
            screen.blit(self.menu_subtitle_str, (0,0))
        elif pygame.time.get_ticks() >= 9000:
            self.menu_subtitle_str.set_alpha((self.subtitle_opacity_bg/2000)*255, pygame.RLEACCEL)
            screen.blit(self.menu_subtitle_str, (0,0))
            if self.subtitle_opacity_bg < 4000:
                self.subtitle_opacity_bg += clock.get_time()
            elif self.subtitle_opacity_bg > 4000:
                self.subtitle_opacity_bg = 4000

        if pygame.time.get_ticks() >= 14000:
            if int(pygame.time.get_ticks()/1000)%2 == 0:
                screen.blit(self.start_str, (0,0))

    def fade_out(self):
        self.opacity_bg += clock.get_time()
        self.curtain.set_alpha((self.opacity_bg/3000)*255)
        screen.blit(self.curtain, (0,0))

current_start_screen = StartScreen()