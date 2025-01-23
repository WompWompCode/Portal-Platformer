import pygame

pygame.init()

run = True
windowWidth = 1920
windowHeight = 1080
win = pygame.display.set_mode((windowWidth,windowHeight))
font = pygame.font.SysFont("comic sans", 30)
level = 1
levelLoaded = False
interactTimer = 0
portalTimer = 0


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.grounded = False
        
    def draw(self):
        return pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))


playerOne = Player(500, 100, 50, 75)

class Terrain:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    def draw(self):
        return pygame.draw.rect(win, (0, 0, 200), (self.x, self.y, self.width, self.height))

Terrains = []

class Portal:
    def __init__(self, colour):
        self.x = 0
        self.y = 0
        self.XPlaced = self.x
        self.YPlaced = self.y
        self.width = 10
        self.height = 100
        self.colour = colour
        self.placed = False
        Portals.append(self)
        
    def draw(self):
        if self.placed:
            return pygame.draw.rect(win, self.colour, (self.XPlaced, self.YPlaced, self.width, self.height))
        else:
            return pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

Portals = []
portalOne = Portal((0, 200, 0))
portalTwo = Portal((200,200,0))

while run:
    
    interactTimer -= 1
    portalTimer -= 1
    
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
    
    if interactTimer <= 0:
        
        if keys[pygame.K_r]:
            for portal in Portals:
                if portal.placed == False:
                    portal.width, portal.height = portal.height, portal.width
                    interactTimer = 30
                
        if pygame.mouse.get_pressed()[0]:
            portalOne.placed = True
            portalOne.XPlaced = portalOne.x
            portalOne.YPlaced = portalOne.y
            interactTimer = 30
            
        if pygame.mouse.get_pressed()[2]:
            portalTwo.placed = True
            portalTwo.XPlaced = portalTwo.x
            portalTwo.YPlaced = portalTwo.y
            interactTimer = 30
        
    
    
    if levelLoaded == False:    
        match level:
            case 1:
                Terrains = []
                Terrains.append(Terrain(0, 780, 2000, 300))
                Terrains.append(Terrain(400, 500, 200, 280))
                Terrains.append(Terrain(800, 600, 1200, 180))
                levelLoaded = True
                
                
    playerOne.grounded = False

    if portalTimer <= 0:

        if playerOne.x <= portalOne.XPlaced <= playerOne.width and portalOne.YPlaced <= playerOne.y <= portalOne.YPlaced <= playerOne.y + playerOne.width:
            playerOne.x == portalTwo.XPlaced
            playerOne.y = portalTwo.YPlaced
            portalTimer = 60
            print("Portal One to Portal Two")
            
        elif playerOne.x <= portalTwo.XPlaced <= playerOne.width and portalTwo.YPlaced <= playerOne.y <= portalTwo.YPlaced <= playerOne.y + playerOne.width:
            playerOne.x == portalOne.XPlaced
            playerOne.y = portalOne.YPlaced
            portalTimer = 60
            print("Portal Two to Portal One")
            
        
        

    for terrain in Terrains:
        if terrain.x <= playerOne.x <= playerOne.x + playerOne.width <= terrain.x + terrain.width:
            pass 
        elif (terrain.x <= playerOne.x + playerOne.width <= terrain.x + terrain.width) and ((playerOne.y > terrain.y or playerOne.y + playerOne.height > terrain.y) and (playerOne.y < terrain.y + terrain.height or playerOne.y + playerOne.width < terrain.y + terrain.height)):
            playerOne.x = terrain.x - playerOne.width
        elif (terrain.x < playerOne.x <= terrain.x + terrain.width) and ((playerOne.y > terrain.y or playerOne.y + playerOne.height > terrain.y) and (playerOne.y < terrain.y + terrain.height or playerOne.y + playerOne.width < terrain.y + terrain.height)):
            playerOne.x = terrain.x + terrain.width
        if playerOne.y+playerOne.height >= terrain.y and playerOne.y < terrain.y and (playerOne.x + playerOne.width > terrain.x and playerOne.x < terrain.x + terrain.width):
            playerOne.y = terrain.y - playerOne.height
            playerOne.grounded = True
            
    
    if playerOne.grounded == False:
        playerOne.y += 10
        
                
                
                
                
    win.fill((10,10,10))
    
    mouseX, mouseY = pygame.mouse.get_pos()
    
    for portal in Portals:
        if portal.placed == False:
            portal.x = mouseX - (portal.width/2)
            portal.y = mouseY - (portal.height/2)
    
    for terrain in Terrains:
        terrain.draw()
    playerOne.draw()
    for portal in Portals:
        portal.draw()
    
    
    
    playerXDisplay = font.render(f"Player X: {playerOne.x}", 1, "white")
    playerYDisplay = font.render(f"Player Y: {playerOne.y}", 1, "white")
    win.blit(playerXDisplay, (100, 50))
    win.blit(playerYDisplay, (100, 100))
    
    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.update()
                
pygame.quit()