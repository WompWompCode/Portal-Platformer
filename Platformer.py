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
        self.velocity = [0,0]
        
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
        self.height = 120
        self.widthPlaced = self.width
        self.heightPlaced = self.height
        self.colour = colour
        self.placed = False
        self.direction = "east"
        self.directionPlaced = self.direction
        Portals.append(self)
        
    def draw(self):
        if self.placed:
            return pygame.draw.rect(win, self.colour, (self.XPlaced, self.YPlaced, self.widthPlaced, self.heightPlaced))
        else:
            return pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

Portals = []
portalOne = Portal((0, 200, 0))
portalTwo = Portal((200,200,0))

def teleport(startPortalDirection, endPortal, endPortalDirection):
    if (startPortalDirection == "north" or startPortalDirection == "south") and (endPortalDirection == "east"):
        if playerOne.velocity[1] < 0:
            playerOne.velocity[1] *= -1
    if (startPortalDirection == "west" and endPortalDirection == "east") or (startPortalDirection == "east" and endPortalDirection == "west"):
        playerOne.velocity[0] *= -1
            
        
    if ((endPortalDirection == "north" or endPortalDirection == "south" ) and (startPortalDirection == "west" or startPortalDirection == "east")) or (endPortalDirection == "east" or endPortalDirection == "west" ) and (startPortalDirection == "north" or startPortalDirection == "south"):
        playerOne.velocity[0], playerOne.velocity[1] = playerOne.velocity[1], playerOne.velocity[0]
    if endPortalDirection == "north":
        playerOne.x = endPortal.XPlaced
        playerOne.y = endPortal.YPlaced - playerOne.height
    elif endPortalDirection == "east":
        playerOne.x = endPortal.XPlaced + endPortal.widthPlaced
        playerOne.y = endPortal.y
    elif endPortalDirection == "south":
        playerOne.x = endPortal.XPlaced
        playerOne.y = endPortal.YPlaced + endPortal.heightPlaced
    elif endPortalDirection == "west":
        playerOne.x = endPortal.XPlaced - playerOne.width
        playerOne.y = endPortal.YPlaced
        
    return playerOne.x, playerOne.y, playerOne.velocity

