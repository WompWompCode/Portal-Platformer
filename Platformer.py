import pygame

pygame.init()

run = True
windowWidth = 1920
windowHeight = 1080
win = pygame.display.set_mode((windowWidth,windowHeight))
font = pygame.font.SysFont("comic sans", 30)
level = 1
levelLoaded = False


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.grounded = False
        
    def draw(self):
        return pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))


playerOne = Player(200, 100, 50, 75)

class Terrain:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self):
        return pygame.draw.rect(win, (0, 0, 200), (self.x, self.y, self.width, self.height))

Terrains = []

while run:
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        playerOne.x -= 5
        
    if keys[pygame.K_d]:
        playerOne.x += 5
    
    if playerOne.grounded == True:
        if keys[pygame.K_SPACE]:
            playerOne.y -= 300
    
    
    if levelLoaded == False:    
        match level:
            case 1:
                Terrains = []
                Terrains.append(Terrain(0, 780, 2000, 300))
                levelLoaded = True
                
                
    playerOne.grounded = False    
    for terrain in Terrains:
        if playerOne.y+playerOne.height >= terrain.y:
            playerOne.grounded = True
    if playerOne.grounded == False:
        playerOne.y += 10
        
                
                
                
                
    win.fill((10,10,10))
    
    for terrain in Terrains:
        terrain.draw()
    playerOne.draw()
    
    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.update()
                
pygame.quit()