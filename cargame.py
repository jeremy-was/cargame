# images are from https://www.flaticon.com/
# music from Mario :)

import pygame
from pygame.locals import *
import random
import math
import sys

pygame.mixer.init()
pygame.init()

class MainRun():
    def __init__(self):
        self.size = self.width, self.height = (900,800)
        self.road_w = int(self.width/1.35) # 1200/1.35 = 888

        self.roadmark_w = int(self.width/80) # 1400/80 = 17.5
        self.middle_lane = self.width/2
        self.right_lane = self.middle_lane + self.road_w/3 # (1400/2 = 700) + (875/4 = 218.75) = 918.75
        self.left_lane = self.middle_lane - self.road_w/3 # (1400/2 = 700) - (875/4 = 218.75) = 481.25
        
        self.middle_lane = int(self.middle_lane)
        self.right_lane = int(self.right_lane) # convert to int
        self.left_lane = int(self.left_lane) # convert to int

        self.running = True
        # self.game_start = False
        self.demo_running = False
        self.off_road = False

        # set window size
        self.screen = pygame.display.set_mode((self.size), pygame.RESIZABLE)
        # set title
        pygame.display.set_caption('JW Car Game')
        # load the images
        self.explosion_img = pygame.image.load('images/explosion3.png')

        self.pause_icon = pygame.image.load('images/pause.png')
        self.pause_icon_loc = self.pause_icon.get_rect()
        self.pause_icon_loc.center = self.width/2,self.height/2

        self.gameover_icon = pygame.image.load('images/gameover.png')
        self.gameover_icon_loc = self.gameover_icon.get_rect()
        self.gameover_icon_loc.center = self.width/2,self.height/4
        
        # load player car
        self.car = pygame.image.load('images/car.png')
        self.car_loc = self.car.get_rect()
        self.car_loc.center = self.left_lane, self.height*0.8 # 481.25,640
        # load other cars
        self.car2 = pygame.image.load('images/car2.png')
        self.car2_loc = self.car2.get_rect()
        self.car2_loc.center = self.right_lane, self.height*0.2 # 918.75,160

        # load trees # # # # # # # # # # # # # 
        self.tree_left1 = pygame.image.load('images/bush1.png')
        self.tree_left1_loc = self.car.get_rect()
        self.tree_left1_loc.center = self.left_lane/1.7, self.height*0.2 

        self.tree_left2 = pygame.image.load('images/bush2.png')
        self.tree_left2_loc = self.car.get_rect()
        self.tree_left2_loc.center = self.left_lane/1.6, self.height*0.4

        self.tree_left3 = pygame.image.load('images/bush3.png')
        self.tree_left3_loc = self.car.get_rect()
        self.tree_left3_loc.center = self.left_lane/1.7, self.height*0.6 

        self.tree_left4 = pygame.image.load('images/bush4.png')
        self.tree_left4_loc = self.car.get_rect()
        self.tree_left4_loc.center = self.left_lane/1.6, self.height*0.8

        self.tree_right1 = pygame.image.load('images/bush1.png')
        self.tree_right1_loc = self.car.get_rect()
        self.tree_right1_loc.center = self.right_lane*1.35, self.height*0.2 

        self.tree_right2 = pygame.image.load('images/bush2.png')
        self.tree_right2_loc = self.car.get_rect()
        self.tree_right2_loc.center = self.right_lane*1.37, self.height*0.4 

        self.tree_right3 = pygame.image.load('images/bush3.png')
        self.tree_right3_loc = self.car.get_rect()
        self.tree_right3_loc.center = self.right_lane*1.36, self.height*0.6 

        self.tree_right4 = pygame.image.load('images/bush4.png')
        self.tree_right4_loc = self.car.get_rect()
        self.tree_right4_loc.center = self.right_lane*1.36, self.height*0.8

        self.tree_speed = 2

        self.left_tree_list = [self.tree_left1_loc,self.tree_left2_loc]
        self.left_tree_list2 = [self.tree_left3_loc,self.tree_left4_loc]
        
        self.right_tree_list = [self.tree_right1_loc,self.tree_right2_loc]
        self.right_tree_list2 = [self.tree_right3_loc,self.tree_right4_loc]
        
        self.tree_func_count = 0

        # the two variables below control the alternating of list and list2
        # to get random trees both sides of the road
        self.left_tree_status = 'even'
        self.right_tree_status = 'even'

        self.car_count = 0
        self.car_speed = 5
        self.level = 1
        self.score = 0
        self.middle_direction = 0

        self.score_font = pygame.font.Font('freesansbold.ttf',30)#CHANGE FONT SIZES TO MAKE THEM RELATIVE
        self.level_font = pygame.font.Font('freesansbold.ttf',30)
        self.game_over_font = pygame.font.SysFont('chalkboard',30)
        self.demo_font = pygame.font.Font('freesansbold.ttf',16)
        self.ukraine_font = pygame.font.SysFont('chalkboard',22)
        
        self.left_text_x = (self.width/2-self.road_w/1.55)
        self.left_text_y = self.height/20
        
        self.right_text_x = (self.width/2+self.road_w/2+self.roadmark_w)
        self.right_text_y = self.height/20

        self.game_over_status = 0
        self.pause_status = 0
        self.demo_mode_status = 0

        self.moving_white_lines = True
        self.line1_y = -350
        self.line2_y = -150
        self.line3_y = 50
        self.line4_y = 250
        self.line5_y = 450
        self.line6_y = 650
        self.line7_y = 850
        self.line8_y = 1050
        self.line9_y = 1250
        self.line_height_list = [self.line1_y,self.line2_y,self.line3_y,self.line4_y,self.line5_y,self.line6_y,self.line7_y,self.line8_y,self.line9_y]

        # LOAD sound effects
        self.chime = pygame.mixer.Sound('sounds/chime.mp3')
        self.a_tone = pygame.mixer.Sound('sounds/a_tone.mp3')
        self.car_horn = pygame.mixer.Sound('sounds/car_horn.mp3')
        self.bike_horn = pygame.mixer.Sound('sounds/bike_horn.mp3')
        self.mario_theme = pygame.mixer.Sound('sounds/mario_theme.mp3')
        # self.bleep = pygame.mixer.Sound('sounds/bleep.mp3') #CAUSED ERROR - SEE BELOW
        self.tyre_screech = pygame.mixer.Sound('sounds/tyre_screeching.mp3') #CAUSED ERROR - SEE BELOW
        # self.car_crash = pygame.mixer.Sound('sounds/car_crash.mp3') #CAUSED ERROR - SEE BELOW
        #Warning: Xing stream size off by more than 1%, fuzzy seeking may be even more fuzzy than by design!

        self.horn_list = [self.car_horn,self.bike_horn]

        self.game_play()

    def show_score(self,x,y):
        self.score_text = self.score_font.render("Score",True,(255,255,255))
        self.score_value_no = self.score_font.render(str(self.score),True,(255,255,255))
        self.screen.blit(self.score_text,(x,y))
        if self.score <10:
            self.screen.blit(self.score_value_no,(x*2.5,y*2.5))
        elif self.score >=10:
            self.screen.blit(self.score_value_no,(x*2,y*2.5))

    def show_level(self,x,y,level_no):
        level_colour = 255,255,255
        if level_no == 21:
            level_colour = 255,255,100
            self.level_font = pygame.font.Font('freesansbold.ttf',36)
        else:
            level_colour = 255,255,255
        self.level_text = self.level_font.render("Level",True,(level_colour))
        self.level_value_no = self.level_font.render(str(level_no),True,(level_colour))
        self.screen.blit(self.level_text,(x,y))
        self.screen.blit(self.level_value_no,(x*1.05,y*2.5))
        if self.demo_running == True:
            self.demo_text = self.demo_font.render("Demo mode",True,(255,255,255))
            self.screen.blit(self.demo_text,(x,self.height*0.9))
        
    def game_over(self,x,y,car_speed):
        if car_speed ==0:
            self.screen.blit(self.gameover_icon, (x+self.road_w/14,y))
            pygame.mixer.Channel(2).play(self.tyre_screech)
            self.win_text = self.ukraine_font.render("Well done!",True,(255,255,255))
            self.screen.blit(self.win_text,(x+self.road_w/12,y*6))
            if self.car2_loc.center[0] == self.right_lane:
                x=self.middle_lane-self.road_w/9
                y=self.height/2
            elif self.car2_loc.center[0] == self.middle_lane:
                x=self.right_lane-self.road_w/9
                y=self.height/2
            else:
                x=self.middle_lane-self.road_w/9
                y=self.height/2/1.5
            self.text_play_again(x,y,'Play again?','y/n')
            self.bang_img_loc = (self.car_loc.center[1] + self.car2_loc.center[1])/2 # Find midpoint between 2 numbers
            self.show_explosion(self.car2_loc.center[0],self.bang_img_loc)
            self.game_over_status = 1

    def show_explosion(self,x,y):
        self.explosion_img_loc = self.explosion_img.get_rect()
        # self.explosion_img_loc.center = x,y
        self.explosion_img_loc.center = self.car2_loc.center
        self.screen.blit(self.explosion_img, self.explosion_img_loc)

    def text_play_again(self,x,y,text1='', text2=''):
        # self.button_font = pygame.font.Font('freesansbold.ttf', 5)
        self.text_line1 = self.game_over_font.render(text1, True, (255,255,255))
        self.screen.blit(self.text_line1, (x,y))
        if text2 != '':
            self.text_line2 = self.game_over_font.render(text2, True, (255,255,255))
            self.screen.blit(self.text_line2, (x+50, y+50))

    def tree_func(self):
        if self.tree_func_count ==0:
            self.left_random_tree = random.choice(self.left_tree_list)
            self.left_random_tree.center = self.left_lane/1.7, random.randint(-100,-0)

            self.right_random_tree = random.choice(self.right_tree_list)
            self.right_random_tree.center = self.right_lane*1.36, random.randint(-50,0)

            self.tree_func_count +=1

        else:
            if self.left_random_tree[1]>self.height/2 and self.left_tree_status == 'even':
                self.left_random_tree = random.choice(self.left_tree_list2)
                self.left_random_tree.center = self.left_lane/1.7, random.randint(-100,0)
                self.left_tree_status = 'odd'
            elif self.left_random_tree[1]>self.height/2 and self.left_tree_status == 'odd':
                self.left_random_tree = random.choice(self.left_tree_list)
                self.left_random_tree.center = self.left_lane/1.7, random.randint(-100,0)
                self.left_tree_status = 'even'

            if self.right_random_tree[1]>self.height/2 and self.right_tree_status == 'even':
                self.right_random_tree = random.choice(self.right_tree_list2)
                self.right_random_tree.center = self.right_lane*1.36, random.randint(-50,0)
                self.right_tree_status = 'odd'
            elif self.right_random_tree[1]>self.height/2 and self.right_tree_status == 'odd':
                self.right_random_tree = random.choice(self.right_tree_list)
                self.right_random_tree.center = self.right_lane*1.36, random.randint(-50,0)
                self.right_tree_status = 'even'

        for x in self.left_tree_list:
            if math.isclose(x[0], self.car_loc[0], abs_tol=2) and x[1] in range(self.car_loc[1]-600,self.car_loc[1]-200) and self.pause_status != 1:
                print('CAR HIT THE TREE')

    def pause_game(self):
        if self.pause_status == 0:
            self.last_car_speed = self.car_speed
            self.car_speed = 0
            self.last_tree_speed = self.tree_speed
            self.tree_speed = 0
            self.pause_status = 1
            self.screen.blit(self.pause_icon, self.pause_icon_loc)
            pygame.display.update()
            pygame.mixer.Channel(2).play(self.a_tone)
            pygame.mixer.Sound.stop(self.mario_theme)
            print('pause status 1')
            print(self.pause_icon_loc)
        else:
            self.pause_status = 0
            self.car_speed = self.last_car_speed
            self.tree_speed = self.last_tree_speed
            pygame.mixer.Channel(0).play(self.mario_theme, -1)
            print('pause status 0')

    def demo_mode(self):
        if self.demo_running == False:
            self.demo_running = True
        else:
            self.demo_running = False
    
    def off_road_mode(self):
        if self.off_road == False:
            self.car_loc.center = self.left_lane/3.6, self.height*0.8
            self.off_road = True
        else:
            self.car_loc.center = self.left_lane, self.height*0.8
            self.off_road = False

    def draw_road_lines(self):
        self.white_lines_left = ['self.left_line1', 'self.left_line2', 'self.left_line3', 'self.left_line4', 'self.left_line5', 'self.left_line6', 'self.left_line7', 'self.left_line8', 'self.left_line9']
        for x in range(len(self.white_lines_left)): # DRAW 9 WHITE LINES
            self.white_lines_left[x] = pygame.draw.rect(self.screen,(255,255,255),(self.width/2-self.road_w/2+self.road_w/3-self.roadmark_w/2,self.line_height_list[x], self.roadmark_w, self.height/7))

        self.white_lines_right = ['self.right_line1', 'self.right_line2', 'self.right_line3', 'self.right_line4', 'self.right_line5', 'self.right_line6', 'self.right_line7', 'self.right_line8', 'self.right_line9']
        for x in range(len(self.white_lines_right)): # DRAW 9 WHITE LINES
            self.white_lines_right[x] = pygame.draw.rect(self.screen,(255,255,255),(self.width/2+self.road_w/2-self.road_w/3-self.roadmark_w/2,self.line_height_list[x], self.roadmark_w, self.height/7))

    def move_repeat_road_lines(self):
        for x in range(len(self.line_height_list)):
            self.line_height_list[x] +=2
            if self.line_height_list[x] >1450:
                self.line_height_list[x]-=1800

    def moving_lines(self):
        if self.moving_white_lines == True:
            self.draw_road_lines()
            self.moving_white_lines = False
        else:
            self.move_repeat_road_lines()
            self.draw_road_lines()
    
    def game_play(self):
        pygame.mixer.Channel(0).play(self.mario_theme, -1) # -1 argument is so that it repeats
        while self.running:
            if math.isclose(self.car_loc[0], self.car2_loc[0], abs_tol=2) and self.car2_loc[1] in range(self.car_loc[1]-600,self.car_loc[1]-200) and self.pause_status != 1:
                pygame.mixer.Channel(1).play(self.car_horn)
            # animate other car
            if self.car_count>4 and self.level in range (1,21): # No faster than speed 25 - (unplayable)
                self.car_speed+=0.5
                self.level+=1
                self.car_count=0
                # pygame.mixer.Sound.play(self.bleep) # need a new level up beep
            self.car2_loc[1] += self.car_speed
            self.tree_left1_loc[1] += self.tree_speed
            self.tree_left2_loc[1] += self.tree_speed
            self.tree_left3_loc[1] += self.tree_speed
            self.tree_left4_loc[1] += self.tree_speed
            self.tree_right1_loc[1] += self.tree_speed
            self.tree_right2_loc[1] += self.tree_speed
            self.tree_right3_loc[1] += self.tree_speed
            self.tree_right4_loc[1] += self.tree_speed
            if self.car2_loc[1]>self.height:
                self.car_count +=1
                self.score +=1
                if random.randint(0,2) == 0:
                    self.car2_loc.center = self.left_lane, -100
                    if math.isclose(self.car_loc.center[0],int(self.left_lane), abs_tol=2) and math.isclose(self.car_loc.center[1],int(self.height*0.8),abs_tol=2) and self.demo_running:
                        self.car_loc = self.car_loc.move([int(self.road_w/3),0]) # 437.5,0
                elif random.randint(0,2) == 1:
                    self.car2_loc.center = self.middle_lane, -100
                    if math.isclose(self.car_loc.center[0],int(self.middle_lane), abs_tol=2) and math.isclose(self.car_loc.center[1],int(self.height*0.8),abs_tol=2) and self.demo_running:
                        if self.middle_direction ==0:
                            self.car_loc = self.car_loc.move([-int(self.road_w/3),0]) # 437.5,0
                            self.middle_direction =1
                        elif self.middle_direction ==1:
                            self.car_loc = self.car_loc.move([int(self.road_w/3),0]) # 437.5,0
                            self.middle_direction =0
                else:
                    self.car2_loc.center = self.right_lane, -100
                    if math.isclose(self.car_loc.center[0],int(self.right_lane), abs_tol=2) and math.isclose(self.car_loc.center[1],int(self.height*0.8),abs_tol=2) and self.demo_running:
                        self.car_loc = self.car_loc.move([-int(self.road_w/3),0]) # -437.5,0
            
            self.tree_func()

            ### END GAME ###
            if math.isclose(self.car_loc[0], self.car2_loc[0], abs_tol=2) and self.car2_loc[1] in range(self.car_loc[1]-200,self.car_loc[1]+150):
                self.car_speed=0
                pygame.mixer.Sound.stop(self.mario_theme)
            # event listeners
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    print('\nYou just clicked QUIT, bye bye!\n')
                if event.type == KEYDOWN and self.game_over_status ==1:
                    if event.key == K_n:
                        self.running = False
                        print('\nYou just hit "n", bye bye!\n')
                    if event.key in [K_y]:
                        self.play_again()
                if event.type == KEYDOWN and self.game_over_status ==0 and self.pause_status ==0: # while game NOT over and not paused
                    # if event.key in [K_a, K_LEFT] and self.car_loc.center == (int(self.right_lane), int(self.height*0.8)):
                    if event.key in [K_a, K_LEFT] and (math.isclose(self.car_loc.center[0],int(self.right_lane), abs_tol=2) or math.isclose(self.car_loc.center[0],int(self.middle_lane), abs_tol=2)) and math.isclose(self.car_loc.center[1],int(self.height*0.8),abs_tol=2):
                        self.car_loc = self.car_loc.move([-int(self.road_w/3),0])
                    if event.key in [K_d, K_RIGHT] and (math.isclose(self.car_loc.center[0],int(self.left_lane), abs_tol=2) or math.isclose(self.car_loc.center[0],int(self.middle_lane), abs_tol=2)) and math.isclose(self.car_loc.center[1],int(self.height*0.8),abs_tol=2):
                        self.car_loc = self.car_loc.move([int(self.road_w/3),0])
                    if event.key == K_o:
                        self.off_road_mode()
                    if event.key == K_7:
                        self.demo_mode()
                key_state = pygame.key.get_pressed() # so user can hold down keys for continuous press
                if key_state[pygame.K_0] and self.level <21:
                    self.level+=1
                    self.car_speed+=1
                if key_state[pygame.K_9] and self.level >1:
                    self.level-=1
                    self.car_speed-=1
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.pause_game()
                if event.type == KEYDOWN and event.key == K_q:
                    self.running = False
                    print('\nYou just hit "q", bye bye!\n')

            if self.pause_status !=1 and self.game_over_status !=1:
                ##### SET BACKGROUND colour
                self.screen.fill((0,153,0))
                ##### DRAW ROAD (rectangle)
                # (50,50,50) grey colour
                # (width/2-road_w/2) x value (horizonal value from where you start drawing the rectangle)
                # (0) y value (virtical value from where you start drawing the rectangle)
                # width of the rectangle
                # height of the rectangle
                pygame.draw.rect(self.screen,(50,50,50),(self.width/2-self.road_w/2, 0, self.road_w, self.height))
                
                self.moving_lines()

                ##### DRAW LEFT YELLOW LINE
                pygame.draw.rect(self.screen,(255,240,60),(self.width/2-self.road_w/2+self.roadmark_w,0,self.roadmark_w,self.height)) #800-500
                ##### DRAW RIGHT YELLOW LINE
                pygame.draw.rect(self.screen,(255,240,60),(self.width/2+self.road_w/2-self.roadmark_w*2,0,self.roadmark_w,self.height))

                self.screen.blit(self.tree_left1, self.tree_left1_loc)
                self.screen.blit(self.tree_left2, self.tree_left2_loc)
                self.screen.blit(self.tree_left3, self.tree_left3_loc)
                self.screen.blit(self.tree_left4, self.tree_left4_loc)

                self.screen.blit(self.tree_right1, self.tree_right1_loc)
                self.screen.blit(self.tree_right2, self.tree_right2_loc)
                self.screen.blit(self.tree_right3, self.tree_right3_loc)
                self.screen.blit(self.tree_right4, self.tree_right4_loc)

                self.screen.blit(self.car, self.car_loc) # screen.blit() a draw operation, takes image and location
                self.screen.blit(self.car2, self.car2_loc)
            
                self.show_score(self.left_text_x,self.left_text_y)
                self.show_level(self.right_text_x,self.right_text_y,self.level)
                self.game_over(self.car2_loc[0],self.height/25,self.car_speed)

            # moved this further up because it was causing blurring with constant overlays
            # if self.pause_status ==1:
            #     self.screen.blit(self.pause_icon, self.pause_icon_loc)
            
                pygame.display.update()

        # pygame.display.quit()
        pygame.quit()
        sys.exit(0) # to prevent the error on exit, pygame.error: video system not initialized

    def play_again(self):
        MainRun()

if __name__== '__main__':
    MainRun()


##################################################

# Maybe a central image for game over / play again
# clickable play_again
# 
# Make the blue car slide smoothly to the left or right, like red car drives smoothly
#
# Make more cars for variety
# Make more explosions for variety
#
##################################################
