##-------------------------------------------------------------------
## Platformer Settings
## Dallas Spendelow
## Novemeber 8, 2018
## Settings for the platformer game.
##-------------------------------------------------------------------

## Game window sizes, as well as frames per second.
TITLE = "Jumpy!"
WIDTH = 480  
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HIGHSCORE_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"
        

## Player properties
PLAYER_ACCELERATION = 0.5
PLAYER_FRICTION = -0.12
GRAVITY = 0.5        ## Acceleration due to gravity. Just a coefficient.
                     ## Doesn't use units or anything like that.
                     ## 0.5 is a reasonable normal. 
JUMP_COEFFICIENT = 20      ## Controls jump speed, and thus how high a jump is.


## Game Properties
BOOST_POWER = 60
POWERUP_SPAWN_PERCENTAGE = 7
MOB_FREQUENCY = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POWERUP_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

## Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),(WIDTH / 2-50, HEIGHT * 3/4),
                 (WIDTH / 4, HEIGHT / 3), (5/6*WIDTH, 1/2*HEIGHT),
                 (2/3*WIDTH, 1/8*HEIGHT)]


## Give some colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
LIGHTBLUE = (51,153,255)
BGCOLOR = LIGHTBLUE