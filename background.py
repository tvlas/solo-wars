import pygame


def game_bg():
    screen = pygame.display.set_mode((1200, 800))
    bg = pygame.image.load('source_files/img/bg.bmp')
    screen.blit(bg, (0, 0))