while run:
    
    interactTimer -= 1
    portalTimer -= 1
    if playerOne.velocity[0] > 0:
        playerOne.velocity[0] -= 0.5
    elif playerOne.velocity[0] < 0:
        playerOne.velocity[0] += 0.5
    if playerOne.grounded:
        playerOne.velocity[1] = 0
    else:
        playerOne.velocity[1] -= 1
        if portalTimer > 5:
            portalTimer = 5
        
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
                
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if playerOne.velocity[0] > -10:
            playerOne.velocity[0] -= 1 
        
    if keys[pygame.K_d]:
        if playerOne.velocity[0] < 10:
            playerOne.velocity[0] += 1 
        
    if playerOne.grounded == True:
        if keys[pygame.K_SPACE]:
            playerOne.velocity[1] = 22
            
    playerOne.x += playerOne.velocity[0]
    playerOne.y -= playerOne.velocity[1]
    
    if interactTimer <= 0:
        
        if keys[pygame.K_r]:
            for portal in Portals:
                portal.width, portal.height = portal.height, portal.width
                match portal.direction:
                    case "north":
                        portal.direction = "east"
                    case "east":
                        portal.direction = "south"
                    case "south":
                        portal.direction = "west"
                    case "west": 
                        portal.direction = "north"
                interactTimer = 30
                
        if pygame.mouse.get_pressed()[0]:
            portalOne.placed = True
            portalOne.XPlaced = portalOne.x
            portalOne.YPlaced = portalOne.y
            portalOne.widthPlaced = portalOne.width
            portalOne.heightPlaced = portalOne.height
            portalOne.directionPlaced = portalOne.direction
            interactTimer = 30
            
        if pygame.mouse.get_pressed()[2]:
            portalTwo.placed = True
            portalTwo.XPlaced = portalTwo.x
            portalTwo.YPlaced = portalTwo.y
            portalTwo.widthPlaced = portalTwo.width
            portalTwo.heightPlaced = portalTwo.height
            portalTwo.directionPlaced = portalTwo.direction
            interactTimer = 30
        
    
    
    if levelLoaded == False:    
        match level:
            case 1:
                Terrains = []
                Terrains.append(Terrain(-1000, 780, 30000, 300))
                Terrains.append(Terrain(400, 500, 200, 280))
                Terrains.append(Terrain(800, 600, 1000, 180))
                levelLoaded = True
                
                
    playerOne.grounded = False

    if portalTimer <= 0:

        #to the right
        if (portalOne.heightPlaced > portalOne.widthPlaced) and (playerOne.x <= portalOne.XPlaced + portalOne.widthPlaced <= playerOne.x + playerOne.width) and (portalOne.YPlaced <= playerOne.y  <= playerOne.y + playerOne.height <= portalOne.YPlaced + portalOne.heightPlaced):
            playerOne.x, playerOne.y, playerOne.velocity = teleport(portalOne.directionPlaced, portalTwo, portalTwo.directionPlaced)
            portalTimer = 15
            print("Portal One to Portal Two")
        
        #to the left  
        elif (portalOne.heightPlaced > portalOne.widthPlaced) and (playerOne.x <= portalOne.XPlaced <= playerOne.x + playerOne.width) and (portalOne.YPlaced <= playerOne.y  <= playerOne.y + playerOne.height <= portalOne.YPlaced + portalOne.heightPlaced):
            playerOne.x, playerOne.y, playerOne.velocity = teleport(portalOne.directionPlaced, portalTwo, portalTwo.directionPlaced)
            portalTimer = 15
            print("Portal One to Portal Two")
            
        #from above
        elif (portalOne.widthPlaced > portalOne.heightPlaced) and (playerOne.y <= portalOne.YPlaced <= playerOne.y + playerOne.height) and (portalOne.XPlaced <= playerOne.x <= playerOne.x + playerOne.width <= portalOne.XPlaced + portalOne.widthPlaced):
            playerOne.x, playerOne.y, playerOne.velocity = teleport(portalOne.directionPlaced, portalTwo, portalTwo.directionPlaced)
            portalTimer = 15
            print("Portal One to Portal Two")
        
        
        
        #right
        elif (portalTwo.heightPlaced > portalTwo.widthPlaced) and (playerOne.x <= portalTwo.XPlaced + portalTwo.widthPlaced <= playerOne.x + playerOne.width) and (portalTwo.YPlaced <= playerOne.y  <= playerOne.y + playerOne.height <= portalTwo.YPlaced + portalTwo.heightPlaced):
            playerOne.x, playerOne.y, playerOne.velocity = teleport(portalTwo.directionPlaced, portalOne, portalOne.directionPlaced)
            portalTimer = 15
            print("Portal Two to Portal One")
            
        #left 
        elif (portalTwo.heightPlaced > portalTwo.widthPlaced) and (playerOne.x <= portalTwo.XPlaced <= playerOne.x + playerOne.width) and (portalTwo.YPlaced <= playerOne.y  <= playerOne.y + playerOne.height <= portalTwo.YPlaced + portalTwo.heightPlaced):
            playerOne.x, playerOne.y, playerOne.velocity = teleport(portalTwo.directionPlaced, portalOne, portalOne.directionPlaced)
            portalTimer = 15
            print("Portal Two to Portal One")
            
        #from above
        elif (portalTwo.widthPlaced > portalTwo.heightPlaced) and (playerOne.y <= portalTwo.YPlaced <= playerOne.y + playerOne.height) and (portalTwo.XPlaced <= playerOne.x <= playerOne.x + playerOne.width <= portalTwo.XPlaced + portalTwo.widthPlaced):
            playerOne.x, playerOne.y, playerOne.velocity = teleport(portalTwo.directionPlaced, portalOne, portalOne.directionPlaced)
            portalTimer = 15
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
        
        if terrain.y + terrain.height > playerOne.y + playerOne.height > terrain.y and (terrain.x <=playerOne.x <= playerOne.x + playerOne.width <=  terrain.x +terrain.width):
            playerOne.y = terrain.y - playerOne.height
            
    
        
    windowScrollMovement = windowWidth - playerOne.x 
    if windowScrollMovement < 200:
        windowScrollMovement = 200 - windowScrollMovement
        for terrain in Terrains:
            terrain.x -= windowScrollMovement
        playerOne.x -= windowScrollMovement
    elif windowScrollMovement > 1720:
        windowScrollMovement = 200 - (windowWidth - windowScrollMovement)
        for terrain in Terrains:
            terrain.x += windowScrollMovement
        playerOne.x += windowScrollMovement
        
                
                
                
                
    win.fill((10,10,10))
    
    mouseX, mouseY = pygame.mouse.get_pos()
    
    for portal in Portals:
        portal.x = mouseX - (portal.width/2)
        portal.y = mouseY - (portal.height/2)
    
    for terrain in Terrains:
        terrain.draw()
    playerOne.draw()
    for portal in Portals:
        portal.draw()
    
    
    
    playerXDisplay = font.render(f"Player X: {playerOne.x}", 1, "white")
    playerYDisplay = font.render(f"Player Y: {playerOne.y}", 1, "white")
    playerVelDisplay = font.render(f"Player Veloctity: {playerOne.velocity[0]}, {playerOne.velocity[1]}", 1, "white")
    portalOneXYDisplay = font.render(f"Portal One: {portalOne.XPlaced}, {portalOne.YPlaced}, ({portalOne.x}, {portalOne.y}), {portalOne.directionPlaced}, ({portalOne.direction}), {portalOne.widthPlaced}, {portalOne.heightPlaced}, ({portalOne.width}, {portalOne.height})", 1, "white")
    portalTwoXYDisplay = font.render(f"Portal Two: {portalTwo.XPlaced}, {portalTwo.YPlaced},({portalTwo.x}, {portalTwo.y}), {portalTwo.directionPlaced}, ({portalTwo.direction}), {portalTwo.widthPlaced}, {portalTwo.heightPlaced}, ({portalTwo.width}, {portalTwo.height})", 1, "white")
    win.blit(playerXDisplay, (100, 50))
    win.blit(playerYDisplay, (100, 100))
    win.blit(playerVelDisplay, (100, 150))
    win.blit(portalOneXYDisplay, (100, 200))
    win.blit(portalTwoXYDisplay, (100, 250))
    
    clock = pygame.time.Clock()
    clock.tick(60)
    pygame.display.update()
                
pygame.quit()