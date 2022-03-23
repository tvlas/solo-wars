import pygame


class Spaceship():
    def __init__(self, sw_settings, screen):
        self.screen = screen
        self.sw_settings = sw_settings
        self.image = pygame.image.load('source_files/img/falcon.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.centery
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.centerx += 5
        if self.moving_left and self.rect.left > 0:
            self.rect.centerx -= 5
        if self.moving_up and self.rect.centery > 50:
            self.rect.centery -= 5
        if self.moving_down and self.rect.centery < 770:
            self.rect.centery += 5

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        pygame.image.load('source_files/img/falcon.png')

    def center_player(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
