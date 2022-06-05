
class AI_Settings:
    """Model of all the setting for the game"""

    def __init__( self ):
        """Initialization of static settings"""
        self.title = 'Alien Invasion'

        #For screen
        self.scrn_width_def = 800 #For full screen mode to fall back to
        self.scrn_height_def = 600 #For full screen mode to fall back to
        self.scrn_width = 800 #For window mode
        self.scrn_height = 600 #For window mode
        #self.bg_color = ( 255, 0, 0 ) #Color red
        self.bg_color = ( 230, 230, 230 ) #Color grey

        #For ship
        self.ship_num_left = 2

        #For bullets
        self.button_name = 'Play'
        self.bullet_width = 2000
        self.bullet_height = 15
        self.bullet_color = ( 60, 60, 60 )
        self.bullet_allowed = 5

        #For aliens
        self.alien_speed_y = 20.0

        #For button
        self.button_size = ( 200, 50 )
        self.button_col = ( 0, 255, 0 )
        self.button_txt_col = ( 255, 255, 255 )
        self.button_font_size = 48

        #Acceleration rate
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.init_dyna_settings()

        #For scorecard
        self.scorecard_txt_col = ( 30, 30, 30 )
        self.scorecard_score_font_size = 30
        self.scorecard_high_score_font_size = 25
        self.scorecard_lvl_font_size = 20

        #For others
        self.raindrop_speed = 2.0 #Exercise only
        
    def init_dyna_settings( self ):
        """Initialization of settings that could change throughout game"""
        #Session-bound settings updated as the game progresses in one go
        self.bullet_speed = 1.5
        self.ship_speed = 1.0
        self.alien_speed_x = 1.0
        self.alien_points = 5

        self.bullet_speed_f = float( self.bullet_speed )
        self.ship_speed_f = float( self.ship_speed )
        self.alien_speed_x_f = float( self.alien_speed_x )
        self.alien_points_f = float( self.alien_points )
        
        #Correspond to direction of ship movement in terms of x coordinate
        self.fleet_direction = 1

    def level_up( self ):
        """Increase speed of all elements that could"""
        self.bullet_speed_f *= self.speedup_scale
        self.ship_speed_f *= self.speedup_scale
        self.alien_speed_x_f *= self.speedup_scale
        self.alien_points_f *= self.score_scale

        self.bullet_speed = self.bullet_speed_f
        self.ship_speed = self.ship_speed_f
        self.alien_speed_x = self.alien_speed_x_f
        self.alien_points = int( self.alien_points_f )
