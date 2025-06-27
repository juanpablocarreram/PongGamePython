import pygame
import random
import time
import math
class Game:
    def __init__(self):
        """Game loop flag variable"""
        self.left_player_score = 0
        self.right_player_score = 0
        self.running = False
        """Main window surface"""
        self.game_resolution = 1280,720
        self.screen = pygame.display.set_mode(self.game_resolution)
        self.clock = pygame.time.Clock()
        self.minimum_horizontal_speed = .014
        self.initial_direction_choice = [self.game_resolution[0] * self.minimum_horizontal_speed,-self.game_resolution[0] *self.minimum_horizontal_speed]
        """ Create a circle like surface inside the box of the circle"""
        self.ball_surface_dimensions = self.game_resolution[0] * .02, self.game_resolution[0] *.02
        self.ball_surface = pygame.Surface(self.ball_surface_dimensions,pygame.SRCALPHA)
        self.ball_position = None
        self.ball_speed = None
        self.ball_speed_bonus_when_player = self.game_resolution[0] * .02
        self.ball_desaceleration = None
        self.max_vertical_speed = self.game_resolution[1] *.01
        self.players_surface_dimensions = self.game_resolution[0] *.01, self.game_resolution[1] * .18
        self.players_surface = pygame.Surface(self.players_surface_dimensions)
        self.players_x_distance_to_borders = self.game_resolution[0] *.12
        self.background = 0,0,0
        self.players_speed_per_frame = self.game_resolution[1] *.021
        self.object_color = 255,255,255,255
        self.players_surface.fill(self.object_color)
        self.score_distance_to_borders = self.game_resolution[0] * .15, self.game_resolution[1] * .05
        self.recent_left_player_point = False
        self.recent_player_point = 0
        self.is_game_closed = False
        self.speed_menu = False
        self.is_exit_menu_active = False
        self.is_game_paused = False
        self.pause_image = pygame.image.load("assets/pauseimage.png").convert_alpha()
        self.pause_image = pygame.transform.scale(self.pause_image, (self.game_resolution[0] *.1,self.game_resolution[0] *.1))
        self.pause_image_dimensions = self.pause_image.get_size()
        self.mid_line_surface_dimension = self.game_resolution[0] * .01, self.game_resolution[1]
        self.mid_line_surface = pygame.Surface(self.mid_line_surface_dimension)
        self.mid_line_surface.fill(self.object_color)
        self.pause_image_rect = self.pause_image.get_rect(topleft = (self.game_resolution[0] //2 - self.pause_image_dimensions[0]// 2, self.game_resolution[1] * .05))
        pygame.draw.circle(self.ball_surface,self.object_color,(self.ball_surface_dimensions[0]//2,self.ball_surface_dimensions[1]//2),self.ball_surface_dimensions[0]//2)
    """ Method for executing game """
    def execute_game(self):
        pygame.init()
        pygame.display.set_caption("Pong Game")
        self.font = pygame.font.SysFont(None,math.ceil(self.game_resolution[0] * .15))
        """ Draw on ball surface a circle (surface,color,center of circle, radius)"""
        self.charge_menu()
        self.game_loop()
    def charge_menu(self):
        self.initial_game_position()
        self.render_screen()
        while not self.running:
            self.clock.tick(30)
            self.event_manager()
            if self.is_game_closed:
                self.running = True
    def game_loop(self):
        while self.running:
            self.clock.tick(60)
            self.event_manager()
            while self.is_game_paused:
                self.event_manager()
            if self.is_game_closed:
                pygame.quit()
                return 'Game Ended succesfully'
            self.player_movement_logic()
            if self.recent_player_point == 0:
                self.ball_movement_logic()
            else:
                self.recent_player_point-= 1
            self.render_screen()
        self.charge_menu()
        self.game_loop()
    def event_manager(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 self.is_game_closed = True 
            if event.type == pygame.KEYDOWN:
                self.is_exit_menu_active = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.running and not self.is_exit_menu_active:
                mouse_pos = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(mouse_pos[0],mouse_pos[1],1,1)
                if self.is_game_paused:
                    if mouse_rect.colliderect(self.menu_buttons_rect[0]) or mouse_rect.colliderect(self.menu_buttons_rect[1]) :
                       self.is_game_paused = False
                    if mouse_rect.colliderect(self.menu_buttons_rect[1]):
                        self.is_game_closed = True
                if self.pause_image_rect.colliderect(mouse_rect) and not self.is_game_paused:
                    self.is_game_paused = True
                    self.render_menu_logic(["Resume Game","Exit Game"])
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.running and not self.is_exit_menu_active:
                mouse_pos = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(mouse_pos[0],mouse_pos[1],1,1)
                if not self.speed_menu:
                    """ Main Menu Buttons Handlers """
                    if mouse_rect.colliderect(self.menu_buttons_rect[0]):
                        self.speed_menu = True
                        self.render_menu_logic(["Return Main Menu","Slow","Fast"])
                    if mouse_rect.colliderect(self.menu_buttons_rect[1]):
                        self.running = True
                    if mouse_rect.colliderect(self.menu_buttons_rect[2]):
                        self.is_game_closed = True
                else:
                    """Speed Menu Button Handlers"""
                    if mouse_rect.colliderect(self.menu_buttons_rect[0]) or mouse_rect.colliderect(self.menu_buttons_rect[1]) or mouse_rect.colliderect(self.menu_buttons_rect[2]):
                        self.speed_menu = False
                        self.render_menu_logic(["Change Ball Speed","Play","Exit Game"])
                    if mouse_rect.colliderect(self.menu_buttons_rect[1]):
                        self.minimum_horizontal_speed = .01
                        self.initial_direction_choice = [self.game_resolution[0] * self.minimum_horizontal_speed,-self.game_resolution[0] *self.minimum_horizontal_speed]
                        self.ball_speed = [random.choice(self.initial_direction_choice),0]
                    if mouse_rect.colliderect(self.menu_buttons_rect[2]):
                        self.minimum_horizontal_speed = .014
                        self.initial_direction_choice = [self.game_resolution[0] * self.minimum_horizontal_speed,-self.game_resolution[0] *self.minimum_horizontal_speed]
                        self.ball_speed = [random.choice(self.initial_direction_choice),0]
    def player_movement_logic(self):
        self.keys = pygame.key.get_pressed()
        """ Manage Players movement considering collisions on main screen limits"""
        """ Set left player key configs """
        if self.keys[pygame.K_w]:
            if not(self.left_player_position[1] <= 0):
                self.left_player_position[1]-= self.players_speed_per_frame
        if self.keys[pygame.K_s]:
            if not(self.left_player_position[1] >= self.game_resolution[1]  - self.players_surface_dimensions[1]):
                self.left_player_position[1] += self.players_speed_per_frame
        """ Set right player key configs """
        if self.keys[pygame.K_UP]:
            if not(self.right_player_position[1] <= 0):
                self.right_player_position[1]-= self.players_speed_per_frame
        if self.keys[pygame.K_DOWN]:
            if not(self.right_player_position[1] >= self.game_resolution[1] - self.players_surface_dimensions[1]):
                self.right_player_position[1]+= self.players_speed_per_frame
    def initial_game_position(self):
        self.left_player_position = [self.players_x_distance_to_borders , self.game_resolution[1] // 2 - self.players_surface_dimensions[1] //2]
        self.right_player_position = [self.game_resolution[0] - (self.players_x_distance_to_borders + self.players_surface_dimensions[0]) ,self.game_resolution[1] // 2 - self.players_surface_dimensions[1]//2]
        self.ball_position = [self.game_resolution[0]//2 - self.ball_surface_dimensions[0] // 2,self.game_resolution[1]//2 - self.ball_surface_dimensions[1] //2]
        if self.ball_speed is None:
            self.ball_speed = [random.choice(self.initial_direction_choice),0]
        else:
            if self.recent_left_player_point:
                self.ball_speed = [self.initial_direction_choice[0],self.max_vertical_speed * random.uniform(-1,1)]
            else:
                self.ball_speed = [self.initial_direction_choice[1],self.max_vertical_speed * random.uniform(-1,1)]
            self.recent_player_point = 30
    def ball_movement_logic(self):
        self.collision_with_player()
        self.collision_with_limits()
        """Change the position with corrected ball speed"""
        self.ball_position[0] += self.ball_speed[0]
        self.ball_position[1] += self.ball_speed[1]
        self.ball_surpasses_player()
    def collision_with_limits(self):
        """ Manage collision with border walls"""
        if self.ball_position[1] <= 0 or self.ball_position[1] >= (self.game_resolution[1] - self.ball_surface_dimensions[1]):
            self.ball_speed[1] = -(self.ball_speed[1])
    def collision_with_player(self):
        """ Detect a collision before changing position"""
        left_player_rect = self.players_surface.get_rect(topleft = self.left_player_position)
        right_player_rect = self.players_surface.get_rect(topleft = self.right_player_position)
        ball_rect = self.ball_surface.get_rect(topleft = self.ball_position)
        has_ball_collided_left_player = ball_rect.colliderect(left_player_rect) 
        has_ball_collided_right_player = ball_rect.colliderect(right_player_rect)
        """ Reduce bonification speed"""
        if self.ball_speed[0] > self.game_resolution[0] *self.minimum_horizontal_speed or self.ball_speed[0] < self.game_resolution[0] *-self.minimum_horizontal_speed:
            self.ball_speed[0] += self.ball_desaceleration  
            """GRADUAL REDUCTION OF X_SPEED_PENDING"""
            pass
        """ Change direction of ball when colliding with a player"""       
        if has_ball_collided_left_player:
            middle_vertical_ball_position = self.ball_position[1] + (self.ball_surface_dimensions[1] //2)
            """ Percentage of bonification speed is calculated based on the difference between the middle of the rect and the middle coordinate of the ball"""
            percentage_of_difference= ((self.left_player_position[1] + self.players_surface_dimensions[1] //2) - middle_vertical_ball_position) / (self.players_surface_dimensions[1]//2)
            bonus_speed = abs(self.ball_speed_bonus_when_player * abs(abs(percentage_of_difference) -1))
            self.ball_speed[0] = abs(self.ball_speed[0]) + bonus_speed
            self.ball_speed[1] = self.max_vertical_speed * -(percentage_of_difference) +  self.max_vertical_speed * random.uniform(-.2,.2)
            self.ball_desaceleration = -(bonus_speed/30)
            self.recent_left_player_point = True
            """DETERMINING VERTICAL DIRECTION AND HORIZONTAL TEMPORAL BONIFICATION SPEED (PENDING TASK)"""
        if has_ball_collided_right_player:
            middle_vertical_ball_position = self.ball_position[1] + (self.ball_surface_dimensions[1] //2)
            percentage_of_difference = ((self.right_player_position[1] + self.players_surface_dimensions[1] //2) - middle_vertical_ball_position) / (self.players_surface_dimensions[1]//2)
            bonus_speed = abs(self.ball_speed_bonus_when_player * abs(abs(percentage_of_difference) -1))
            self.ball_speed[0] = -(abs(self.ball_speed[0]) + bonus_speed)
            self.ball_speed[1] = self.max_vertical_speed * -(percentage_of_difference) + self.max_vertical_speed * random.uniform(-.2,.2)
            self.ball_desaceleration = bonus_speed/30
            """DETERMINING VERTICAL DIRECTION AND HORIZONTAL TEMPORAL BONIFICATION SPEED (PENDING TASK)"""
            self.recent_left_player_point = False
    def ball_surpasses_player(self):
        if self.ball_position[0] + self.ball_surface_dimensions[0] <= 0:
            self.right_player_score += 1
            self.initial_game_position()
        if self.ball_position[0] >= self.game_resolution[0]:
            self.left_player_score +=1
            self.initial_game_position()
        """ END OF A GAME """
        if self.left_player_score == 10:
            self.winner = "Left"
        if self.right_player_score == 10:
            self.winner ="Right"
        if self.left_player_score == 10 or self.right_player_score == 10:
            self.running = False
            self.exit_menu()
            self.left_player_score, self.right_player_score = 0,0
    def render_screen(self):
        self.screen.fill(self.background)
        self.screen.blit(self.players_surface,self.left_player_position)
        self.screen.blit(self.players_surface,self.right_player_position)
        self.screen.blit(self.mid_line_surface,(self.game_resolution[0] // 2 - self.mid_line_surface_dimension[0] // 2,0))
        self.left_text_score_surface = self.font.render(f"{self.left_player_score}",True,self.object_color)
        self.right_text_score_surface = self.font.render(f"{self.right_player_score}",True,self.object_color)
        self.left_player_score_surface_dimensions = self.left_text_score_surface.get_size()
        self.right_player_score_surface_dimensions = self.right_text_score_surface.get_size()
        self.screen.blit(self.left_text_score_surface, (self.score_distance_to_borders[0],self.score_distance_to_borders[1]))
        self.screen.blit(self.right_text_score_surface,(self.game_resolution[0] - (self.score_distance_to_borders[0] + self.right_player_score_surface_dimensions[0]), self.score_distance_to_borders[1]))
        if self.running:
            self.screen.blit(self.ball_surface,self.ball_position)
            """ Insert Pause Button """
            self.screen.blit(self.pause_image,self.pause_image_rect)
        else:
           self.render_menu_logic(["Change Ball Speed","Play","Exit Game"])
        pygame.display.flip()
    def render_menu_logic(self,button_string_list):
        """ Menu Buttons Appearance """
        number_buttons_menu = len(button_string_list)
        total_vertical_space_for_buttons = .6
        self.menu_button_surface_dimensions = self.game_resolution[0] *.5 , self.game_resolution[1] * (total_vertical_space_for_buttons / number_buttons_menu)
        menu_buttons_margin =((1 - total_vertical_space_for_buttons) / (number_buttons_menu + 1)) * self.game_resolution[1]
        self.menu_button_surface = pygame.Surface(self.menu_button_surface_dimensions)
        self.menu_button_surface.fill(self.object_color)
        self.menu_buttons_rect = {} 
        for i in range(number_buttons_menu):
            actual_top_left_corner = (self.game_resolution[0] // 2 - self.menu_button_surface_dimensions[0]//2) , menu_buttons_margin *(i + 1) + self.menu_button_surface_dimensions[1] * i
            self.screen.blit(self.menu_button_surface,actual_top_left_corner)
            self.menu_buttons_rect[i] = self.menu_button_surface.get_rect(topleft = actual_top_left_corner)
            """ Calculate optimal font size """
            text_size = 1
            buttons_text_fonts = pygame.font.SysFont(None,text_size)
            text_surface = buttons_text_fonts.render(button_string_list[i], True, (0, 0, 0))
            text_dimensions = 0,0
            while text_dimensions[0] < self.menu_button_surface_dimensions[0] //2 and text_dimensions[1] < self.menu_button_surface_dimensions[1]//2:
                text_size+=15
                buttons_text_fonts = pygame.font.SysFont(None,text_size)
                text_surface = buttons_text_fonts.render(button_string_list[i], True, (0, 0, 0))
                text_dimensions = text_surface.get_size()
            self.screen.blit(text_surface,(self.menu_buttons_rect[i].center[0] - text_dimensions[0] // 2,self.menu_buttons_rect[i].center[1] - text_dimensions[1]//2))
        pygame.display.flip()
    def exit_menu(self):
        winner_text_surface =  self.font.render(f"{self.winner} Player Wins!",True,self.object_color)
        winner_text_surface_dimensions = winner_text_surface.get_size()
        return_text_font = pygame.font.SysFont(None,math.ceil(self.game_resolution[0] *.05))
        return_text_surface =  return_text_font.render(f"Press any key to return to main menu",True,self.object_color)
        return_text_surface_dimensions = return_text_surface.get_size()
        self.screen.blit(winner_text_surface,(self.game_resolution[0] // 2 - winner_text_surface_dimensions[0] //2, self.game_resolution[1] *.2))
        self.screen.blit(return_text_surface,(self.game_resolution[0] // 2 - return_text_surface_dimensions[0] //2, self.game_resolution[1] *.4))
        pygame.display.flip()
        self.is_exit_menu_active = True
        while self.is_exit_menu_active:
            self.event_manager()
pongGame = Game()
pongGame.execute_game()