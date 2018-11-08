##-------------------------------------------------------------------
## Jumpy! Platformer game main code
## Dallas Spendelow
## November 8, 2018
## This file contains the main code running the game.
##-------------------------------------------------------------------


import pygame
import random
from settings import *
from sprites import *
from os import path

class Game:
    def __init__(self):
        ## Initialize game window, set FPS
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fontName = pygame.font.match_font(FONT_NAME)
        self.loadData()
    
    def loadData(self):
        ## Load high score
        self.directory = path.dirname(__file__)
        imageDirectory = path.join(self.directory, "image")
        with open(path.join(self.directory, HIGHSCORE_FILE), 'r') as f:
            try: 
                self.highScore = int(f.read())
            except:
                self.highScore = 0
        ## Load spritesheet image
        self.spritesheet = Spritesheet(path.join(imageDirectory, SPRITESHEET))
        
        ## Cloud images
        self.cloudImages = []
        for i in range(1,4):
            self.cloudImages.append(pygame.image.load(path.join(imageDirectory, 'cloud{}.png'.format(i))).convert())
               
        ## Load sounds
        self.soundDirectory = path.join(self.directory, "sound")
        self.jumpSound = pygame.mixer.Sound(path.join(self.soundDirectory, "Jump33.wav"))
        self.boostSound = pygame.mixer.Sound(path.join(self.soundDirectory, "Boost16.wav"))
    
    def new(self):
        ## Start a new game
        self.score = 0
        self.allSprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.player = Player(self)
        for platform in PLATFORM_LIST:
            Platform(self,*platform)
        self.mobTimer = 0
        pygame.mixer.music.load(path.join(self.soundDirectory, "HappyTune.ogg"))
        for i in range(8):
            c = Cloud(game)
            c.rect.y += 500
        self.run()

    def run(self):
        ## Game loop
        pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)
    
    def update(self):
        ## Update game loop
        self.allSprites.update()
        
        ## Spawn a mob?
        now = pygame.time.get_ticks()
        if now - self.mobTimer > 5000 + random.choice([-1000,-500,0,500,1000]):
            self.mobTimer = now
            Mob(self)
        
        ## Hit mobs?
        mobHits = pygame.sprite.spritecollide(self.player,self.mobs, False, pygame.sprite.collide_mask)
        if mobHits:
            self.playing = False
        
        ## Check if player hits a platform when falling
        if self.player.velocity.y > 0:      
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.position.x < lowest.rect.right + 10 and \
                   self.player.position.x > lowest.rect.left - 10:
                    if self.player.position.y < lowest.rect.centery:
                        self.player.position.y = lowest.rect.top 
                        self.player.velocity.y = 0
                        self.player.jumping = False
                    
        ## If the player reaches the top quarter of the screen
        if self.player.rect.top <= HEIGHT /4:
            if random.randrange(100) < 10:
                Cloud(self)
            self.player.position.y += max(abs(self.player.velocity.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.velocity.y/2), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.velocity.y), 2)
            for platform in self.platforms:
                platform.rect.y += max(abs(self.player.velocity.y), 2)
                if platform.rect.top >= HEIGHT:
                    platform.kill()
                    self.score += 10
        
        ## If player hits powerup
        powerupHits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerupHits:
            if powerup.type == 'boost':
                self.boostSound.play()
                self.player.velocity.y = -BOOST_POWER
                self.player.jumping = False
                
        
         
        ## Die, when falling off screen                          
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.allSprites:
                sprite.rect.y -= max(self.player.velocity.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
            
                    
        ## Spawn new platforms to keep the same number, roughly
        while len(self.platforms) < 6:
            width = random.randrange(50,100)            
            Platform(self, random.randrange(0, WIDTH-width),
                    random.randrange(-75, -30))


    def events(self):
        ## Events of the game loop
        for event in pygame.event.get():
            ## Check for closing window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jumpCut()
    
    def draw(self):
        ## Draw the game loop
        self.screen.fill(BGCOLOR)
        self.allSprites.draw(self.screen)
        self.drawText(str(self.score), 22, WHITE, WIDTH / 2, 15)
        ## Flip the display, so the user can see it.
        pygame.display.flip()

    def showStartScreen(self):
        ## Game start screen
        pygame.mixer.music.load(path.join(self.soundDirectory, "Yippee.ogg"))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.drawText(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Arrows to move, Space to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press a key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        self.drawText("High Score: " + str(self.highScore), 22, WHITE, WIDTH /2 , 15)
        pygame.display.flip()
        self.waitForKey()
        pygame.mixer.music.fadeout(500)
        
    def showGameOverScreen(self):
        ## Game over and continue
        if not self.running:
            return
        pygame.mixer.music.load(path.join(self.soundDirectory, "Yippee.ogg"))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.drawText("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.drawText("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.drawText("Press a key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        if self.score > self.highScore:
             self.highScore = self.score
             self.drawText("NEW HIGH SCORE!", 22, WHITE, WIDTH / 2 , HEIGHT / 2 + 40)
             with open(path.join(self.directory, HIGHSCORE_FILE), 'w') as f:
                 f.write(str(self.score))
        else:
            self.drawText("High Score: " + str(self.highScore), 22, WHITE, WIDTH /2 , HEIGHT / 2 + 40)
        pygame.display.flip()
        self.waitForKey()
        pygame.mixer.music.fadeout(500)
    
    def waitForKey(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def drawText(self, text, size, color, x, y):
        font = pygame.font.Font(self.fontName, size)
        textSurface = font.render(text, True, color)
        textRectangle = textSurface.get_rect()
        textRectangle.midtop = (x, y)
        self.screen.blit(textSurface, textRectangle)  
    

game = Game()
game.showStartScreen()
while game.running:
    game.new()
    game.showGameOverScreen()

pygame.quit()
    
