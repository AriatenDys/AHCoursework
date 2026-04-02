import pygame
import os
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, FONT_PATH, IMAGE_PATH

class MenuTemplate:
    def __init__(self):
        self.visible = False

        self.width = int(WINDOW_WIDTH * 0.65)
        self.height = int(WINDOW_HEIGHT * 0.65)

        self.rect = pygame.Rect((WINDOW_WIDTH - self.width)//2, (WINDOW_HEIGHT - self.height)//2, self.width, self.height)

        self.close_button = pygame.Rect(self.rect.right - 40, self.rect.top + 10, 30, 30)

        self.scroll_offset = 0
        self.row_height = 35
        self.max_visible_rows = (self.height - 150)//self.row_height

        self.scroll_up_button = pygame.Rect(self.rect.right - 45, self.rect.top + 70, 30, 30)
        self.scroll_down_button = pygame.Rect(self.rect.right - 45, self.rect.bottom - 50, 30, 30)

        self.up_img = pygame.image.load(os.path.join(IMAGE_PATH, "up.png")).convert_alpha()
        self.down_img = pygame.image.load(os.path.join(IMAGE_PATH, "down.png")).convert_alpha()

        self.up_img = pygame.transform.smoothscale(self.up_img,(22,22))
        self.down_img = pygame.transform.smoothscale(self.down_img,(22,22))

        self.overlay_colour = (0,0,0,160)
        self.bg_colour = (25,25,35)
        self.border_colour = (200,200,220)
        self.text_colour = (235,235,245)
        self.close_colour = (180,60,60)
        self.close_hover_colour = (220,80,80)

        self.title_font_size = 36
        self.body_font_size = 22

        default_font = os.path.join(FONT_PATH,"Ldfcomicsans-jj7l.ttf")

        self.title_font = pygame.font.Font(default_font,self.title_font_size)
        self.body_font = pygame.font.Font(default_font,self.body_font_size)

        self.item_rects = []

    def set_font(self, font_path):
        self.title_font = pygame.font.Font(font_path,self.title_font_size)
        self.body_font = pygame.font.Font(font_path,self.body_font_size)

    def open(self):
        self.visible = True
        self.scroll_offset = 0

    def close(self):
        self.visible = False

    def handle_event(self,event):
        if not self.visible:
            return
        
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.close_button.collidepoint(event.pos):
                self.close()

            elif self.scroll_up_button.collidepoint(event.pos):
                self.scroll_offset = max(0,self.scroll_offset-1)

            elif self.scroll_down_button.collidepoint(event.pos):
                self.scroll_offset += 1

    def draw(self,surface):
        if not self.visible:
            return

        overlay = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT),pygame.SRCALPHA)
        overlay.fill(self.overlay_colour)
        surface.blit(overlay,(0,0))

        pygame.draw.rect(surface,self.bg_colour,self.rect,border_radius=14)
        pygame.draw.rect(surface,self.border_colour,self.rect,2,border_radius=14)

        title_surf = self.title_font.render(self.title,True,self.text_colour)
        title_rect = title_surf.get_rect(midtop=(self.rect.centerx,self.rect.top+20))
        surface.blit(title_surf,title_rect)

        mouse = pygame.mouse.get_pos()

        colour = self.close_hover_colour if self.close_button.collidepoint(mouse) else self.close_colour
        pygame.draw.rect(surface,colour,self.close_button,border_radius=6)

        x_text = self.body_font.render("x",True,(255,255,255))
        surface.blit(x_text,x_text.get_rect(center=self.close_button.center))

        pygame.draw.rect(surface,self.border_colour,self.scroll_up_button,border_radius=6)
        surface.blit(self.up_img,self.up_img.get_rect(center=self.scroll_up_button.center))

        pygame.draw.rect(surface,self.border_colour,self.scroll_down_button,border_radius=6)
        surface.blit(self.down_img,self.down_img.get_rect(center=self.scroll_down_button.center))