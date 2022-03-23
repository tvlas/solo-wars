import pygame
from pygame.sprite import Group

import background as bg
import game_functions as gf
import sound as music
from botao_play import Button
from game_stats import GameStats
from player import Spaceship
from score import Score
from settings import Settings


def main():
    pygame.init()
    sw_settings = Settings()
    screen = pygame.display.set_mode(
        (sw_settings.screen_width, sw_settings.screen_height))
    pygame.display.set_caption("Solo Wars by tvlas")
    play_button = Button(sw_settings, screen, "PLAY")
    pygame.display.flip()
    bullets = Group()
    troopers = Group()
    nave = Spaceship(sw_settings, screen)
    stats = GameStats(sw_settings)
    sb = Score(sw_settings, screen, stats)
    gf.create_fleet(sw_settings, screen, nave, troopers)
    music.bg_sound()

    while True:
        gf.check_events(sw_settings, screen, stats,
                        play_button, nave, troopers, bullets)
        if stats.game_active:
            nave.update()
            gf.update_bullets(sw_settings, screen, nave,
                              stats, sb, troopers, bullets)
            gf.update_troopers(sw_settings, stats, screen,
                               nave, troopers, bullets)
        gf.update_screen(sw_settings, screen, stats, sb,
                         nave, troopers, bullets, play_button)
        bg.game_bg()


if __name__ == '__main__':
    main()
