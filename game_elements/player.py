import pygame


# from game_elements.grid import Grid


class Player:
    def __init__(self, screen, startPos: (), size=20):  # Start pos in grid spaces
        self.screen = screen
        self.size = size  # radius of player circle
        self.x, self.y = (startPos[0], startPos[1])
        self.collider = self.getCollider()
        self.move_direction = 1

    def draw(self):  # to be placed in game loop
        pygame.draw.circle(self.screen, "green", (self.x, self.y), self.size)
        pygame.draw.rect(self.screen, 'pink', self.getCollider())

    def getCollider(self):
        sr = self.screen.shrinkRatio
        self.collider = pygame.Rect(self.x - sr / 2, self.y - sr / 2, sr, sr).inflate(-5, -5)
        return self.collider

    def parse_input_and_draw(self, gestureList):  # moves the player appropriately + draws and updates movement
        if not gestureList: return
        if gestureList[-1]['Name'] == None:
            pass
        elif gestureList[-1]["Name"] == "Open_Palm":
            self.x += self.move_direction  # move right
        elif gestureList[-1]["Name"] == "Closed_Fist":
            self.x += -self.move_direction  # move left
        elif gestureList[-1]["Name"] == "Victory":
            self.y += -self.move_direction  # move up (y increasing is going down)
        elif gestureList[-1]["Name"] == "Thumb_Down":
            self.y += self.move_direction  # move down
        elif gestureList[-1]["Name"] == "Pointing_Up":
            self.x, self.y = (self.size, self.size)
        self.draw()

    def collided(self, rect):
        # TODO: Fix offscreen coliding
        # [down, top, right, and left]
        diffList = [self.collider.midbottom[1] - rect.midtop[1], # TODO Fix this so we get the right vals originally
                    rect.midbottom[1] - self.collider.midtop[1],
                    rect.midleft[0] - self.collider.midright[0],
                    rect.midright[0] - self.collider.midleft[0]]
        absDiff = []
        for difference in diffList:
            absDiff.append(abs(difference))

        index = absDiff.index(min(absDiff))  # index of the current colliding direction
        # print(index)
        if index == 0:
            self.y -= self.move_direction # move up
        elif index == 1:
            self.y += self.move_direction # move down
        elif index == 2:
            self.x -= self.move_direction # move left
        elif index == 3:
            self.x += self.move_direction # move right

        # print(rect.midtop, self.collider.midbottom, "Down")  # going down
        # print(rect.midbottom, self.collider.midtop, "Up")  # going up
        # print(rect.midleft, self.collider.midright, "Right")  # going right
        # print(rect.midright, self.collider.midleft, "Left")  # going left
