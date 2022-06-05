import pygame
from pygame.sprite import Sprite

class AI_Bullet( Sprite ):
    """Module of a bullet fired from the ship for Alien Invasion game"""

    def __init__( self, ai_game ):
        """Create a bullet for the game"""
        super().__init__()
        self.screen = ai_game.screen
        self.ai_settings = ai_game.ai_settings
        self.color = self.ai_settings.bullet_color
        
        #Initiate bullet rect at ( 0, 0 ) before repositioning
        self.rect = pygame.Rect( 0, 0, self.ai_settings.bullet_width, 
            self.ai_settings.bullet_height )
        self.rect.midtop = ai_game.ship.rect.midtop
        #Exercise (horizontal bullet) only
        #self.rect.midright = ai_game.ship.rect.midright

        self.coordy = float( self.rect.y ) #Keep a decimal copy of coordinate
        self.coordx = float( self.rect.x ) #Keep a decimal copy of coordinate

    def update( self ):
        """Move the bullet up the screen"""
        
        self.coordy -= self.ai_settings.bullet_speed #Via the decimal copy
        self.rect.y = self.coordy 
        #Exercise (horizontal bullet) only
        #self.coordx += self.ai_settings.bullet_speed #Via the decimal copy
        #self.rect.x = self.coordx 

    def draw_itself( self ):
        """Draw the bullet to the screen"""
        pygame.draw.rect( self.screen, self.color, self.rect )
