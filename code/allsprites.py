import pygame
from pygame.math import Vector2
from settings import *


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = Vector2()
        self.display_surf = pygame.display.get_surface()
        self.bg = pygame.image.load('../graphics/other/bg.png').convert()

    def customize_draw(self, player):

        # Change the offset vector
        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        # Blit the bg
        self.display_surf.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surf.blit(sprite.image, offset_rect)

