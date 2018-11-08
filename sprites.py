##-------------------------------------------------------------------
## Sprites for Jumpy! Platformer
## Dallas Spendelow
## November 8, 2018
## This file deals with sprites for the Jumpy! game. 
##-------------------------------------------------------------------

import pygame
from settings import *
from random import choice, randrange
vector = pygame.math.Vector2

class Spritesheet:
    ## Class for loading and parsing  spritesheet
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
        
    def getImage(self, x, y, width, height):
        ## Get an image out of a spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.currentFrame = 0
        self.lastUpdate = 0
        self.loadImages()
        self.image = self.standingFrames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.position = vector(40, HEIGHT - 100)
        self.velocity = vector(0, 0)
        self.acceleration = vector(0, 0)
        
    def loadImages(self):
        self.standingFrames = [self.game.spritesheet.getImage(614, 1063, 120, 191),
                               self.game.spritesheet.getImage(690, 406, 120, 201)]
        for frame in self.standingFrames:
            frame.set_colorkey(BLACK)
        self.walkFramesRight = [self.game.spritesheet.getImage(678, 860, 120, 201),
                                self.game.spritesheet.getImage(692, 1458, 120, 207)]
        
        for frame in self.walkFramesRight:
            frame.set_colorkey(BLACK)                            
        
        self.walkFramesLeft = []
        for frame in self.walkFramesRight:
            frame.set_colorkey(BLACK) 
            self.walkFramesLeft.append(pygame.transform.flip(frame, True, False))
            
        self.jumpFrame = self.game.spritesheet.getImage(382, 764, 150, 181)
        self.jumpFrame.set_colorkey(BLACK) 
        
    
    def jumpCut(self):
        if self.jumping:
            if self.velocity.y < -3:
                self.velocity.y = -3
    

    def jump(self):
        ## Jump only if standing on a platform
        self.rect.x += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jumpSound.play()
            self.jumping = True 
            self.velocity.y = -JUMP_COEFFICIENT
        
    def update(self):
        self.animate()
        self.acceleration = vector(0, GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acceleration.x = -PLAYER_ACCELERATION
        if keys[pygame.K_RIGHT]:
            self.acceleration.x = PLAYER_ACCELERATION
        
        ## Apply friction
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        
        ## Equations of motion for the player
        self.velocity += self.acceleration
        if abs(self.velocity.x) < 0.1:    ## If velocity drops below a threshold
            self.velocity.x = 0
        self.position += self.velocity + 0.5 * self.acceleration
        
        ## Wrap around the sides of the screen
        if self.position.x > WIDTH + self.rect.width / 2:
            self.position.x = 0 - self.rect.width / 2
        if self.position.x < 0 - self.rect.width / 2:
            self.position.x = WIDTH + self.rect.width / 2
        
        self.rect.midbottom = self.position
        
    def animate(self):
        now = pygame.time.get_ticks()
        if self.velocity.x != 0:
            self.walking = True
        else:
            self.walking = False
        ## Show walking animation
        if self.walking:
            if now - self.lastUpdate > 200:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.walkFramesLeft)
                bottom = self.rect.bottom
                if self.velocity.x > 0:
                    self.image = self.walkFramesRight[self.currentFrame]
                else:
                    self.image = self.walkFramesLeft[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom 
        
        ## Show idle animation
        if not self.jumping and not self.walking:
            if now - self.lastUpdate > 350:
                self.lastUpdate = now
                self.currentFrame = (self.currentFrame + 1) % len(self.standingFrames)
                bottom = self.rect.bottom
                self.image = self.standingFrames[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
        self.mask = pygame.mask.from_surface(self.image)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.allSprites, game.clouds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloudImages)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50,101)/100
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
                                            int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)
        
    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()
        
class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.allSprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.getImage(0, 288, 380, 94),
                  self.game.spritesheet.getImage(213, 1662, 201, 100)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POWERUP_SPAWN_PERCENTAGE:
            Powerup(self.game, self)
    
class Powerup(pygame.sprite.Sprite):
    def __init__(self, game, platform):
        self._layer = POWERUP_LAYER
        self.groups = game.allSprites, game.powerups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.platform = platform
        self.type = choice(['boost'])
        self.image = self.game.spritesheet.getImage(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5
    
    def update(self):
        self.rect.bottom = self.platform.rect.top-5
        if not self.game.platforms.has(self.platform):
            self.kill()
            
class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.allSprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.imageUp = self.game.spritesheet.getImage(566, 510, 122, 139)
        self.imageUp.set_colorkey(BLACK)
        self.imageDown = self.game.spritesheet.getImage(568, 1534, 122, 135)
        self.imageDown.set_colorkey(BLACK)
        self.image = self.imageUp
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.velocityX = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.velocityX *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.velocityY = 0
        self.differenceY = 0.5
        
    def update(self):
        self.rect.x += self.velocityX
        self.velocityY += self.differenceY
        if self.velocityY > 3 or self.velocityY < -3:
            self.differenceY *= -1
        center = self.rect.center
        if self.differenceY < 0:
            self.image = self.imageUp
        else:
            self.image = self.imageDown
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.velocityY
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()
