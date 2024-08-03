from GestureDetection import GestureDetector
import pygame


class GestureScreen:  # sets up a pygame screen connected to a live stream, detecting your current hand gesture
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((1000, 700))

        self.clock = pygame.time.Clock()
        self.running = True
        self.gd = GestureDetector(10)

        self.streamArea: pygame.Surface = None
        self.gestureIconLayout: pygame.Surface = None
        self.iconOffset: int = None

    def initUI(self, gap):  # Initializes the UI and all necessary components
        self.gd.initStream()  # must run in order to get the camera properties from the stream

        gestureLayoutWidth = (((self.gd.height / 4) + gap) * len(self.gd.possibleGestures)) - gap  # 7 gap sizes and 8 icon sizes

        self.streamArea = pygame.Surface((self.gd.width, self.gd.height))
        self.gestureIconLayout = pygame.Surface((gestureLayoutWidth, self.gd.height / 4))
        self.gestureIconLayout.fill("green")
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

    def display(self):
        self.addStream()
        heightOffset = self.gd.height+self.gestureIconLayout.get_height()+10 + 20
        # Rect Order  -> (top_left_x, top_left_y, ending_x, ending_y)
        pygame.draw.rect(self.screen, "black", pygame.Rect(0, heightOffset, self.screen.get_width(), 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break

        pygame.display.flip()
        self.clock.tick(60)
