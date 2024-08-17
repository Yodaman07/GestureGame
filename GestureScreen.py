from GestureDetection import GestureDetector
from game_elements import *

import pygame
import pygame_widgets
from pygame_widgets.button import Button


class GestureScreen:  # sets up a pygame screen connected to a live stream, detecting your current hand gesture
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("GestureGame")

        self.clock = pygame.time.Clock()
        self.running = True
        self.gd = GestureDetector(10)

        self.player: Player = None
        self.mg: MazeGen = None
        self.canGenerate: bool = False
        self.generating: bool = False

        self.streamArea: pygame.Surface = None
        self.gestureIconLayout: pygame.Surface = None
        self.buttonSurface: pygame.Surface = None
        self.grid: Grid = None

        self.btn = Button = None
        self.font = pygame.font.SysFont("Serif", 32)
        self.text = None
        self.canUpdateTitle = False  # Changes title from default val to boolean controlled val

        self.readyToPlay: bool = False

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

        self.genBtn = Button(self.screen, self.gd.width * 1.75, self.heightOffset / 2, 250, 50, radius=20,
                             text="Generate Maze", fontSize=20,
                             inactiveColour=(200, 50, 0), onClick=lambda: self.canGen())

        self.text = self.font.render(f"Status: Not Generated", True, "red")  # default

        self.grid = Grid((self.screen.get_width(), self.screen.get_height() - self.heightOffset), 25)

        # DON'T CHANGE the shrink factor in GestureDetection.py

        self.mg = MazeGen(self.grid)

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

    def canGen(self):
        self.canUpdateTitle = True
        if self.generating == False:
            self.grid.resetAll()
            start = self.mg.findStart(False)

            sr = self.grid.shrinkRatio
            playerStart = ((start[0] * sr) + (sr / 2), (start[1] * sr) + (sr / 2))
            self.player = Player(self.grid, playerStart, size=9)

            self.canGenerate = True
            self.generating = True

    def addGameContent(self):
        if self.canGenerate:
            self.canGenerate = self.mg.generate()  # coordinates are stored in self.mg
        else:
            self.grid.resetColorMarkers()
            if self.mg.coordinates == []:
                if self.canUpdateTitle: self.mg.addStartAndEnd()
                self.generating = False

        if not self.generating and self.canUpdateTitle:
            self.grid.generateGrid(self.player, self.gd.gestures)
            self.player.parse_input_and_draw(self.gd.gestures)

        self.screen.blit(self.text, (self.gd.width * 1.75, (self.heightOffset / 2) + 75))
        self.screen.blit(self.grid, (0, self.heightOffset))

    def display(self):
        if self.canUpdateTitle:
            self.text = self.font.render(f"Status: {'Generated' if not self.generating else 'Generating'}", True,
                                         "green" if not self.generating else "red")

        self.addStream()

        # Rect Order  -> (top_left_x, top_left_y, ending_x, ending_y)
        pygame.draw.rect(self.screen, "red",
                         pygame.Rect(0, self.heightOffset - 10, self.screen.get_width(), 10))  # dividing line
        self.addGameContent()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                break

        pygame_widgets.update(events)

        pygame.display.flip()
        self.clock.tick(60)
