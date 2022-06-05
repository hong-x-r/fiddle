import pygame.font
from ai_ship import AI_Ship
from pygame.sprite import Group

class ScoreCard:
    """Report/display information/statistics of the game"""
    
    def __init__( self, ai_game, text_col, score_size, hscore_size, lvl_size ):
        """Initialize scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_game.ai_settings
        self.stats = ai_game.stats

        #Font attributes
        self.text_col = text_col
        self.font_score = pygame.font.SysFont( None, score_size )
        self.font_hscore = pygame.font.SysFont( None, hscore_size )
        self.font_lvl = pygame.font.SysFont( None, lvl_size )
        
        #A rect is not needed for click event
        
        self.prep_score()
        self.prep_high_score()
        self.prep_lvl()
        self.prep_ships()

    def prep_score( self ):
        """Render session score to image on card/board"""
        score = round( self.stats.score, -1 )
        score_fmt = "{:,}".format( score )
        self.score_img = self.font_score.render( score_fmt, True, 
                    self.text_col, self.ai_settings.bg_color )
        self.score_rect = self.score_img.get_rect()
        self.score_rect.right = self.screen_rect.right - 15
        self.score_rect.top = 15

    def prep_high_score( self ):
        """Render highest score to image on card/board"""
        high_score = round( self.stats.high_score, -1 )
        high_score_fmt = "{:,}".format( high_score )
        self.high_score_img = self.font_hscore.render( high_score_fmt, True, 
                    self.text_col, self.ai_settings.bg_color )
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score( self ):
        """Refresh high score from active session"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_lvl( self ):
        """Render session level to image on card/board"""
        self.lvl_img = self.font_lvl.render( "Level: " + str( self.stats.lvl ), 
                        True, self.text_col, self.ai_settings.bg_color )
        self.lvl_rect = self.lvl_img.get_rect()
        self.lvl_rect.right = self.score_rect.right
        self.lvl_rect.top = self.score_rect.bottom + 5

    def prep_ships( self ):
        """Visualize the remaining ships for play in current session"""
        self.ships = Group()
        for n in range( self.stats.ship_num_left ):
            ship = AI_Ship( self.ai_game )
            ship.rect.x = 10 + n * ship.rect.width
            ship.rect.y = 10
            self.ships.add( ship )

    def show( self ):
        self.screen.blit( self.score_img, self.score_rect )
        self.screen.blit( self.high_score_img, self.high_score_rect )
        self.screen.blit( self.lvl_img, self.lvl_rect )
        self.ships.draw( self.screen )

