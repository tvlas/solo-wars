import sys
from time import sleep

import pygame
from pygame import mixer

from projetil import Bullet
from trooper import Trooper


def check_keydown_events(event, sw_settings, screen, player, bullets):
    """ Eventos de pressionar teclas """
    if event.key == pygame.K_RIGHT:
        player.moving_right = True
    elif event.key == pygame.K_LEFT:
        player.moving_left = True
    elif event.key == pygame.K_UP:
        player.moving_up = True
    elif event.key == pygame.K_DOWN:
        player.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(sw_settings, screen, player, bullets)
        laser_sound = mixer.Sound('source_files/music/lasers.wav')
        laser_sound.play()
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def fire_bullet(sw_settings, screen, player, bullets):
    if len(bullets) < sw_settings.bullets_allowed:
        new_bullet = Bullet(sw_settings, screen, player)
        bullets.add(new_bullet)


def check_keyup_events(event, player):
    # Verifica os eventos ao liberar teclas
    if event.key == pygame.K_RIGHT:
        player.moving_right = False
    elif event.key == pygame.K_LEFT:
        player.moving_left = False
    elif event.key == pygame.K_UP:
        player.moving_up = False
    elif event.key == pygame.K_DOWN:
        player.moving_down = False


def check_events(sw_settings, screen, stats, play_button,
                 player, troopers, bullets):
    # Captura os eventos quando o jogo é executado
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, sw_settings, screen, player, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, player)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(sw_settings, screen, stats, play_button,
                              player, troopers, bullets, mouse_x, mouse_y)


def check_play_button(sw_settings, screen, stats, play_button,
                      player, troopers, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        sw_settings.ini_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        troopers.empty()
        bullets.empty()
        create_fleet(sw_settings, screen, player, troopers)
    player.center_player()


def update_screen(sw_settings, screen, stats, sb, player,
                  troopers, bullets, play_button):
    """  Atualiza as imagens na tela  """
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    player.blitme()
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    troopers.draw(screen)
    pygame.display.flip()


def update_bullets(sw_settings, screen, player, stats, sb, troopers, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_trooper_collisions(
        sw_settings, screen, player, stats, sb, troopers, bullets)


def check_bullet_trooper_collisions(sw_settings, screen, player,
                                    stats, sb, troopers, bullets):
    """  Verifica quando as balas atingirem os aliens  """
    collisions = pygame.sprite.groupcollide(bullets, troopers, True, True)
    if collisions:
        for troopers in collisions.items():
            stats.score += sw_settings.trooper_points * len(troopers)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(troopers) == 0:
        bullets.empty()
        sw_settings.increase_speed()   # new
        create_fleet(sw_settings, screen, player, troopers)


def get_number_troopers_x(sw_settings, trooper_width):
    """  O numero de tropas será gerado com forme suas dimensões  """
    available_space_x = sw_settings.screen_width - 2 * trooper_width
    number_troopers_x = int(available_space_x / (2 * trooper_width))
    return number_troopers_x


def create_trooper(sw_settings, screen, troopers, trooper_number, row_number):
    trooper = Trooper(sw_settings, screen)
    trooper_width = trooper.rect.width
    trooper.x = trooper_width + 2 * trooper_width * trooper_number
    trooper.rect.x = trooper.x
    trooper.rect.y = trooper.rect.height + 2 * trooper.rect.height * row_number
    trooper.add(troopers)


def create_fleet(sw_settings, screen, player, troopers):
    """  Cria uma frota de aliens """
    trooper = Trooper(sw_settings, screen)
    number_troopers_x = get_number_troopers_x(sw_settings, trooper.rect.width)
    number_rows = get_number_rows(
        sw_settings, player.rect.height, trooper.rect.height)
    for row_number in range(number_rows):
        for trooper_number in range(number_troopers_x):
            create_trooper(sw_settings, screen, troopers,
                           trooper_number, row_number)


def get_number_rows(sw_settings, player_height, trooper_height):
    """  Define a quantidade de aliens com base em seu tamanho  """
    available_space_y = (sw_settings.screen_height -
                         (3 * trooper_height) - player_height)
    number_rows = int(available_space_y / (4 * trooper_height))
    return number_rows


def player_hit(sw_settings, stats, screen, player, troopers, bullets):
    """ Função que define o comportamento da nave caso colida """
    if stats.players_left > 0:
        stats.players_left -= 1
        troopers.empty()
        bullets.empty()
        create_fleet(sw_settings, screen, player, troopers)
        player.center_player()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    sleep(0.5)


def update_troopers(sw_settings, stats, screen, player, troopers, bullets):
    """  Quando a nave colidir será criada uma nova frota de aliens """
    check_fleet_edges(sw_settings, troopers)
    check_troopers_bottom(sw_settings, stats, screen,
                          player, troopers, bullets)
    troopers.update()
    if pygame.sprite.spritecollideany(player, troopers):
        player_hit(sw_settings, stats, screen, player, troopers, bullets)


def check_fleet_edges(sw_settings, troopers):
    """ Verifica se as tropas colidiram com as bordas da janela """
    for trooper in troopers.sprites():
        if trooper.check_edges():
            change_fleet_direction(sw_settings, troopers)
            break


def change_fleet_direction(sw_settings, troopers):
    """  Mudança de direção das tropas  """
    for trooper in troopers.sprites():
        trooper.rect.y += sw_settings.fleet_drop_speed
    sw_settings.fleet_direction *= -1


def check_troopers_bottom(sw_settings, stats, screen,
                          player, troopers, bullets):
    """Verifica se as tropas inimigas alcançaram o final da tela."""
    screen_rect = screen.get_rect()
    for trooper in troopers.sprites():
        if trooper.rect.bottom >= screen_rect.bottom:
            # Acontece o mesmo que a nave quando atingida.
            player_hit(sw_settings, stats, screen, player, troopers, bullets)
            break


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
