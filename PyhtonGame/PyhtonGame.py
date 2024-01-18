from re import S, X
import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Game")

#define font
font = pygame.font.SysFont('Constantia', 30)

#define game variables
live_ball = False
margin = 50
playerScore = 0
playerTwoScore = 0
fps = 60
winner = 0

#define players
player = pygame.Rect((10, 250, 30, 150))
playerTwo = pygame.Rect((SCREEN_WIDTH - 40, 250, 30, 150))
speed = 5


#define colours
bg = (50, 20, 50)
red = (255, 0 , 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)


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
    
    if self.rect.bottom > SCREEN_HEIGHT:
       self.pongSpeedY += -1
    
    # collision with paddles (players)
    if self.rect.colliderect(player):
       self.pongSpeedX += 1
    if self.rect.colliderect(playerTwo):
       self.pongSpeedX += -1

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
     self.pongSpeedX = -4
     self.pongSpeedY = 4
     self.winner = 0 # 1 means P1 scored and 2 neans P2 scored  


pong = ball(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)

def controls():
   key = pygame.key.get_pressed()
  # player 1 controls scheme
   if key[pygame.K_w] and player.top > margin:
    player.move_ip(0, -1 * speed)
   elif key[pygame.K_s] and player.bottom < SCREEN_HEIGHT:
    player.move_ip(0, 1 * speed)
    
   # player 2 controls scheme
   elif key[pygame.K_UP] and playerTwo.top > margin:
    playerTwo.move_ip(0, -1 * speed)
   elif key[pygame.K_DOWN] and playerTwo.bottom < SCREEN_HEIGHT:
    playerTwo.move_ip(0, 1 * speed)

run = True
while run:
   
   fpsClock.tick(fps) 

   screen.fill((bg))
   # draw players
   pygame.draw.rect(screen, blue, player)
   pygame.draw.rect(screen, red, playerTwo)
   
   # draw margin
   pygame.draw.line(screen, white, (0, margin), (SCREEN_WIDTH, margin))
   
   # draw ball and live ball  
   if live_ball == True:
       winner = pong.move()
       if winner == 0:
         controls()
         pong.draw()
       elif winner != 0:
         live_ball == False
         if winner == 1:
           playerScore += 1
           pong.reset(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)
         elif winner == 2:
           playerTwoScore += 1
           pong.reset(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)

   
   print(winner)
   
   draw_text('P1: ' + str(playerScore), font, white, 20, 15)
   draw_text('P2: ' + str(playerTwoScore), font, white, SCREEN_WIDTH -100, 15)
   
   
   for event in pygame.event.get():
    if event.type == pygame.QUIT:
     run = False
    if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
       live_ball = True
       pong.reset(SCREEN_WIDTH - 60, SCREEN_HEIGHT // 2 + 50)
   
   pygame.display.update()
   
pygame.quit()