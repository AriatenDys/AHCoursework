# imports
import pygame
import os
from settings import FONT_PATH
from menu_template import MenuTemplate

class BodyMenu(MenuTemplate):
    def __init__(self, db):
        """constructor for the body menu class"""
        super().__init__()
        self.db = db
        self.planets = []

        self.row_height = 26
        self.max_visible_rows = (self.height - 170)//self.row_height
        self.highlight_colour = (255,255,120)
        self.body_font = pygame.font.Font(os.path.join(FONT_PATH, "Ldfcomicsans-jj7l.ttf"), 18)
        self.columns = [
            ("name",110), ("mass",110), ("px",80), ("py",80),
            ("vx",80), ("vy",80), ("radius",80),
            ("colour_r",70), ("colour_g",70), ("colour_b",70)
        ]

        self.title = "your planets"

    # ---------- display handling ----------

    def set_font(self, font_path):
        """sets the font for the body menu"""
        super().set_font(font_path)
        self.body_font = pygame.font.Font(font_path,18)

    def load_planets(self):
        """opens the database and reads the planets stored"""
        self.planets = []
        for p in self.db.get_all_planets():
            self.planets.append({
                "name": p["name"],
                "mass": p["mass"],
                "px": p["position"].x,
                "py": p["position"].y,
                "vx": p["velocity"].x,
                "vy": p["velocity"].y,
                "radius": p["radius"],
                "colour_r": p["colour"][0],
                "colour_g": p["colour"][1],
                "colour_b": p["colour"][2],
                "_old_name": p["name"]
            })

    def open(self):
        """displays the body menu"""
        super().open()
        self.load_planets()

    # ---------- event handling ----------

    def handle_event(self, event):
        """handles mouse clicking to close the menu or scroll the menu"""
        super().handle_event(event)


    # ---------- drawing ----------

    def draw(self, surface):
        """draws the body menu"""
        super().draw(surface)

        if not self.visible:
            return

        # redraw title position for content spacing
        title = self.title_font.render(self.title, True, self.text_colour)
        title_rect = title.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))

        total_width = sum(width for _, width in self.columns)
        x_start = self.rect.left + (self.width - total_width)//2
        y_start = title_rect.bottom + 30

        # column headers
        x = x_start
        for name, width in self.columns:
            text = self.body_font.render(name, True, self.highlight_colour)
            surface.blit(text,(x+3,y_start))
            x += width
        y_start += 30

        # rows
        for r in range(self.max_visible_rows):
            real_row = r + self.scroll_offset
            if real_row >= len(self.planets):
                break
            x = x_start
            y = y_start + r*self.row_height
            for col, width in self.columns:
                cell = pygame.Rect(x,y,width,self.row_height)
                pygame.draw.rect(surface,self.border_colour,cell,1)
                text_value = str(self.planets[real_row][col])
                text = self.body_font.render(text_value,True,self.text_colour)
                surface.blit(text,(x+3,y+3))
                x += width