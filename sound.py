import pygame


def bg_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('source_files/music/bg_sound.wav')
    pygame.mixer.music.play(-1)
