import pygame


# from game_elements.grid import Grid


class Player:
    def __init__(self, screen, startPos: (), size=20):  # Start pos in grid spaces
        self.screen = screen
        self.size = size  # radius of player circle
        self.x, self.y = (startPos[0], startPos[1])
        self.collider = self.getCollider()
        self.move_direction = 1
        self.gestureList = None

    def draw(self):  # to be placed in game loop
        pygame.draw.circle(self.screen, "green", (self.x, self.y), self.size)
        pygame.draw.rect(self.screen, 'pink', self.getCollider())

    def getCollider(self):
        sr = self.screen.shrinkRatio
        self.collider = pygame.Rect(self.x - sr / 2, self.y - sr / 2, sr, sr).inflate(-5, -5)
        return self.collider

    def parse_input_and_draw(self, gestureList):  # moves the player appropriately + draws and updates movement
        if not gestureList: return
        self.gestureList = gestureList
        if self.gestureList[-1]['Name'] == None:
            pass
        elif self.gestureList[-1]["Name"] == "Open_Palm":
            self.x += self.move_direction  # move right
        elif self.gestureList[-1]["Name"] == "Closed_Fist":
            self.x += -self.move_direction  # move left
        elif self.gestureList[-1]["Name"] == "Victory":
            self.y += -self.move_direction  # move up (y increasing is going down)
        elif self.gestureList[-1]["Name"] == "Thumb_Down":
            self.y += self.move_direction  # move down
        elif self.gestureList[-1]["Name"] == "Pointing_Up":
            self.x, self.y = (self.size, self.size)
        self.draw()

    def collided(self):
        if self.gestureList[-1]["Name"] == "Open_Palm":
            self.x -= self.move_direction
        elif self.gestureList[-1]["Name"] == "Closed_Fist":
            self.x -= -self.move_direction
        elif self.gestureList[-1]["Name"] == "Victory":
            self.y -= -self.move_direction
        elif self.gestureList[-1]["Name"] == "Thumb_Down":
            self.y -= self.move_direction
