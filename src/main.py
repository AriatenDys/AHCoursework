# imports
import sys
try:
    import pygame
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
    import pygame
from physics import physics_setup
from ui import UI
from utils import *
from settings import *                
from user_input_handler import *
from infomenu import StartMenu
from sql_commands import PlanetDB
from self_defined_decorators import log_call
from bodymenu import BodyMenu
from audio_and_font_menu import ChangeAudio, ChangeFont
from controlsmenu import ControlsMenu

class Simulation:
    def __init__(self):
        """class for handling the main running of the simulation"""
        pygame.init()

        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
        width, height = self.display_surface.get_size()
        self.screen_centre = SCREEN_CENTRE 

        # handle fps
        self.clock = pygame.time.Clock()
        self.FPS = 30

        # handle zoom
        self.scale = 1.0 
        self.min_scale = 0.1
        self.max_scale = 5.0
        self.zoom_step = 0.1

        # handle surfaces for the objects and text to be written on
        self.object_surface = pygame.Surface((width, height))
        self.object_surface.set_colorkey((0, 0, 0))
        self.text_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # predefined variables for creating an object
        self.creating_body = False
        self.input_boxes = []
        self.new_body_pos = None

        # ui and keyboard controls visibility
        self.show_ui = True

        # load prechosen song and font, also ensure audio is set to unmute initially
        self.img = "audio.png"
        self.current_font = "Ldfcomicsans-jj7l.ttf"
        self.current_song = "sugar_star_planetarium.mp3"
        self.font = pygame.font.Font(os.path.join(FONT_PATH, self.current_font), 30)
        import_assets(self.current_song)

        # instantiation of classes from other files
        self.ui = UI(self.font) # writes planet positions on the right side
        self.change_audio = ChangeAudio() # creates a button on the left for changing the song
        self.change_font = ChangeFont() # creates a button on the left for changing the font
        self.db = PlanetDB() # allows access to the database within self
        self.start_menu = StartMenu(os.path.join(FONT_PATH, self.current_font)) # allows the info menu to be drawn
        self.body_menu = BodyMenu(self.db) # allows the body menu to be drawn
        self.controls_menu = ControlsMenu(os.path.join(FONT_PATH, self.current_font)) # allows the control menu to be drawn

        # extra variables, check for key press for decorator, set up the physics, and by default turn on the music
        self.key_was_pressed = False
        self.physics = physics_setup(self.db)
        self.audio_on = True
    
    def draw_text(self, text, position, colour=(255, 255, 255)):
        """display text on the screen showing the coordinates of the planets"""
        surf = self.font.render(text, True, colour)
        self.display_surface.blit(surf, surf.get_rect(bottomleft=position))

    def get_preview_value(self, label, default):
        """get value from input box safely for preview rendering"""
        for box in self.input_boxes:
            if hasattr(box, "label") and box.label == label: # check that the label is actually in the box and that the label matches the requested box
                value = box.get_value().strip()
                if value == "":
                    return default # ensure something is there for the user to try see the planet before cration
                try:
                    return float(value)
                except ValueError:
                    return default

        return default
    
    def draw_preview_body(self):
        """preview the body when creating it on screen"""
        if not self.creating_body or not self.new_body_pos: # dont go drawing if not creating or not selected a position
            return

        radius = int(self.get_preview_value("radius", 5)) # check for user input and default 5
        radius = max(1, radius)

        vx = self.get_preview_value("vx", 0) # check for user input and default 0
        vy = self.get_preview_value("vy", 0)

        colour = (255,0,0) # default to red and check the option box for the selected colour
        for box in self.input_boxes:
            if hasattr(box, "get_selected_colour"):
                colour = box.get_selected_colour()

        pos = pygame.Vector2(self.screen_position(self.new_body_pos)) # find the position and scale the radius to the zoom
        scaled_radius = int(radius * self.scale)

        pygame.draw.circle(self.display_surface, colour, pos, scaled_radius, 2)

        arrow_scale = 5 # set up the velocity vector arrow
        velocity_vec = pygame.Vector2(vx, vy) * arrow_scale

        if velocity_vec.length() > 0:
            direction = velocity_vec.normalize() # find  the vector norm, direction of the vector, and draw it at the circle edge
            start = pos + direction * scaled_radius
            end = start + velocity_vec

            pygame.draw.line(self.display_surface, colour, start, end, 2)

            left = end - direction * 10 + pygame.Vector2(-direction.y, direction.x) * 5
            right = end - direction * 10 + pygame.Vector2(direction.y, -direction.x) * 5

            pygame.draw.line(self.display_surface, colour, end, left, 2)
            pygame.draw.line(self.display_surface, colour, end, right, 2)

    @log_call
    def reset_simulation(self):
        """resets the simulation to default - NOTE: DOES NOT CLEAR THE DB"""
        self.object_surface.fill((0, 0, 0)) 
        self.physics.bodies = []
        self.physics = physics_setup(self.db)

    def screen_position(self, pos):
        """takes actual screen coordinates the changes it to make the screen centre (0, 0) and not the top left or wherever it actually is"""
        return int(pos.x*self.scale + self.screen_centre.x), int(pos.y*self.scale + self.screen_centre.y)

    def run(self):
        """the main loop that keeps the simulation running"""
        self.paused = False
        self.running = True

        fade_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.controls_menu.open()

        while self.running:
            key_presses(self)
            self.key_was_pressed = False
            # handle font menu clicks
            if self.change_font.visible:
                mouse_pos = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:  # left click
                    for i, rect in enumerate(self.change_font.item_rects):
                        if rect.collidepoint(mouse_pos):
                            new_font_path = self.change_font.paths[i]
                            self.current_font = new_font_path
                            self.font = pygame.font.Font(new_font_path, 30)
                            self.start_menu.set_font(new_font_path)
                            self.body_menu.set_font(new_font_path)
                            self.change_audio.set_font(new_font_path)
                            self.ui.set_font(self.font)
                            for box in self.input_boxes:
                                box.update_font(new_font_path)
                            self.change_font.close()
                            break

            if not self.paused:
                fade_surface.set_alpha(20)
                fade_surface.fill((0, 0, 0))
                self.physics.integrate()
                self.object_surface.blit(fade_surface, (0, 0))

            for body in self.physics.bodies:
                try:
                    scaled_radius = max(1, int(body.radius * self.scale)) # prevent a 0 pixel circle
                    pygame.draw.circle(self.object_surface, body.colour, self.screen_position(body.position), scaled_radius)
                except TypeError:
                    self.db.delete_planet(body.name)

            self.text_surface.fill((0, 0, 0, 0))
            self.ui.set_bodies(self.physics.bodies)
            if self.show_ui:
                self.ui.ui_draw(self.text_surface)

            self.display_surface.fill((0, 0, 0))
            self.display_surface.blit(self.object_surface, (0, 0))
            self.display_surface.blit(self.text_surface, (0, 0))

            if self.creating_body:
                self.draw_preview_body()
                for box in self.input_boxes:
                    box.draw(self.display_surface)

            if self.show_ui:
                self.ui.audio_draw(self.display_surface, self.img)
                self.ui.music_draw(self.display_surface)
                self.ui.font_draw(self.display_surface)
                self.draw_text("press 'i' for info", (10, WINDOW_HEIGHT - 100))
                self.draw_text(f"fps: {self.FPS} | paused: {self.paused} | zoom: {self.scale:f}", (10, WINDOW_HEIGHT - 10))
                self.draw_text("press 'c' to view the controls", (10, WINDOW_HEIGHT - 50))

            self.start_menu.draw(self.display_surface)
            self.body_menu.draw(self.display_surface)
            self.change_audio.draw(self.display_surface)
            self.change_font.draw(self.display_surface)
            self.controls_menu.draw(self.display_surface)

            pygame.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    simulation = Simulation()
    simulation.run()
