import pygame
import sys, math
from time import sleep
from ai_settings import AI_Settings
from ai_ship import AI_Ship
from ai_bullet import AI_Bullet
from ai_alien import AI_Alien
from star import Star
from random import randint
from ai_stats import GameStats
from ai_button import Button
from ai_scorecard import ScoreCard

class AlienInvasion:
    """Overal model of game assets and behaviours"""

    def __init__( self ):
        """Initialize the game, create game resources"""
        pygame.init() #Initialize background setting 
        self.ai_settings = AI_Settings()

        self.mode_fs = self._init_mode_fs()
        #self.mode_fs = self._init_mode_ar()
        pygame.display.set_caption( self.ai_settings.title )
        
        self.stats = GameStats( self ) #Keep track of game statistics

        self.ship = AI_Ship( self ) #Initiate ship instance
        
        self.bullets = pygame.sprite.Group() #Introduce bullet group
        self.aliens = pygame.sprite.Group() #Introduce alien group
        
        self.flt = -1
        #Claculation of aliens accommodated in a row
        self.a_wid, self.a_hgt = AI_Alien( self ).rect.size #Tuple attribute
        self.ship_hgt = self.ship.rect.height
        self.avai_room_x = self.ai_settings.scrn_width - ( 2 * self.a_wid )
        self.num_aliens_x = self.avai_room_x // ( 2 * self.a_wid )
        #Claculation of aliens accommodated vertically
        self.avai_room_y = ( self.ai_settings.scrn_height - self.ship_hgt -
                ( 3 * self.ship_hgt )  ) #Wrapped in parentheses across lines
        self.num_rows = self.avai_room_y // ( 2 * self.ship_hgt )

        self._create_fleet() #First run of the fleet
        
        self.play_btn = Button( self, self.ai_settings.button_name, 
                        self.ai_settings.button_size, 
                        self.ai_settings.button_col, 
                        self.ai_settings.button_txt_col, 
                        self.ai_settings.button_font_size )
        
        self.scorecard = ScoreCard( self, self.ai_settings.scorecard_txt_col, 
                        self.ai_settings.scorecard_score_font_size, 
                        self.ai_settings.scorecard_high_score_font_size, 
                        self.ai_settings.scorecard_lvl_font_size )

    def run_game( self ):
        """Main loop of the game"""
        while True: #watch for keyboard or mouse events and act accordingly
            self._check_events() #Quit the game even after screen frozen

            #====Refresh of the location or validity for all elements start====
            if self.stats.game_active: #Play mode or game eligibility
                self.ship.update() #Gets triggered more than number of events
                self._update_bullets() #Activities on bullets
                self._update_fleet()
            #====Refresh of the location or validity for all elements end====
            
            self._update_screen() #Last call for the game to render screen

    def _init_mode_fs( self ):
        print( "Setup for full screen mode" )
        self.screen = pygame.display.set_mode( ( 0, 0 ), pygame.FULLSCREEN )
        self.ai_settings.scrn_width = self.screen.get_rect().width
        self.ai_settings.scrn_height = self.screen.get_rect().height
        return 'Y'

    def _init_mode_ar( self ):
        print( "Setup for auto resizable mode" )
        self.screen = pygame.display.set_mode( 
            ( self.ai_settings.scrn_width, self.ai_settings.scrn_height ), 
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_btn( mouse_pos )

            #print( f"Event ship loc { self.ship.rect.x }, { self.ship.rect.y }" )

        #print( f"Check ship loc { self.ship.rect.x }, { self.ship.rect.y }" )

    def _check_events_keydown( self, event ):
        if event.key == pygame.K_RIGHT:
            #self.ship.rect.x += 1
            self.ship.flg_moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.flg_moving_left = True
            #self.ship.rect.x -= 1
        elif event.key == pygame.K_q: #module 'pygame' has no attribute 'K_Q'
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        elif event.key == pygame.K_ESCAPE: #How to scale screen or relocate all components?
            if self.mode_fs != 'N':
                print( "In full screen mode" )
                self._quit_fullscreen()
        elif event.key == pygame.K_MODE: #Not triggered
            if self.mode_fs != 'Y':
                print( "In normal mode" )
                self._enter_fullscreen()

        #Exercise (vertical ship movement) only
        elif event.key == pygame.K_UP:
            self.ship.flg_moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.flg_moving_dn = True

    def _check_events_keyup( self, event ):
        if event.key == pygame.K_RIGHT:
            self.ship.flg_moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.flg_moving_left = False

        #Exercise (vertical ship movement) only
        elif event.key == pygame.K_UP:
            self.ship.flg_moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.flg_moving_dn = False

    def _check_play_btn( self, mouse_pos ):
        if self.play_btn.rect.collidepoint( mouse_pos ):
            #From 'Play' label in the start and 'Play again' btw sessions
            self.ai_settings.init_dyna_settings()
            self.stats.game_active = True #To hide button
            
            #Hide mouse right after click event on button rect 
            #which activates the game and hides button
            pygame.mouse.set_visible( False )

            self.scorecard.prep_ships()
            #_prep_do_over() Same as _alien_hit/_ship_hit...

    def _create_fleet( self ):
        """Setup a fleet of aliens"""
        self.flt += 1
        row = -1

        while( row < self.num_rows -1 ): #Row by row
            row += 1
            print( f"In row of { row } for fleet { self.flt }" )
            for seq in range( self.num_aliens_x ): #Room for sideway
                self._create_alien( self.flt, row, seq, self.a_wid, self.a_hgt )

    def _create_alien( self, fleet, row, seq, a_wid, a_hgt ):
        a = AI_Alien( self, fleet, row, seq )
        a_x = a_wid + 2 * a_wid * seq #a_wid is the defaul pos-x of alien
        a.rect.x = a_x
        a_y = a_hgt * 2 + 2 * a_hgt * row #a_hgt * 2 is alien's default pos-y
        a.rect.y = a_y
        self.aliens.add( a )

    def _check_fleet_edge( self ):
        for a in self.aliens:
            if a.hit_edge():
                self._fleet_repos()
                break

    def _fleet_repos( self ):
        #print( "Hit wall now" )
        #self.aliens.drop() #AttributeError: 'Group' object has no attribute 'drop'
        #for a in self.aliens.sprites():
        for a in self.aliens:
            a.drop()
        self.ai_settings.fleet_direction *= -1
        
        
    def _update_screen( self ): #Render latest location of all valid elements
        """Refresh screen"""
        self.screen.fill( self.ai_settings.bg_color ) #Apply intended bg color
        self.ship.blitme() #Place the ship on screen
        
        #for bullet in self.bullets.sprites():
        for bullet in self.bullets:
            #print( f"The type of bullete in group is { type( bullet ) }" )
            bullet.draw_itself()

        self.aliens.draw( self.screen ) #Batch call of the draw of image

        self.scorecard.show() #Show scorecard with latest score

        if not self.stats.game_active: #Show button when game not active
            self.play_btn.show()

        pygame.display.flip() #Visualize the recently updated screen/surface

    def _fire_bullet( self ):
        """Add a bullet into the Sprite group of bullets"""
        if len( self.bullets ) < self.ai_settings.bullet_allowed:
            self.bullets.add( AI_Bullet( self ) )

    def _update_bullets( self ):
        """Activity of all bullets during the game run"""
        self.bullets.update() #Gets triggered on all Sprite group memebers 
        
        for bullet in self.bullets.copy(): #Iterate over a copy for write oper
            if bullet.rect.bottom <= 0:
            #if bullet.rect.right >= self.screen.get_rect().width: #Horizontal
                self.bullets.remove( bullet ) #Take out out-of-bound bullets
        #print( f"Length of the group is, now, { len( self.bullets ) }" )
        
        self._check_collisions_bullets_aliens()

    def _check_collisions_bullets_aliens( self ):
        collision_bullets_aliens = pygame.sprite.groupcollide( self.bullets, 
                                    self.aliens, False, True )
        for aliens in collision_bullets_aliens.values():
            self.stats.score += self.ai_settings.alien_points * len( aliens )
            #for a in aliens:
                #pass
                #print( f"The { a.desc() } got hit" )
            self.scorecard.prep_score() #In-session score refresh on scorecard
            self.scorecard.check_high_score()

        if not self.aliens: #A fleet destroyed
            print( f"Done for fleet { self.flt }" )
            self.bullets.empty()
            self._create_fleet()

            #Level goes up with next fleet
            self.ai_settings.level_up()
            self.stats.lvl += 1
            self.scorecard.prep_lvl() #In-session level refresh on scorecard

    def _update_fleet( self ):
        """Activity of all aliens during the game run"""
        self.aliens.update() #Only update method can be triggered one for all?
        #self.aliens.update_x()
        self._check_fleet_edge() 
        
        a_h = pygame.sprite.spritecollideany( self.ship, self.aliens )
        if a_h: #Alien hits the ship
            print( f"Ship hit by { a_h.desc() }" )
            self._alien_hit()
        
        for a in self.aliens:
            if a.rect.bottom >= self.screen.get_rect().bottom: #lien hits bottom
                print( "Alien hit bottom" )
                self._alien_hit()
                break
        #Take out hit aliens after _update_bullets?

    def _alien_hit( self ): #_ship_hit
        """Refresh screen after a pause for next round of the session or 
        stop for session reset upon any alien hitting the ship or bottom"""
        #Decrement number of ships eligible for current session
        if self.stats.ship_num_left > 0: #Still got life left in the session
            self.stats.ship_num_left -= 1
            self._prep_do_over()
            self.scorecard.prep_ships() #Take out one immediately

            sleep( 1 ) #Prepare for next go-around
        else: #Done for the session
            self.stats.game_active = False #Game over to switch button text
            #Visualize button right after end of a session which inactivates
            #the game and resets game status as well as screen elements 
            #for next session upon a click event on the button
            pygame.mouse.set_visible( True )
            self._reset_play()
            #pass

    def _reset_play( self ):
        msg = 'Play again'
        self.play_btn.reset( msg )
        #Only right after game active flag switched off to end a session 
        #and before game active flag switched on by button to start a session
        #upon preparation of the screen by system
        self.stats.reset_stats()
        self.scorecard.prep_score() #Clear score in scorecard immediately
        self.scorecard.prep_lvl() #Clear level in scorecard immediately
        self._prep_do_over()

    def _prep_do_over( self ): 
        """ALL activities of game screen reset together for easy maintenace
        - executed only right after game-stopper and long before any other 
        activity, i.e. accident mouse click on the invisible button rect"""
        self.aliens.empty() #Clear remaining aliens out of screen
        self.bullets.empty() #Clear existing bullets out of screen

        self._create_fleet() #Get new fleets of aliens and reposition the ship
        self.ship.ready()

    def _quit_fullscreen( self ):
        self.ai_settings.scrn_width = self.ai_settings.scrn_width_def
        self.ai_settings.scrn_height = self.ai_settings.scrn_height_def
        self.screen = pygame.display.set_mode( 
            ( self.ai_settings.scrn_width, self.ai_settings.scrn_height ) )
        self.mode_fs = 'N'

    def _enter_fullscreen( self ):
        self.screen = pygame.display.set_mode( ( 0, 0 ), pygame.FULLSCREEN )
        self.ai_settings.scrn_width = self.screen.get_rect().width
        self.ai_settings.scrn_height = self.screen.get_rect().height
        self.mode_fs = 'Y'

    def _max_screen( self ): #Go to full screen mode?
        self.screen = pygame.display.set_mode( ( 0, 0 ), pygame.FULLSCREEN )
        self.ai_settings.scrn_width = self.screen.get_rect().width
        self.ai_settings.scrn_height = self.screen.get_rect().height
        self.mode_fs = 'Y'

    def _restore_screen( self ): #Back to default screen mode?
        self.ai_settings.scrn_width = self.ai_settings.scrn_width_def
        self.ai_settings.scrn_height = self.ai_settings.scrn_height_def
        self.screen = pygame.display.set_mode( 
            ( self.ai_settings.scrn_width, self.ai_settings.scrn_height ) )
        self.mode_fs = 'Y'


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()



#resize by the maximax/restor button on top right corner
#back to full screen
#button to pause game (p) that complicates matter for game_active
#DB connection to read/load/show high score

