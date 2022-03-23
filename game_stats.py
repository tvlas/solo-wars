class GameStats():

    def __init__(self, sw_settings):
        self.sw_settings = sw_settings
        self.high_score = 0
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.players_left = self.sw_settings.player_limit
        self.score = 0
