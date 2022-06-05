import pygame

class GameStats:
    """Track status of the Alien Invasion game"""
    
    def __init__( self, ai_game ): #Attributes not getting rest across sessions
        """Prep for game status instance by calling stats initialization def"""
        self.ai_seetings = ai_game.ai_settings
        self.reset_stats()
        self.game_active = False #Linked to the button and game eligibility
        self.high_score = 0

    #Called by __init__ at the start of the game or AlienInvasion anytime
    def reset_stats( self ): #Attributes that need to be reset for each session
        """Initialize/reset statistics for the game"""
        self.ship_num_left = self.ai_seetings.ship_num_left
        self.score = 0
        self.lvl = 1
