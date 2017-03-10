

import pygame
import random
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
DKGREEN = (0, 100, 0)
 


class Enemy(pygame.sprite.Sprite):
    #This class represents the block (enemies)

    def __init__(self):
        super(Enemy,self).__init__()

        self.image = pygame.image.load('enemySprite.jpg')
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]/6),int(self.size[1]/8)))

        self.rect = self.image.get_rect()
        

class Bullet(pygame.sprite.Sprite):
    #This class represents the bullet

    def __init__(self):
        super(Bullet,self).__init__()

        self.image = pygame.Surface([4,10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y -= 3
 
# This class represents the Ship
# It derives from the "Sprite" class in Pygame
class Ship(pygame.sprite.Sprite):
    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super(Ship,self).__init__()
 
        # Create an image of the ball, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.image.load('shipSprite.jpg')

        self.size = self.image.get_size()

        self.image = pygame.transform.scale(self.image, (int(self.size[0]/2),int(self.size[1]/3)))
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()
 
    # Update the position of the ship
    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()
        x = pos[0]
        #450 is bot of screen
        #350 is (currently) min y coordinate for ship
        if pos[1] > 450:
            y = 450
        elif pos[1] < 350:
            y = 350
        else:
            y = pos[1]
        
 
        # Set the attribute for the top left corner where this object is
        # located
        self.rect.x = x
        self.rect.y = y
 


#Initialize Game Clock

gameClock = 0

gameOver = False



pygame.init()



#Background Music

pygame.mixer.music.load('backgroundMusic.mp3')
pygame.mixer.music.set_endevent(pygame.constants.USEREVENT)
pygame.mixer.music.play()
 
# Set the height and width of the screen

screenWidth = 700
screenHeight = 500
screen = pygame.display.set_mode([screenWidth,screenHeight])
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# This is a list of 'sprites.' Each ship in the program (there is only 1) is
# added to this list. The list is managed by a class called 'Group.'
ships = pygame.sprite.Group()
 
ship = Ship()

# Add the ship to the list of player-controlled objects
ships.add(ship)


#List of enemies in the game
enemies = pygame.sprite.Group()

#List of bullets
bullets = pygame.sprite.Group()

#List of all sprites in game
allSprites = pygame.sprite.Group()

#create the enemies

for i in range(50):
    enemy = Enemy()

    enemy.rect.x = random.randrange(15,screenWidth - 15)
    enemy.rect.y = random.randrange(5,250)

    enemies.add(enemy)
    allSprites.add(enemy)    


#Initialize Score
score = 0

tickCount = 60

# -------- Main Program Loop -----------
while not done and not gameOver:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            bullet = Bullet()
            bullet.rect.x = ship.rect.x
            bullet.rect.y = ship.rect.y
            allSprites.add(bullet)
            bullets.add(bullet)
        elif event.type == pygame.constants.USEREVENT:
            pygame.mixer.music.load('backgroundMusic.mp3')
            pygame.mixer.music.play()

    #Move the enemies down the screen
    if gameClock > 100:
        gameClock = 0
        for enemy in enemies:
            enemy.rect.y += 10
            if enemy.rect.y > screenHeight:
                gameOver = True
                print "Game Over"

    allSprites.update()

    for bullet in bullets:

        enemiesHit = pygame.sprite.spritecollide(bullet, enemies, True)
    
        for enemy in enemiesHit:
            bullets.remove(bullet)
            allSprites.remove(bullet)
            score +=1
            print(score)

        if bullet.rect.y < -10:
            bullets.remove(bullet)
            allSprites.remove(bullet)

    # Clear the screen
    screen.fill(BLACK)
 
    # Update the position of the sprites (using the mouse) and draw the sprites
    ship.update()
    allSprites.add(ship)
    allSprites.draw(screen)
    
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    gameClock += 1
pygame.quit()
