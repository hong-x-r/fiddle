import pygame.font

class Button:
    """Representation of a button-like rect"""
    def __init__( self, ai_game, msg, btn_size, btn_col, txt_col, font_size ):
        """Initial setup for the [button]"""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        
        self.msg = msg
        self.btn_wid, self.btn_hgt = btn_size;
        self.btn_col = btn_col
        self.txt_col = txt_col
        self.font = pygame.font.SysFont( None, font_size )
        
        #self.rect is being looked at by pygame collidepoint for click event
        self.rect = pygame.Rect( 0, 0, self.btn_wid, self.btn_hgt )
        self.rect.center = self.screen_rect.center
        
        self._prep_msg()

    def _prep_msg( self ):
        """Convert the msg to rendered image as button with the text centered"""
        self.img = self.font.render( self.msg, True, self.txt_col, self.btn_col )
        self.img_rect = self.img.get_rect()
        self.img_rect.center = self.rect.center
        #self.img_rect.center = self.screen_rect.center

    #def update( self ):
    def show( self ):
        """Visualize the button"""
        self.screen.fill( self.btn_col, self.rect )
        self.screen.blit( self.img, self.img_rect )

    def reset( self, msg ):
        self.msg = msg
        self._prep_msg()
