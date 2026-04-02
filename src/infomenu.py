# imports
import pygame
from settings import *
import os


class StartMenu:
    def __init__(self, font=None):
        """constructor for the start menu class"""
        self.visible = False
        self.controls_visible = False

        self.width = int(WINDOW_WIDTH * 0.65)
        self.height = int(WINDOW_HEIGHT * 0.65)
        self.rect = pygame.Rect((WINDOW_WIDTH - self.width) // 2, (WINDOW_HEIGHT - self.height) // 2, self.width, self.height)
        self.close_button = pygame.Rect(self.rect.right - 40, self.rect.top + 10, 30, 30)
        self.next_button = pygame.Rect(self.rect.right - 110, self.rect.bottom - 50, 90, 30)
        self.prev_button = pygame.Rect(self.rect.left + 20, self.rect.bottom - 50, 90, 30)

        self.overlay_colour = (0, 0, 0, 160)
        self.bg_colour = (25, 25, 35)
        self.border_colour = (200, 200, 220)
        self.text_colour = (235, 235, 245)
        self.close_colour = (180, 60, 60)
        self.close_hover_colour = (220, 80, 80)

        self.current_font = os.path.join(FONT_PATH, "Ldfcomicsans-jj7l.ttf") # setup for dynamic font, or default to comic sans
        self.title_font_size = 36
        self.body_font_size = 22

        self.title_font = pygame.font.Font(self.current_font, self.title_font_size)
        self.body_font = pygame.font.Font(self.current_font, self.body_font_size)

        # load images and scale appropriately to fit on the screen
        self.example_body_img = pygame.image.load(os.path.join(IMAGE_PATH, "exampleBody.png")).convert_alpha()
        w = self.example_body_img.get_width()
        h = self.example_body_img.get_height()
        
        scale = 0.6
        new_size = (int(w * scale), int(h * scale))
        self.example_body_img = pygame.transform.scale(self.example_body_img, new_size)

        second_scale = 0.4
        self.example_orbit_img = pygame.image.load(os.path.join(IMAGE_PATH, "exampleOrbit.png")).convert_alpha()
        w, h = self.example_orbit_img.get_size()
        self.example_orbit_img = pygame.transform.scale(self.example_orbit_img, (int(w * second_scale), int(h * second_scale)))

        self.dropdownColours_img = pygame.image.load(os.path.join(IMAGE_PATH, "dropdownColours.png")).convert_alpha()
        w, h = self.dropdownColours_img.get_size()
        self.dropdownColours_img = pygame.transform.scale(self.dropdownColours_img, (int(w * scale), int(h * scale)))

        self.controls_img = pygame.image.load(os.path.join(IMAGE_PATH, "keyboard.png")).convert_alpha()
        w, h = self.controls_img.get_size()
        self.controls_img = pygame.transform.scale(self.controls_img, (int(w * scale), int(h * scale)))

        self.title = "how this simulation works"
        self.latex_cache = {}

        self.pages = [
        [
        ""
        ],
        [
        "this simulation aims to create a 2D solar system using pygame",
        "to pause the simulation press \"SPACE\"",
        "press \"UP ARROW\" or \"DOWN ARROW\" to speed up or slow down the simulation respectively",
        "press \"PLUS\" to zoom in and \"MINUS\" to zoom out",
        "press \"R\" to reset the planets"
        ],
        [
        "click anywhere on the screen to create a planet",
        "to quit creating a body press \"Q\"",
        "you must enter:",
        "name, mass, velocity x, velocity y, radius, rgb colour",
        "the planet will be created at the position you clicked on the screen",
        "typical values:",
        "mass: 5-30",
        "radius: 5-30",
        "velocity: 0-20",
        "An example input would look like this:",
        ],
        [
        "buttons on the left:",
        "1. mute audio",
        "2. change music",
        "3. change font",
        "",
        "press DELETE to clear the database",
        "",
        "by pressing \"M\" you can open a menu containing planet information",
        "it shows you what the database stores on your object",
        "which includes all the data you gave to create it, alongside where you clicked to create the planet",
        "the cells cannot be modified, they are just for viewing purposes"
        ],
        [
        "when creating a body, you will be asked to choose a colour",
        "when you click on the box for the colour, a drop down menu will open",
        "this drop down menu contains a list of colours you may choose from to colour your planet",
        "despite black being an option, do be careful that it is not visible very well due to the background also being black",
        "the drop down menu looks like this:"
        ],
        [
        "you are free to create an object however and wherever you like",
        "however",
        "take care to note that if your object doesnt agree with the physics, it may be slingshot by the sun",
        "this means your object will be fired away at a rapid speed",
        "recommendation is to keep one velocity component zero, and the other velocity a small number",
        "for example, placing to above and the left of the sun",
        "",
        "if you have an x component, it will fly towards the sun due to its pull",
        "this will result in a slingshot to fire it away",
        "however a positive y component will send it underneath the sun and its pull will wrap it around to create an orbit",
        "",
        "if you place directly beside the sun at either side,",
        "keep the component that its lined with the sun in at zero to help stabalise the orbit",
        "the further away you are, the smaller the speed should be to maintain orbit",
        "if you are close, you should have a bigger number",
        "do note that \"big\" can refer to numbers of ~10 in one component, whereas \"small\" can mean ~2"
        ],
        [
        "congratulations! you are now ready to start using the simulation",
        "you are welcome to play around and use whatever numbers on planets as you want",
        "be aware that once a planet is created theres no deleting just that planet, youll have to clear the whole collection"
        ]
        ]

        self.current_page = 0

    # ---------- visibility control ----------

    def open(self):
        """allow the start menu to be drawn in main"""
        self.visible = True

    def close(self):
        """dont allow the start menu to be drawn in main"""
        self.visible = False

    # ---------- event handling ----------

    def handle_event(self, event):
        """handle close button on start menu"""
        if not self.visible:
            return
        
        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                if self.close_button.collidepoint(event.pos):
                    self.close()
                    self.current_page = 0

                elif self.next_button.collidepoint(event.pos):
                    if self.current_page < len(self.pages) - 1:
                        self.current_page += 1

                elif self.prev_button.collidepoint(event.pos):
                    if self.current_page > 0:
                        self.current_page -= 1
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if self.current_page < len(self.pages) - 1:
                    self.current_page += 1

            elif event.key == pygame.K_LEFT:
                if self.current_page > 0:
                    self.current_page -= 1

    # ---------- drawing ----------

    def set_font(self, font_path):
        """set up for dynamic font"""
        self.current_font = font_path
        self.title_font = pygame.font.Font(self.current_font, self.title_font_size)
        self.body_font = pygame.font.Font(self.current_font, self.body_font_size)

    def draw(self, surface):
        """steps to draw the start menu"""
        if not self.visible:
            return

        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(self.overlay_colour)
        surface.blit(overlay, (0, 0))

        pygame.draw.rect(surface, self.bg_colour, self.rect, border_radius=14)
        pygame.draw.rect(surface, self.border_colour, self.rect, 2, border_radius=14)

        title_surf = self.title_font.render(self.title, True, self.text_colour)
        title_rect = title_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + 20))
        surface.blit(title_surf, title_rect)

        y = title_rect.bottom + 30
        for line in self.pages[self.current_page]:
            if isinstance(line, str) and "\\" in line: # making sure its a string and its latex before converting to an image
                eq_surface = self.render_latex(line)
                eq_rect = eq_surface.get_rect(midtop=(self.rect.centerx, y))
                surface.blit(eq_surface, eq_rect)
                y += eq_surface.get_height() + 10
            else:
                text_surf = self.body_font.render(line, True, self.text_colour)
                text_rect = text_surf.get_rect(midtop=(self.rect.centerx, y))
                surface.blit(text_surf, text_rect)
                y += 28

        # close button, including hover
        mouse_pos = pygame.mouse.get_pos()
        colour = (self.close_hover_colour if self.close_button.collidepoint(mouse_pos) else self.close_colour)
        pygame.draw.rect(surface, colour, self.close_button, border_radius=6)
        x_text = self.body_font.render("x", True, (255, 255, 255))
        x_rect = x_text.get_rect(center=self.close_button.center)
        surface.blit(x_text, x_rect)

        # next and previous page buttons
        page_text = f"page {self.current_page + 1}/{len(self.pages)}"

        # first page
        if self.current_page == 0:
            img_rect = self.controls_img.get_rect(center=(self.rect.centerx, self.rect.centery))
            surface.blit(self.controls_img, img_rect)

            next_text = self.body_font.render("next", True, (255,255,255))
            pygame.draw.rect(surface, (80,80,120), self.next_button, border_radius=6)
            surface.blit(next_text, next_text.get_rect(center=self.next_button.center))
        
        elif self.current_page == 1:
            img_rect = self.example_orbit_img.get_rect()
            img_rect.midleft = (self.rect.left + 10 + img_rect.width // 2, self.rect.top + 450)
            surface.blit(self.example_orbit_img, img_rect)

            next_text = self.body_font.render("next", True, (255,255,255))
            prev_text = self.body_font.render("back", True, (255,255,255))

            pygame.draw.rect(surface, (80,80,120), self.next_button, border_radius=6)
            pygame.draw.rect(surface, (80,80,120), self.prev_button, border_radius=6)

            surface.blit(next_text, next_text.get_rect(center=self.next_button.center))
            surface.blit(prev_text, prev_text.get_rect(center=self.prev_button.center))

        elif self.current_page == 2:
            img_rect = self.example_body_img.get_rect(center=(self.rect.centerx, self.rect.bottom - 200))
            surface.blit(self.example_body_img, img_rect)

            next_text = self.body_font.render("next", True, (255,255,255))
            prev_text = self.body_font.render("back", True, (255,255,255))

            pygame.draw.rect(surface, (80,80,120), self.next_button, border_radius=6)
            pygame.draw.rect(surface, (80,80,120), self.prev_button, border_radius=6)

            surface.blit(next_text, next_text.get_rect(center=self.next_button.center))
            surface.blit(prev_text, prev_text.get_rect(center=self.prev_button.center))

        elif self.current_page == 4:
            img_rect = self.dropdownColours_img.get_rect(center=(self.rect.centerx, self.rect.bottom - 250))
            surface.blit(self.dropdownColours_img, img_rect)

            next_text = self.body_font.render("next", True, (255,255,255))
            prev_text = self.body_font.render("back", True, (255,255,255))

            pygame.draw.rect(surface, (80,80,120), self.next_button, border_radius=6)
            pygame.draw.rect(surface, (80,80,120), self.prev_button, border_radius=6)

            surface.blit(next_text, next_text.get_rect(center=self.next_button.center))
            surface.blit(prev_text, prev_text.get_rect(center=self.prev_button.center))

        # middle pages
        elif 0 < self.current_page < len(self.pages) - 1:
            next_text = self.body_font.render("next", True, (255,255,255))
            prev_text = self.body_font.render("back", True, (255,255,255))

            pygame.draw.rect(surface, (80,80,120), self.next_button, border_radius=6)
            pygame.draw.rect(surface, (80,80,120), self.prev_button, border_radius=6)

            surface.blit(next_text, next_text.get_rect(center=self.next_button.center))
            surface.blit(prev_text, prev_text.get_rect(center=self.prev_button.center))

        # last page
        else:
            prev_text = self.body_font.render("back", True, (255,255,255))
            pygame.draw.rect(surface, (80,80,120), self.prev_button, border_radius=6)
            surface.blit(prev_text, prev_text.get_rect(center=self.prev_button.center))

        page_num = self.body_font.render(page_text, True, (255,255,255))
        surface.blit(page_num, page_num.get_rect(center=(self.rect.centerx, self.rect.bottom - 35)))
