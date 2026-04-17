import pygame

BASE_SIZE:tuple[int, int] = (800, 600)

FULLSCREEN:bool = False

FULLSCREEN_SIZE:tuple[int, int] = (0, 0)

FULLSCREEN_KEY:int = pygame.K_F11

CURRENT_SIZE:tuple[int, int] = BASE_SIZE

LAST_SIZE:tuple[int, int] = BASE_SIZE

DISPLAY: pygame.Surface  # pyright: ignore[reportAssignmentType]

SCALE = {"width":1.0, "height":1.0, "overall":1.0}

ALL_OBJECTS_CACHE = []

