# imports
import pygame
from settings import FONT_PATH, AUDIO_PATH
from menu_template import MenuTemplate
import os

def toggle_audio(audio_on):
    """mute or play the audio when the user presses the button"""
    audio_on = not audio_on
    if audio_on:
        pygame.mixer.music.set_volume(0.5)
        img = "audio.png"
    else:
        pygame.mixer.music.set_volume(0)
        img = "muted.png"
    return audio_on, img

class ChangeAudio(MenuTemplate):
    def __init__(self):
        """class for changing the audio of the simulation"""
        super().__init__()

        self.title = "select music"

        self.songs = []
        self.paths = []

    def load_songs(self):
        """load the songs from graphics"""
        self.songs.clear()
        self.paths.clear()

        for file in os.listdir(AUDIO_PATH):

            if file.lower().endswith((".mp3",".wav")):

                self.songs.append(file)
                self.paths.append(os.path.join(AUDIO_PATH,file))

    def open(self):
        """open the menu and show the songs"""
        super().open()

        self.load_songs()

    def handle_event(self,event):
        """handle events for the audio menu"""
        super().handle_event(event)

        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i,rect in enumerate(self.item_rects):
                if rect.collidepoint(event.pos): # check if the user click any item inside the array and try to play it
                    path = self.paths[self.scroll_offset+i]
                    try:
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(path)
                        pygame.mixer.music.play(-1)

                        print(path)

                        self.close()
                    except pygame.error as e:
                        print(f"could not load {path}: {e}")

    def draw(self,surface):
        super().draw(surface)

        if not self.visible:
            return

        y = self.rect.top + 100
        self.item_rects.clear()

        visible = self.songs[self.scroll_offset:self.scroll_offset+self.max_visible_rows]

        mouse = pygame.mouse.get_pos()

        for song in visible:
            text = self.body_font.render(song,True,self.text_colour)
            rect = text.get_rect(topleft=(self.rect.x+40,y))
            if rect.collidepoint(mouse):
                pygame.draw.rect(surface,(80,80,120),rect.inflate(10,6))
            surface.blit(text,rect)
            self.item_rects.append(rect)
            y += self.row_height

class ChangeFont(MenuTemplate):
    def __init__(self):
        super().__init__()
        
        self.title = "select font"

        self.fonts = []
        self.paths = []

    def load_fonts(self):
        """reads the folder containing the fonts"""
        self.fonts.clear()
        self.paths.clear()

        for file in os.listdir(FONT_PATH):
            if file.lower().endswith((".ttf", ".otf")):
                self.fonts.append(file)
                self.paths.append(os.path.join(FONT_PATH, file))

    def open(self):
        """opens the change font menu"""
        super().open()
        self.load_fonts()

    def handle_event(self, event, simulation):
        """handles mouse clicking to close the menu and choose a font"""
        super().handle_event(event)

        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.item_rects):
                if rect.collidepoint(event.pos):
                    new_font_path = self.paths[self.scroll_offset + i]
                    simulation.current_font = os.path.basename(new_font_path)
                    simulation.font = pygame.font.Font(new_font_path, 30)
                    simulation.ui.font = simulation.font
                    return
                
    def draw(self, surface):
        """draws the change font menu with scrolling"""
        super().draw(surface)

        if not self.visible:
            return

        mouse_pos = pygame.mouse.get_pos()

        y = self.rect.top + 100

        self.item_rects.clear()

        for i in range(self.scroll_offset, min(len(self.fonts), self.scroll_offset + self.max_visible_rows)):
            font_name = self.fonts[i]
            text_surf = self.body_font.render(font_name, True, self.text_colour)
            rect = text_surf.get_rect(topleft=(self.rect.x + 40, y))
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, (80,80,120), rect.inflate(10,6))
            surface.blit(text_surf, rect)
            self.item_rects.append(rect)
            y += self.row_height
