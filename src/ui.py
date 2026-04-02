# imports
import pygame
import os
from settings import *
from self_defined_decorators import log_call

class UI:
    def __init__(self, font):
        """class for displaying the UI to the user"""
        self.display_surface = pygame.display.get_surface()
        self.font = font

        self.padding = 10
        self.line_height = font.get_height() + 4
        self.text_colour = (255, 255, 255)

        self.bodies = []

    def set_bodies(self, bodies):
        """update the list if changed"""
        self.bodies = bodies

    def set_font(self, new_font):
        """update the font if changed"""
        self.font = new_font
        self.line_height = self.font.get_height() + 4

    @log_call
    def ui_draw(self, surface):
        """display on screen the name and position of bodies"""
        x = surface.get_width() - self.padding
        y = surface.get_height() - self.padding

        for body in reversed(self.bodies):
            name = getattr(body, "name", "body")
            px = body.position.x 
            py = body.position.y
            text = f"{name}: ({px:.1f}, {py:.1f})"
            text_surf = self.font.render(text, True, self.text_colour)
            text_rect = text_surf.get_rect(bottomright=(x, y))
            surface.blit(text_surf, text_rect)
            y -= self.line_height

    @log_call
    def audio_draw(self, surface, img_file=None):
        """display the button for muting"""
        x = self.padding
        y = self.padding

        erase_rect = pygame.Rect(x, y+464, 62, 52)
        pygame.draw.rect(surface, (0,0,0), erase_rect)

        if img_file:
            img_file = img_file
        else:
            img_file = "audio.png"
        self.audio_img = pygame.image.load(os.path.join(IMAGE_PATH, img_file)).convert_alpha()
        self.audio_img = pygame.transform.smoothscale(self.audio_img, (62, 62))
        self.audio_rect = self.audio_img.get_rect(midleft=(x, y+490))
        surface.blit(self.audio_img, self.audio_rect)
            
    @log_call 
    def music_draw(self, surface):
        """display button for changing audio"""
        x = self.padding 
        y = self.padding 

        self.music_img = pygame.image.load(os.path.join(IMAGE_PATH, "music.png")).convert_alpha()
        self.music_img = pygame.transform.smoothscale(self.music_img, (62, 52))
        self.music_rect = self.music_img.get_rect(midleft=(x, y+550))
        surface.blit(self.music_img, self.music_rect)

    @log_call 
    def font_draw(self, surface):
        """display button for changing font"""
        x = self.padding 
        y = self.padding 
        
        self.font_img = pygame.image.load(os.path.join(IMAGE_PATH, "font.png")).convert_alpha()
        self.font_img = pygame.transform.smoothscale(self.font_img, (62, 52))
        self.font_rect = self.font_img.get_rect(midleft=(x, y+610))
        surface.blit(self.font_img, self.font_rect)
