import pygame
from pygame.sprite import Sprite

class Star( Sprite ):
    """Representation of an alien invading earth"""

    def __init__( self, ai_game ):
        """Initial setup of an alien instance"""
        super().__init__()
        self.screen = ai_game.screen

        #Load image and get its rec
        self.image = pygame.image.load( 'images//star.bmp' )
        self.rect = self.image.get_rect()

        #Start it at the top left corner
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        #Keep decimal copies of the coordinates
        self.coordx = float( self.rect.x )
        self.coordy = float( self.rect.y )

        
