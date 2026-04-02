# imports
import pygame
from settings import colours, COLOUR_INACTIVE

class OptionBox:
    def __init__(self, x:int, y:int, w:int, h:int, highlight_color:str, label:str, font_path=None, font_size=20, selected=0):
        """class for creating the option box for colours, modified by something on stack overflow"""
        self.rect = pygame.Rect(x, y, w, h)
        self.highlight_color = highlight_color
        self.option_list = list(colours.keys())
        self.colour_list = [self.str_to_rgb(colours[name]) for name in self.option_list]
        self.selected = selected
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1
        self.label = label
        self.error = None
        self.color = COLOUR_INACTIVE

        # font setup
        self.font_path = font_path
        self.font_size = font_size
        self.font = pygame.font.Font(self.font_path, self.font_size) if self.font_path else pygame.font.SysFont(None, self.font_size)

    def str_to_rgb(self, s):
        """convert '(r, g, b)' string to tuple"""
        return tuple(map(int, s.strip("()").split(",")))

    def clear_error(self):
        """remove the error from the box"""
        self.error = None

    def update_font(self, font_path):
        """change font when user requests"""
        self.font_path = font_path
        self.font = pygame.font.Font(self.font_path, self.font_size)
        
    def draw(self, screen):
        """draw the option box on screen and when requested the options inside"""
        # label
        label_surf = self.font.render(self.label, True, (200,200,200))
        screen.blit(label_surf, (self.rect.x, self.rect.y - 25))

        # main selected colour
        current_colour = self.colour_list[self.selected]
        pygame.draw.rect(screen, current_colour, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # dropdown menu
        if self.draw_menu:
            for i, colour_rgb in enumerate(self.colour_list):
                rect = self.rect.copy()
                rect.y += (i + 1) * self.rect.height

                pygame.draw.rect(screen, self.highlight_color if i == self.active_option else colour_rgb, rect)

                pygame.draw.rect(screen, (0,0,0), rect, 2)

                text = self.font.render(self.option_list[i], True, (0,0,0))
                screen.blit(text, (rect.x + 5, rect.y + 5))

        # error display
        if self.error:
            err_surf = self.font.render(self.error, True, (255,80,80))
            err_rect = err_surf.get_rect(midleft=(self.rect.right + 10, self.rect.centery))
            screen.blit(err_surf, err_rect)

    def update(self, event_list):
        """when the user selects an option update the box to show that option"""
        mpos = pygame.mouse.get_pos()
        self.menu_active = self.rect.collidepoint(mpos)

        # determine which option is hovered
        self.active_option = -1
        for i in range(len(self.option_list)):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if rect.collidepoint(mpos):
                self.active_option = i
                break

        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

        # handle mouse clicks
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.menu_active:
                    self.draw_menu = not self.draw_menu
                elif self.draw_menu and self.active_option >= 0:
                    self.selected = self.active_option
                    self.draw_menu = False
                    return self.selected
        return -1

    def get_selected_colour(self):
        """returns (r, g, b) tuple of selected colour"""
        return self.colour_list[self.selected]