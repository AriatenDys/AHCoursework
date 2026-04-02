# imports
import pygame
from settings import *
from body import *
import os

class InputBox:
    def __init__(self, x: float, y: float, w: float, h: float, label: str, font_path=None, font_size=20):
        """constructor for the input box class"""
        self.rect = pygame.Rect(x, y, w, h)
        self.label = label
        self.text = " "
        self.active = False
        self.error = None

        # check for user selected font, otherwise default to comic sans
        self.font_path = os.path.join(FONT_PATH, "Ldfcomicsans-jj7l.ttf")
        if font_path:
            self.font_path = font_path
        self.font_size = font_size
        self.font = pygame.font.Font(self.font_path, self.font_size)

        self.typing = False
        self.color = COLOUR_INACTIVE
        self.txt_surface = self.font.render("", True, self.color)

    # ---------- event handling ----------
    
    def clear_error(self):
        """remove any displayed error on the boxes"""
        self.error = None

    def get_value(self):
        """return the text inside the box"""
        return self.text

    def handle_event(self, event):
        """handle user events on input boxes"""
        self.typing = False
        if event.type == pygame.MOUSEBUTTONDOWN: # check for box being clicked
            self.active = self.rect.collidepoint(event.pos)
            self.color = COLOUR_ACTIVE if self.active else COLOUR_INACTIVE

        if event.type == pygame.KEYDOWN and self.active: # type or delete user input
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.typing = True
            else:
                self.text += event.unicode

            # display what the user tped
            self.txt_surface = self.font.render(self.text, True, self.color)

    # ---------- display handling ----------

    def update_font(self, font_path):
        self.font_path = font_path
        self.font = pygame.font.Font(self.font_path, self.font_size)
    
    def draw(self, screen):
        """method for drawing the input boxes"""
        label_surf = self.font.render(self.label, True, (200, 200, 200))
        screen.blit(label_surf, (self.rect.x, self.rect.y - 25))

        text_rect = self.txt_surface.get_rect()
        text_rect.topleft = (self.rect.x + 5, self.rect.y + 5)

        clip_rect = self.rect.inflate(-10, -10)
        screen.set_clip(clip_rect)
        screen.blit(self.txt_surface, text_rect)
        screen.set_clip(None)

        pygame.draw.rect(screen, self.color, self.rect, 2)

        if not self.typing:
            pass

        if self.error:
            err_surf = self.font.render(self.error, True, (255, 80, 80))
            err_rect = err_surf.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
            screen.blit(err_surf, err_rect)
