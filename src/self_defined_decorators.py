# imports
from settings import *
from functools import wraps
import datetime
import os

def log_call(func):
    """decorator to log when some functions are called"""
    @wraps(func) # ensure function keeps its original properties
    def wrapper(*args, **kwargs):
        """function being called"""
        try:
            with open(os.path.join(LOG_PATH, 'log.txt'), "a") as file:
                if func.__name__ == "reset_simulation": # log when simulation is reset
                    file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + f": The simulation has been reset!\n")
                elif func.__name__ == "ui_draw": # log when the UI is drawn
                    file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + f": The UI has been drawn!\n")
                elif func.__name__ == "audio_draw": # log when the UI is drawn
                    file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + f": The audio UI has been drawn!\n")
                elif func.__name__ == "music_draw": # log when the UI is drawn
                    file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + f": The music UI has been drawn!\n")
                elif func.__name__ == "font_draw": # log when the UI is drawn
                    file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + f": The font UI has been drawn!\n")
        except FileNotFoundError: # create file if not found
            with open(os.path.join(LOG_PATH, 'log.txt'), "w") as file:
                file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + f": {func.__name__} called, log file created.\n")
        except PermissionError: # just give up if somehow you cant read the file
            print("You do not have access to this file's directory!")
        return func(*args, **kwargs)
    return wrapper

def physics_log_call(func):
    """decorator to log when a physics function runs"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with open(os.path.join(LOG_PATH, 'physics.txt'), 'a') as file: # log when physics function runs
                file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + f": Physics function {func.__name__} ran successfully!\n")
        except FileNotFoundError: # create file and log when function runs
            with open(os.path.join(LOG_PATH, 'physics.txt'), 'w') as file:
                file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + f": Physics function {func.__name__} ran and log file created.\n")
        except PermissionError:
            print("You do not have access to this file's directory!")

        result = func(*args, **kwargs) # ensure decorator wont stop function returning what it needs to
        return result
    return wrapper

def log_key_press(func):
    """decorator to log when a key is pressed"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        self = args[0] # since the only one function being put into here, the first item passed into args is the simulation "self" variable

        if self.key_was_pressed: # if a key was pressed write time into file
            try:
                with open(os.path.join(LOG_PATH, 'keys.txt'), "a") as file:
                    file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ": A key was pressed!\n")
            except FileNotFoundError:
                with open(os.path.join(LOG_PATH, 'keys.txt'), "w") as file:
                    file.write(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) + ": A key was pressed, log file created.\n")
            except PermissionError:
                print("You do not have access to this file's directory!")

        self._key_was_pressed = False
        return result
    return wrapper
