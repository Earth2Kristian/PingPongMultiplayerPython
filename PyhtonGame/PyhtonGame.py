from re import S, X
import pygame
from pygame.locals import *
from pygame import mixer

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ping Pong 2P")

#define font
font = pygame.font.SysFont("monospace", 30)
gameStartFont = pygame.font.SysFont("monospace", 20)
gameStartFont2 = pygame.font.SysFont("monospace", 15)

#define game variables
live_ball = False
gameOver = True
margin = 50
marginB = 550
playerOneScore = 0
playerTwoScore = 0
fps = 60
winner = 0

#define players
playerOne = pygame.Rect((10, 250, 30, 100))
playerTwo = pygame.Rect((SCREEN_WIDTH - 40, 250, 30, 100))
speed = 5


#define colours
bg = (50, 20, 100)
red = (255, 0 , 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

#load sounds
beepSfx = pygame.mixer.Sound("sound/beep.wav")
beepSfx.set_volume(0.5)
goalSfx = pygame.mixer.Sound("sound/goal.wav")
goalSfx.set_volume(0.5)

#define texts
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y) )
  

class ball():
   def __init__(self, x, y):
    self.reset(x, y)
    
   def move(self):
    
    # collision detection
    if self.rect.top < margin:
       self.pongSpeedY += 1
       beepSfx.play()
    
    if self.rect.bottom > marginB:
       self.pongSpeedY += -1
       beepSfx.play()
    
    # collision with paddles (players)
    if self.rect.colliderect(playerOne):
       self.pongSpeedX += 1
       beepSfx.play()
    if self.rect.colliderect(playerTwo):
       self.pongSpeedX += -1
       beepSfx.play()

    # if the ball is out of bounds       
    if self.rect.right > SCREEN_WIDTH:
      self.winner = 1
      
    if self.rect.left < 0:
       self.winner = 2
    
    self.rect.x += self.pongSpeedX
    self.rect.y += self.pongSpeedY
    
    return self.winner
    
   def draw(self):
    pygame.draw.circle(screen, white, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius), self.ball_radius)
   
   def reset(self, x, y):
     self.x = x
     self.y = y
     self.ball_radius = 8
     self.rect = Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
     self.pongSpeedX = -6
     self.pongSpeedY = 6
     self.winner = 0 # 1 means P1 scored and 2 means P2 scored  


pong = ball(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)

def controls():
   key = pygame.key.get_pressed()
   key2 = pygame.key.get_pressed()
  # player 1 controls scheme
   if key[pygame.K_w] and playerOne.top > margin:
    playerOne.move_ip(0, -1 * speed)
   elif key[pygame.K_s] and playerOne.bottom < marginB:
    playerOne.move_ip(0, 1 * speed)
    
   # player 2 controls scheme
   if key2[pygame.K_UP] and playerTwo.top > margin:
    playerTwo.move_ip(0, -1 * speed)
   elif key2[pygame.K_DOWN] and playerTwo.bottom < marginB:
    playerTwo.move_ip(0, 1 * speed)

run = True
while run:
   
   fpsClock.tick(fps) 

   screen.fill((bg))
   # draw players
   pygame.draw.rect(screen, blue, playerOne)
   pygame.draw.rect(screen, red, playerTwo)
   
   # draw margin
   pygame.draw.line(screen, white, (0, margin), (SCREEN_WIDTH, margin))
   pygame.draw.line(screen, white, (0, marginB), (SCREEN_WIDTH, marginB))
   
   # draw ball and live ball  
   if live_ball == True:
       winner = pong.move()
       if winner == 0:
         controls()
         pong.draw()
       elif winner != 0:
         live_ball == False
         if winner == 1:
           playerOneScore += 1
           print("Player 1 Scored")
           goalSfx.play()
           if playerOneScore < 7:
             pong.reset(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)
         elif winner == 2:
           playerTwoScore += 1
           print("Player 2 Scored")
           goalSfx.play()
           if playerTwoScore < 7:
             pong.reset(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)
   
   # Just to avoid the increasing bug after 7
   if playerOneScore >= 7:
      playerOneScore = 7
      goalSfx.stop()
   if playerTwoScore >= 7:
      playerTwoScore = 7
      goalSfx.stop()
        
   # create score text
   draw_text('P1: ' + str(playerOneScore), font, white, 20, 15)
   draw_text('P2: ' + str(playerTwoScore), font, white, SCREEN_WIDTH -100, 15)
   draw_text("FIRST PLAYER GETS TO 7 WINS THE GAME", gameStartFont, white, 180, 560)   


   # create text if the game hasn't started yet
   if live_ball == False:
       draw_text("CLICK THE LEFT MOUSE BUTTON TO START THE GAME", gameStartFont, white, 130, 250)
     
       draw_text("CONTROLS SCHEME:", gameStartFont2, white, 20, 430)
       draw_text("P1: PRESS KEY BUTTON W OR S TO MOVE", gameStartFont2, white, 20, 450)
       draw_text("P2: PRESS KEY BUTTON UP OR DOWN TO MOVE", gameStartFont2, white, 20, 470)
       
   # create text if player 1 gets up to 7
   if live_ball == True and playerOneScore >= 7:
      gameOver = True 
      draw_text("PLAYER 1 WINS", gameStartFont, white, 300, 300)
      draw_text("PRESS R TO RESTART", gameStartFont, white, 300, 350)
      print("Player 1 Wins")

   # create text if player 2 gets up to 7
   if live_ball == True and playerTwoScore >= 7:
      gameOver = True
      draw_text("PLAYER 2 WINS", gameStartFont, white, 300, 300)
      draw_text("PRESS R TO RESTART", gameStartFont, white, 300, 350)
      print("Player 2 Wins")
      

   if gameOver == True:
      key = pygame.key.get_pressed()
      if key[pygame.K_r]:
        pong.reset(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)
        playerOneScore = 0
        playerTwoScore = 0
        print("Restart")
   
   
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
     run = False
    if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False and gameOver == True:
       live_ball = True
       gameOver = False
       pong.reset(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)
   
   pygame.display.update()
   
pygame.quit()