from GestureDetection import GestureDetector
from game_elements import *

import pygame


class GestureScreen:  # sets up a pygame screen connected to a live stream, detecting your current hand gesture
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 700))

        self.clock = pygame.time.Clock()
        self.running = True
        self.gd = GestureDetector(10)

        self.player: Player = None
        self.mg: MazeGen = None
        self.canGenerate: bool = True

        self.streamArea: pygame.Surface = None
        self.gestureIconLayout: pygame.Surface = None
        self.grid: Grid = None

        self.iconOffset: int = None  # icon spacing
        self.heightOffset: int = None  # divider from the stream and the game

    def initUI(self, gap):  # Initializes the UI and all necessary components
        self.gd.initStream()  # must run in order to get the camera properties from the stream

        gestureLayoutWidth = (((self.gd.height / 4) + gap) * len(
            self.gd.possibleGestures)) - gap  # 7 gap sizes and 8 icon sizes

        self.streamArea = pygame.Surface((self.gd.width, self.gd.height))
        self.gestureIconLayout = pygame.Surface((gestureLayoutWidth, self.gd.height / 4))
        self.gestureIconLayout.fill("green")

        self.heightOffset = self.gd.height + self.gestureIconLayout.get_height() + 10 + 20

        # DON'T CHANGE the shrink factor in GestureDetection.py
        # 1000 pixels by 400 pixels (assuming shrink factor = 5)

        self.grid = Grid((self.screen.get_width(), self.screen.get_height() - self.heightOffset), 25)
        # self.grid.set((12, 2), "white")

        self.mg = MazeGen(self.grid)
        self.mg.findStart(False)
        # self.grid.set((18, 15), "white")
        # self.mg.findAvailableLocations((18, 15), True)

        self.player = Player(self.grid)

        self.iconOffset = gap + (self.gd.height / 4)

    def addStream(self):
        addedOffset = 0
        for gesture in self.gd.possibleGestures:
            color = "purple"
            if self.gd.gestures != []:
                if self.gd.gestures[-1]["Name"] == gesture:
                    color = "red"  # red means detected

            pygame.draw.rect(self.gestureIconLayout, color,
                             pygame.Rect(addedOffset, 0, self.gd.height / 4, self.gd.height / 4))
            addedOffset += self.iconOffset

        currentFrame = self.gd.getCurrentFrame()
        # code from https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
        img = pygame.image.frombuffer(currentFrame.tostring(), currentFrame.shape[1::-1],
                                      "BGR")

        self.screen.fill("white")
        self.screen.blit(self.gestureIconLayout, (0, self.gd.height + 10))
        self.screen.blit(self.streamArea, (0, 0))
        self.streamArea.blit(img, (0, 0))

    def addGameContent(self):
        self.grid.resetColorMarkers()
        if self.canGenerate:
            self.canGenerate = self.mg.generate()  # coordinates are stored in self.mg

        # self.player.parse_input_and_draw(self.gd.gestures)
        self.screen.blit(self.grid, (0, self.heightOffset))

    def display(self):
        # self.addStream()

        # Rect Order  -> (top_left_x, top_left_y, ending_x, ending_y)
        pygame.draw.rect(self.screen, "black",
                         pygame.Rect(0, self.heightOffset, self.screen.get_width(), 10))  # dividing line
        self.addGameContent()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        pygame.display.flip()
        self.clock.tick(60)
