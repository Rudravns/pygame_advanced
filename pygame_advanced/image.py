import pygame
from . import vars, pg_obj

class image:
    def __init__(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.base_rect = self.rect.copy()
        self.update_scaling()
        vars.ALL_OBJECTS_CACHE.append(self)

    def update_scaling(self):
        self.rect.width = self.base_rect.width * vars.SCALE["width"]
        self.rect.height = self.base_rect.height * vars.SCALE["height"]
        self.rect.x = self.base_rect.x * vars.SCALE["width"]
        self.rect.y = self.base_rect.y * vars.SCALE["height"]
        

