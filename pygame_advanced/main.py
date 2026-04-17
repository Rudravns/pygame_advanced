import pygame
from . import vars
import os

def create_display(starting_display_size:tuple[int,int], fullscreen_key = pygame.K_F11) -> pygame.Surface:
    """
    Initiates the display info and validates the existing surface.\n
    :starting_display_size: The size of the display
    :fullscreen_key: The key to toggle fullscreen, default is F11
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Ensure pygame's display system is ready to report hardware info
    if not pygame.display.get_init():
        pygame.display.init()

    info = pygame.display.Info()
    vars.FULLSCREEN_SIZE = (info.current_w, info.current_h)
    vars.BASE_SIZE = starting_display_size
    vars.FULLSCREEN_KEY = fullscreen_key
    vars.CURRENT_SIZE = vars.BASE_SIZE
    vars.LAST_SIZE = vars.BASE_SIZE

    vars.DISPLAY = pygame.display.set_mode(starting_display_size, pygame.RESIZABLE)


    return vars.DISPLAY



def event(event: pygame.event.Event):
    """
    Gets the event for resizing \n
    :event: The event
    """
    if event.type == pygame.VIDEORESIZE:
        vars.LAST_SIZE = vars.CURRENT_SIZE
        vars.CURRENT_SIZE = (event.w, event.h)
        rescale()
        
    
    if event.type == pygame.KEYDOWN:
        if event.key == vars.FULLSCREEN_KEY:
            if vars.FULLSCREEN:
                pygame.display.set_mode(vars.LAST_SIZE, pygame.RESIZABLE)
            else:
                pygame.display.set_mode(vars.FULLSCREEN_SIZE)

            vars.FULLSCREEN = not vars.FULLSCREEN
            vars.CURRENT_SIZE = vars.DISPLAY.get_size() # pyright: ignore[reportAttributeAccessIssue]
            rescale()

def rescale():
    vars.SCALE["width"] = vars.CURRENT_SIZE[0] / vars.BASE_SIZE[0]
    vars.SCALE["height"] = vars.CURRENT_SIZE[1] / vars.BASE_SIZE[1] 
    vars.SCALE["overall"] = min(vars.SCALE["width"], vars.SCALE["height"])

    #scale all obj
    for obj in vars.ALL_OBJECTS_CACHE:
        obj.update_scaling()
     

            
            
        