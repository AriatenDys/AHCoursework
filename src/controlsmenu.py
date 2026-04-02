# imports
import pygame
from settings import *
import os

class ControlsMenu:
    def __init__(self, font_path):
        """menu that shows the keyboard controls overlay"""
        self.visible = False

        self.width = int(WINDOW_WIDTH * 0.65)
        self.height = int(WINDOW_HEIGHT * 0.65)

        self.rect = pygame.Rect((WINDOW_WIDTH - self.width) // 2,(WINDOW_HEIGHT - self.height) // 2,self.width,self.height)

        self.close_button = pygame.Rect(self.rect.right - 40, self.rect.top + 10, 30, 30)

        self.overlay_colour = (0,0,0,160)
        self.bg_colour = (25,25,35)
        self.border_colour = (200,200,220)
        self.text_colour = (235,235,245)

        self.close_colour = (180,60,60)
        self.close_hover_colour = (220,80,80)

        self.title = "controls"

        self.title_font = pygame.font.Font(font_path, 36)
        self.body_font = pygame.font.Font(font_path, 22)

        self.controls_img = pygame.image.load(os.path.join(IMAGE_PATH, "keyboard.png")).convert_alpha()

        scale = 0.6
        w, h = self.controls_img.get_size()

        self.controls_img = pygame.transform.scale(self.controls_img,(int(w * scale), int(h * scale)))

    def open(self):
        self.visible = True

    def close(self):
        self.visible = False

    def set_font(self, font_path):
        self.title_font = pygame.font.Font(font_path, 36)
        self.body_font = pygame.font.Font(font_path, 22)

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.close_button.collidepoint(event.pos):
                    self.close()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()

    def draw(self, surface):
        if not self.visible:
            return

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(self.overlay_colour)

        surface.blit(overlay, (0,0))

        pygame.draw.rect(surface, self.bg_colour, self.rect, border_radius=14)
        pygame.draw.rect(surface, self.border_colour, self.rect, 2, border_radius=14)

        title_surf = self.title_font.render(self.title, True, self.text_colour)
        title_rect = title_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))

        surface.blit(title_surf, title_rect)
        img_rect = self.controls_img.get_rect(center=self.rect.center)
        surface.blit(self.controls_img, img_rect)

        mouse_pos = pygame.mouse.get_pos()
        colour = (self.close_hover_colour if self.close_button.collidepoint(mouse_pos) else self.close_colour)

        pygame.draw.rect(surface, colour, self.close_button, border_radius=6)
        x_text = self.body_font.render("x", True, (255,255,255))
        surface.blit(x_text, x_text.get_rect(center=self.close_button.center))