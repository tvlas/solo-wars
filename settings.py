class Settings():
    def __init__(self):
        self.player_speed_factor = 1
        self.screen_width = 1200
        self.screen_height = 800
        self.bullet_speed_factor = 5
        self.bullet_width = 3
        self.bullet_height = 20
        self.bullet_color = 0, 255, 255
        self.bullets_allowed = 3
        self.trooper_speed_factor = 1
        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.fleet_direction = 1
        self.ini_dynamic_settings()
        self.player_limit = 3

    def ini_dynamic_settings(self):
        self.player_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.trooper_speed_factor = 1
        self.fleet_direction = 1
        self.trooper_speed_factor = 1
        self.trooper_points = 5

    def increase_speed(self):
        self.player_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.trooper_speed_factor *= self.speedup_scale
        self.trooper_points = int(self.trooper_points * self.score_scale)
        print(self.trooper_points)
