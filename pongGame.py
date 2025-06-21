import pygame
class Game:
    def __init__(self):
        """Game loop flag variable"""
        self.left_player_score = 0
        self.right_player_score = 0
        self.running = True
        """Main window surface"""
        self.screen = None
        self.clock = None
        self.game_resolution = 1000,500
        """ Create a circle like surface inside the box of the circle"""
        self.ball_surface = None
        self.ball_position =  self.game_resolution[0] // 2, self.game_resolution[1] // 2   
        self.ball_speed = 3,3
        self.players_surface = None
        self.players_surface_dimensions = 10,100
        self.players_x_distance_to_borders = 100
        self.left_player_position = [self.players_x_distance_to_borders , self.game_resolution[1] // 2]
        self.right_player_position = [self.game_resolution[0] - (self.players_x_distance_to_borders + self.players_surface_dimensions[0]) , self.game_resolution[1] // 2]
        self.background = 0,0,0
        self.players_speed_per_frame = 10
    """ Method for executing game """
    def execute_game(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.game_resolution)
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()
        """ Define Players Surface """
        self.players_surface = pygame.Surface(self.players_surface_dimensions)
        """ Draw a red rectangle on """
        self.players_surface.fill((255,0,0,255))
        self.ball_surface = pygame.Surface((50,50),pygame.SRCALPHA)
        """ Draw on ball surface a circle """
        pygame.draw.circle(self.ball_surface,(255,0,0,255),(50,50),50)
        self.game_loop()
        self.end_game()
    def game_loop(self):
        while self.running:
            self.clock.tick(60)
            self.event_manager()
            self.render_screen()
            pass
    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.keys = pygame.key.get_pressed()
        """ Manage Players movement considering collisions on main screen """
        if self.keys[pygame.K_w]:
            if not(self.left_player_position[1] <= 0):
                self.left_player_position[1]-= self.players_speed_per_frame
        if self.keys[pygame.K_s]:
            if not(self.left_player_position[1] >= self.game_resolution[1]  - self.players_surface_dimensions[1]):
                self.left_player_position[1] += self.players_speed_per_frame
        if self.keys[pygame.K_UP]:
            if not(self.right_player_position[1] <= 0):
                self.right_player_position[1]-= self.players_speed_per_frame
        if self.keys[pygame.K_DOWN]:
            if not(self.right_player_position[1] >= self.game_resolution[1] - self.players_surface_dimensions[1]):
                self.right_player_position[1]+= self.players_speed_per_frame
    def render_screen(self):
        self.screen.fill(self.background)
        self.screen.blit(self.players_surface,self.left_player_position)
        self.screen.blit(self.players_surface,self.right_player_position)
        pygame.display.flip()
        """ self.screen.blit(self.ball_object,self.ball_position) """
    def end_game(self):
        pygame.quit()
pongGame = Game()
pongGame.execute_game()