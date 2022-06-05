import pygame
from pygame.sprite import Sprite

class AI_Alien( Sprite ):
    """Representation of an alien invading earth"""

    def __init__( self, ai_game, fleet = None, row = None, seq = None ):
        """Initial setup of an alien instance"""
        super().__init__()
        #self.row = row, #Type of tuple with trailing comma
        self.fleet = fleet
        self.row = row
        self.seq = seq
        self.game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #Load image and get its rec
        self.image = pygame.image.load( 'images//alien.bmp' )
        self.rect = self.image.get_rect()

        #Start it at the top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height * 2

        self.ai_settings = ai_game.ai_settings

#    def update( self ):
    def update( self ):
        """Flying sideways"""
        self.speed_x = self.ai_settings.alien_speed_x
        self.direction = self.ai_settings.fleet_direction 
        self.coordx = float( self.rect.x )
        self.coordx += self.speed_x * self.direction
        self.rect.x = self.coordx

    def hit_edge( self ):
        if( self.rect.right >= self.screen_rect.right or 
            self.rect.left <= self.screen_rect.left ):
            return True;
        
    def drop( self ):
        """Dropping"""
        self.speed_y = self.ai_settings.alien_speed_y 
        self.coordy = float( self.rect.y )
        self.coordy += self.speed_y #Drop vertically 
        self.rect.y = self.coordy

    def desc( self ):
        return f"Alien in fleet { self.fleet } row { self.row } seq { self.seq }" 

