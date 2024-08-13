import pygame


class Player:
    def __init__(self, screen, size=20):
        self.screen = screen
        self.size = size  # radius of player circle
        self.x, self.y = (self.size, self.size)

    def draw(self):  # to be placed in game loop
        # print(self.x, self.y)
        pygame.draw.circle(self.screen, "green", (self.x, self.y), self.size)

    def parse_input_and_draw(self, gestureList):  # moves the player appropriately + draws and updates movement
        move_direction = 5
        if not gestureList: return
        if gestureList[-1]['Name'] == None:
            pass
        elif gestureList[-1]["Name"] == "Open_Palm":
            self.x += move_direction  # move right
        elif gestureList[-1]["Name"] == "Closed_Fist":
            self.x += -move_direction  # move left
        elif gestureList[-1]["Name"] == "Victory":
            self.y += -move_direction  # move up (y increasing is going down)
        elif gestureList[-1]["Name"] == "Thumb_Down":
            self.y += move_direction  # move down
        elif gestureList[-1]["Name"] == "Pointing_Up":
            self.x, self.y = (self.size, self.size)
        self.draw()
