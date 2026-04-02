# imports
import pygame
from settings import *
import os

def import_assets(current_song):
    """load the song from graphics and play"""
    pygame.mixer.music.load(os.path.join(AUDIO_PATH, current_song))
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

def bubble_sort(array):
    """bubble sort the array of objects in increasing order of mass"""
    n = len(array)
    for i in range(1, n):
        swapped = False
        for j in range(0, n - 1):
            if array[j].mass > array[j + 1].mass:
                array[j], array[j + 1] = array[j + 1], array[j]
                swapped = True
        n -= 1
        if not swapped:
            break
    return array