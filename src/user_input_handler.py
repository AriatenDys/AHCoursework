# imports
import pygame
from input_box import *
from settings import *
from infomenu import *
from create_bodies import create_body_from_input
from self_defined_decorators import log_key_press
from audio_and_font_menu import toggle_audio
from option_box import OptionBox

@log_key_press
def key_presses(self):
    """function to handle user inputs"""
    for event in pygame.event.get():
        # ensure control menu is at the top of the hierarchy
        if self.controls_menu.visible:
            self.controls_menu.handle_event(event)
            continue  # nothing else runs

        # body creation is the second in the hierarchy, and stops everything else but the control menu
        if self.creating_body:

            # allow quitting
            if event.type == pygame.QUIT:
                self.running = False

            # allow cancelling body creation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.creating_body = False
                    self.paused = False
                    continue

                if event.key == pygame.K_c:
                    self.controls_menu.open()
                    continue

            # normal input box handling 
            for box in self.input_boxes:
                if isinstance(box, OptionBox):
                    box.update([event])
                else:
                    box.handle_event(event)

            # confirm creation
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                create_body_from_input(self)

            continue # skip menus / world interaction

        # if any menu is open then the rest of the events cannot happen
        menu_was_open = self.start_menu.visible
        mass_menu_was_open = self.body_menu.visible
        audio_menu_was_open = self.change_audio.visible
        font_menu_was_open = self.change_font.visible

        self.start_menu.handle_event(event)
        self.body_menu.handle_event(event)
        self.change_audio.handle_event(event)
        self.change_font.handle_event(event, self)

        if menu_was_open or mass_menu_was_open or audio_menu_was_open or font_menu_was_open:
            continue

        # bottom of the hierarchy is the keyboard and mouse contorls
        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.KEYDOWN:
            self.key_was_pressed = True
            match event.key: # key handling for things like zoom, fps, menus, resets, etc
                case pygame.K_ESCAPE:
                    self.running = False
                case pygame.K_SPACE:
                    self.paused = not self.paused
                case pygame.K_UP:
                    if self.FPS < 240:
                        self.FPS += 5
                case pygame.K_DOWN:
                    if self.FPS > 5:
                        self.FPS -= 5
                case pygame.K_i:
                    self.start_menu.open()
                case pygame.K_DELETE:
                    self.db.delete_all_planets(self.physics)
                    self.reset_simulation()
                case pygame.K_r:
                    self.reset_simulation()
                case pygame.K_EQUALS | pygame.K_PLUS:
                    if self.scale <= self.max_scale-0.1:
                        self.scale += self.zoom_step
                        self.object_surface.fill((0, 0, 0))
                case pygame.K_MINUS | pygame.K_UNDERSCORE:
                    if self.scale >= self.min_scale+0.1:
                        self.scale -= self.zoom_step
                        self.object_surface.fill((0, 0, 0))
                case pygame.K_m:
                    self.body_menu.open()
                case pygame.K_u:
                    self.show_ui = not self.show_ui
                case pygame.K_c:
                    self.controls_menu.open()

        if event.type == pygame.MOUSEBUTTONDOWN:
            match event.pos: # check for user clicking buttons
                case pos if self.ui.audio_rect.collidepoint(pos):
                    self.audio_on, self.img = toggle_audio(self.audio_on)
                    return
                case pos if self.ui.music_rect.collidepoint(pos):
                    self.change_audio.open()
                    return
                case pos if self.ui.font_rect.collidepoint(pos):
                    self.change_font.open()
                    return

        # creating a new body
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos # get position
            wx = round((mx - self.screen_centre.x) / self.scale, 2)
            wy = round((my - self.screen_centre.y) / self.scale, 2)

            self.new_body_pos = R2Vector(x=wx, y=wy)
            self.creating_body = True
            self.paused = True

            self.input_boxes = [ # create input boxes on screen
                InputBox(50, 50, 200, 32, "name", os.path.join(FONT_PATH, self.current_font)),
                InputBox(50, 100, 200, 32, "mass", os.path.join(FONT_PATH, self.current_font)),
                InputBox(50, 150, 200, 32, "vx", os.path.join(FONT_PATH, self.current_font)),
                InputBox(50, 200, 200, 32, "vy", os.path.join(FONT_PATH, self.current_font)),
                InputBox(50, 250, 200, 32, "radius", os.path.join(FONT_PATH, self.current_font)),
                OptionBox(50,300, 200, 32, (200, 200, 200), "colour", font_path=os.path.join(FONT_PATH, self.current_font))
            ]