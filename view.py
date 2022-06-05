import pygame
import sys, math
from raindrop import Raindrop
from star import Star
from random import randint
from ai_settings import AI_Settings

class View:
    """Overal model of game assets and behaviours"""

    def __init__( self ):
        """Initialize the game, create game resources"""
        pygame.init() #Initialize background setting 
        self.settings = AI_Settings()

        self.mode_fs = self._init_mode_fs()
        #self.mode_fs = self._init_mode_ar()
        pygame.display.set_caption( self.settings.title )

        self.raindrops = pygame.sprite.Group() #Introduce raindrop group
        
        #Claculation of raindrops accommodated in a row
        self.rd_width, self.rd_height = Raindrop( self ).rect.size #Tuple
        self.avai_space_x = self.settings.scrn_width - ( 2 * self.rd_width )
        self.num_rd_x = self.avai_space_x // ( 2 * self.rd_width )

        self.avai_space_y = self.settings.scrn_height - ( 2 * self.rd_height )
        self.num_rows = self.avai_space_y // ( 2 * self.rd_height )

        self._create_raindrops()
        
        #13-1/13-2 (random placement)
        self.stars = pygame.sprite.Group() #Stars to be spread randomly
        self._create_stars()

    def run_game( self ):
        """Main loop of the game"""
        while True: #watch for keyboard or mouse events and act accordingly
            self._check_events()

            #====Refresh of the location or validity for all elements start====
            self._update_raindrops()
            #self.stars.update() #Gets triggered more than number of events
            #====Refresh of the location or validity for all elements end====
            
            self._update_screen() #Last call for the game to render screen

    def _init_mode_fs( self ):
        print( "Setup for full screen mode" )
        self.screen = pygame.display.set_mode( ( 0, 0 ), pygame.FULLSCREEN )
        self.settings.scrn_width = self.screen.get_rect().width
        self.settings.scrn_height = self.screen.get_rect().height
        return 'Y'

    def _init_mode_ar( self ):
        print( "Setup for auto resizable mode" )
        self.screen = pygame.display.set_mode( 
            ( self.settings.scrn_width, self.settings.scrn_height ), 
            pygame.RESIZABLE )
        return 'N'

    def _check_events( self ):
        """Response to keyboard or mouse events"""
        for event in pygame.event.get():
            #try:
            #    event_key = event.key
            #except AttributeError:
            #    print( "Found no event" )
            #    pass
            #else:
            #    print( f"Found event key of { event_key }" )
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_events_keydown( event )
            elif event.type == pygame.KEYUP:
                self._check_events_keyup( event )
            #if event.type == pygame.VIDEORESIZE:
                #screen.blit(pygame.transform.scale(pic, event.dict['size']), (0, 0))
                #pygame.display.update()

    def _check_events_keydown( self, event ):
        if event.key == pygame.K_RIGHT:
            print( "Dummy right arrwow" )
        elif event.key == pygame.K_q: #module 'pygame' has no attribute 'K_Q'
            sys.exit()
        elif event.key == pygame.K_SPACE:
            print( "Dummy space bar" )

        elif event.key == pygame.K_ESCAPE: #How to scale screen or relocate all components?
            if self.mode_fs != 'N':
                print( "In full screen mode" )
                self._quit_fullscreen()
        elif event.key == pygame.K_MODE: #Not triggered
            if self.mode_fs != 'Y':
                print( "In normal mode" )
                self._enter_fullscreen()

    def _check_events_keyup( self, event ):
        if event.key == pygame.K_RIGHT:
            print( "Dummy right arrwow" )

    def _create_raindrops( self ):
        """Setup a fleet of raindrops"""
        #self.raindrops.add( Raindrop( self ) ) #start with one for look & feel

        #Extra row to avoid holes between old and new rows 
        for row in range( self.num_rows + 1 ):
            #For a row of raindrops
            self._create_rq_row( self.num_rd_x, row, self.rd_width, self.rd_height )
            #for seq in range( num_rd_x ): #Some sideway room on the right
                #self._create_rq( seq, row, rd_width, rd_height )

    def _create_rq_row( self, num_rd_x, row, rd_width, rd_height ):
        for seq in range( num_rd_x ): #Some sideway room on the right
            rd = Raindrop( self )
            rd_x = rd_width + 2 * rd_width * seq
            rd.rect.x = rd_x
            rd_y = rd_height + 2 * rd_height * row
            rd.rect.y = rd_y
            self.raindrops.add( rd )

    def _update_screen( self ): #Render latest location of all valid elements
        """Refresh screen"""
        self.screen.fill( self.settings.bg_color ) #Apply intended bg color
        
        #13-1/13-2 (random placement)
        self.stars.draw( self.screen ) #The draw on the screen for all elements

        self.raindrops.draw( self.screen ) #The draw on the screen for all elems

        pygame.display.flip() #Visualize the recently updated screen/surface

    def _update_raindrops( self ):
        """Activity of all raindrops during the game run"""
        self.raindrops.update() #Only update method can be triggered one for all?
        self._check_bottom() 
        self._check_top() 
        
        #Take out hit raindrops

    def _check_bottom( self ):
        for rd in self.raindrops.copy():
            if rd.hit_bottom():
                self.raindrops.remove( rd )
        
    def _check_top( self ):
        flg_row_one = False
        for rd in self.raindrops:
            if rd.rect.top <= rd.rect.height * 3: #Look for element in row 1
                flg_row_one = True #Found

            if flg_row_one:
                break

        #if flg_row_one:
        #    pass
        #else:
        if not flg_row_one: #Position for row 1 is open
            self._create_rq_row( self.num_rd_x, 0, self.rd_width, self.rd_height )       

    #13-1/13-2 (random placement)
    def _create_stars( self ):
        coordx_max = self.settings.scrn_width
        coordy_max = self.settings.scrn_height - 200
        offset = math.ceil( Star( self ).rect.width / 2 ) #Offset for center
        
        for idx in range( 10 ):
            star = Star( self )
            #Calculate the tuple value for star center position
            cntr = randint( offset, coordx_max ), randint( offset, coordy_max )
            star.rect.center = cntr
            self.stars.add( star )

    def _quit_fullscreen( self ):
        self.settings.scrn_width = self.settings.scrn_width_def
        self.settings.scrn_height = self.settings.scrn_height_def
        self.screen = pygame.display.set_mode( 
            ( self.settings.scrn_width, self.settings.scrn_height ) )
        self.mode_fs = 'N'

    def _enter_fullscreen( self ):
        self.screen = pygame.display.set_mode( ( 0, 0 ), pygame.FULLSCREEN )
        self.settings.scrn_width = self.screen.get_rect().width
        self.settings.scrn_height = self.screen.get_rect().height
        self.mode_fs = 'Y'

    def _max_screen( self ): #Go to full screen mode?
        self.screen = pygame.display.set_mode( ( 0, 0 ), pygame.FULLSCREEN )
        self.settings.scrn_width = self.screen.get_rect().width
        self.settings.scrn_height = self.screen.get_rect().height
        self.mode_fs = 'Y'

    def _restore_screen( self ): #Back to default screen mode?
        self.settings.scrn_width = self.settings.scrn_width_def
        self.settings.scrn_height = self.settings.scrn_height_def
        self.screen = pygame.display.set_mode( 
            ( self.settings.scrn_width, self.settings.scrn_height ) )
        self.mode_fs = 'Y'


if __name__ == '__main__':
    ai = View()
    ai.run_game()



#resize by the maximax/restor button on top right corner
#back to full screen