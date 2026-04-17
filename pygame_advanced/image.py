from flask.cli import F
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
    
    def move_ip(self, dx, dy):
        self.base_rect.x += dx / vars.SCALE["width"]
        self.base_rect.y += dy / vars.SCALE["height"]
        self.update_scaling()
    
    def draw(self, surface:pygame.Surface | None = None, hitbox = False):
        if surface is None:
            surface = vars.DISPLAY
        surface.blit(self.image, self.rect)
        if hitbox:
            pygame.draw.rect(surface, (255,0,0), self.rect, 2)
    
    def change_img(self, path:str):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self.base_rect = self.rect.copy()
        self.update_scaling()


    def __del__(self):
        vars.ALL_OBJECTS_CACHE.remove(self)

