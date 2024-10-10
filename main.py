import pygame
import random

# initialize game
pygame.init()

# general game variables
FPS = 60
player_lives = 3
zombie_and_cacti_speed = 5
bullet_speed = 5

# jump variables
jumping = False
velocity_y = 0
gravity = 1
jump_height = -15

# set up screen size and game name
WIDTH = 800
HEIGHT = 600
RESOLUTION = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(RESOLUTION)

pygame.display.set_caption("Megaman Zombie Shooter")

# load in sprites and background
BULLET = pygame.image.load('images/bullet.png')
CACTUS = pygame.image.load('images/cactus.png')
ZOMBIE = pygame.image.load('images/zombie.png')
PLAYER_LIVE = pygame.image.load('images/heart2.0.png')
BACKGROUND = pygame.image.load('images/background.png')
PLAYER_CHARACTER = pygame.image.load('images/megaman.png')

# upscaling of player_character to match resolution
player_new_width = PLAYER_CHARACTER.get_width() * 3
player_new_height = PLAYER_CHARACTER.get_height() * 3
PLAYER_CHARACTER = pygame.transform.scale(PLAYER_CHARACTER, (player_new_width, player_new_height))

# def player character x, y position bottom left of screen 
player_width = player_new_width
player_height = player_new_height

player_x = WIDTH * 0.1
player_y = HEIGHT - player_height
ground_y = HEIGHT - player_height # def ground level y

# upscaling of bullet 
bullet_new_width = BULLET.get_width() * 3
bullet_new_height = BULLET.get_height() * 3
BULLET = pygame.transform.scale(BULLET, (bullet_new_width, bullet_new_height))

bullet_width = bullet_new_width
bullet_height = bullet_new_height

# bullet class 
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = BULLET

    def move(self):
        self.x += bullet_speed

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def off_screen(self):
        return self.x > WIDTH

# list to hold bullets
bullets = []

# upscaling hearts
heart_new_width = PLAYER_LIVE.get_width() * 2
heart_new_height = PLAYER_LIVE.get_height() * 2
PLAYER_LIVE = pygame.transform.scale(PLAYER_LIVE, (heart_new_width, heart_new_height))

# set up font and variables for displaying time alive in seconds
font = pygame.font.Font('Press_Start_2P/PressStart2P-Regular.ttf', 15)
start_time = pygame.time.get_ticks()  # record the start time
elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # convert to seconds

# main game loop
game_running = True
clock = pygame.time.Clock()

while game_running:
    # init background with image 
    screen.blit(BACKGROUND, (0,0))

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # detect space key press once
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + (player_width * 0.95)
                bullet_y = player_y + (player_height * 0.37)
                bullets.append(Bullet(bullet_x, bullet_y))

    # get keys pressed
    keys = pygame.key.get_pressed()

    # jump logic
    if not jumping:
        if keys[pygame.K_UP]:
            jumping = True
            velocity_y = jump_height
    
    # apply gravity
    if jumping:
        player_y += velocity_y
        velocity_y += gravity

        # stop jumping when player reaches the ground
        if player_y >= ground_y:
            player_y = ground_y
            jumping = False
    
    # move and draw bullets
    for bullet in bullets:
        bullet.draw(screen)
        bullet.move()
        
    # remove bullet once off screen
        if bullet.off_screen():
            bullets.remove(bullet)

    # draw character on screen
    screen.blit(PLAYER_CHARACTER, (player_x, player_y))

    # draw players hearts
    for i in range(player_lives):
        screen.blit(PLAYER_LIVE, (WIDTH - 40 - i * 40, 10)) # top right position

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()