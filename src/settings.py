# imports
import pygame
from vector import R2Vector
from pathlib import Path 

# define variables going to be used throughout the program, may move some if i realise im only using them in one file
pygame.display.init()
info = pygame.display.Info()
WINDOW_WIDTH = info.current_w
WINDOW_HEIGHT = info.current_h
SCREEN_CENTRE = R2Vector(x=WINDOW_WIDTH//2, y=WINDOW_HEIGHT//2)
COLOUR_INACTIVE = pygame.Color('chartreuse4') # contender to be moved when i can be bothered to go checking - spoiler i never bothered to check
COLOUR_ACTIVE = pygame.Color('dodgerblue2')
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
GRAPHICS_PATH = PROJECT_DIR / "graphics"
FONT_PATH = GRAPHICS_PATH / "fonts" 
AUDIO_PATH = GRAPHICS_PATH / "audio" 
DATABASE_PATH = PROJECT_DIR / "database" / "planets.db"
LOG_PATH = PROJECT_DIR / "logs"
IMAGE_PATH = PROJECT_DIR / "graphics" / "images"
colours = { # colours for planet creation
    "RED": "(255, 0, 0)",
    "GREEN": "(0, 255, 0)",
    "BROWN": "(150, 75, 0)",
    "BLUE": "(0, 0, 255)",
    "PURPLE": "(160, 32, 240)",
    "CYAN": "(0, 255, 255)",
    "LIGHT_GRAY": "(211, 211, 211)",
    "DARK_GRAY": "(169, 169, 169)",
    "LIGHT_RED": "(255, 204, 203)",
    "LIGHT_GREEN": "(144, 238, 144)",
    "YELLOW": "(255, 255, 0)",
    "LIGHT_BLUE": "(173, 216, 230)",
    "LIGHT_PURPLE": "(223, 197, 254)",
    "LIGHT_CYAN": "(224, 255, 255)",
    "BLACK": "(0, 0, 0)",
    "WHITE": "(255, 255, 255)"
}