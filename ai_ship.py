import pygame
from pygame.sprite import Sprite

class AI_Ship( Sprite ):
    """A class to manage Ship for Alien Invasion game"""
    
    def __init__( self, ai_game ):
        """Initialization of the ship for game"""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.ai_settings = ai_game.ai_settings

        self.image = pygame.image.load( 'images//ship.bmp' ) #Load image
        self.rect = self.image.get_rect() #Get rec for positioning

        self.flg_moving_right, self.flg_moving_left = False, False
        self.flg_moving_up, self.flg_moving_dn = False, False #Exercise

        self.ready()

    def update( self ):
        """Setup ship position"""
        #Increments of coordinate x by fractions of pixel with float copy
        if self.flg_moving_right and self.rect.right < self.screen_rect.right:
            self.coordx += self.ai_settings.ship_speed #self.rect.x += 1
        elif self.flg_moving_left and self.rect.left > 0:
            self.coordx -= self.ai_settings.ship_speed
        elif self.flg_moving_up and self.rect.top > 0: #Vertical movement (Exer)
            self.coordy -= self.ai_settings.ship_speed
        elif self.flg_moving_dn and self.rect.bottom < self.screen_rect.bottom:
            self.coordy += self.ai_settings.ship_speed

        self.rect.x = self.coordx #Transfer float coord-x back to int
        self.rect.y = self.coordy #Exercise (ship vertical movement) only

    def blitme( self ):
        """Draw the ship at its current location"""
        self.screen.blit( self.image, self.rect )

    def ready( self ):
        """Put ship back to the initial point for next round"""
        self.rect.midbottom = self.screen_rect.midbottom #Overlay midbottom
        self.coordx = float( self.rect.x ) #Refresh a decimal copy
        self.coordy = float( self.rect.y ) #Refresh a decimal copy

        #self.rect.midleft = self.screen_rect.midleft #midtop/center
        #self.rect.x, self.rect.y = 300, 300 #Position by coordinates

        #self.rect.centerx = self.screen_rect.centerx
        #self.rect.centery = self.screen_rect.centery
      
