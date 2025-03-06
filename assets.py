def menuAssets():
    pass

def platformerAssets(win):
    Player = playerAssets(win)
    Terrain = terrainAssets(win)
    Portal = portalAssets(win)
    
    return Player, Terrain, Portal

def playerAssets(win): 
    import pygame 
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
    
    return Player


def terrainAssets(win):
    import pygame
    class Terrain:
        
        def __init__(self,x,y,width,height):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            
        def draw(self):
            return pygame.draw.rect(win, (0, 0, 200), (self.x, self.y, self.width, self.height))

    return Terrain
    

def portalAssets(win):
    import pygame

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
            
        def draw(self):
            if self.placed:
                return pygame.draw.rect(win, self.colour, (self.XPlaced, self.YPlaced, self.widthPlaced, self.heightPlaced))
            else:
                return pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))

    
    return Portal

