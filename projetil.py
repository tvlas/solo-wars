import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, sw_settings, screen, nave):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(
            0, 0, sw_settings.bullet_width, sw_settings.bullet_height)
        self.rect.centerx = nave.rect.centerx
        self.rect.top = nave.rect.top
        self.y = float(self.rect.y)
        self.color = sw_settings.bullet_color
        self.speed_factor = sw_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
