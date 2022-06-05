import pygame
from pygame.sprite import Sprite

class Raindrop( Sprite ):
    """Representation of an raindrop invading earth"""

    def __init__( self, view ):
        """Initial setup of an raindrop instance"""
        super().__init__()
        self.view = view
        self.screen = view.screen
        self.screen_rect = self.screen.get_rect()

        #Load image and get its rec
        self.image = pygame.image.load( 'images//raindrop.bmp' )
        self.rect = self.image.get_rect()

        #Start it at the top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        self.settings = view.settings

#    def update( self ):
    def update( self ):
        """Flying sideways"""
        self.speed = self.settings.raindrop_speed
        self.coordy = float( self.rect.y )
        self.coordy += self.speed
        self.rect.y = self.coordy

    def hit_bottom( self ):
        if self.rect.top >= self.screen_rect.bottom - self.rect.height:
            return True;

        