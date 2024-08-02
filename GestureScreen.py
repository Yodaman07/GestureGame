from GestureDetection import GestureDetector
import cv2 as cv
import pygame


class GestureScreen:  # sets up a pygame screen connected to a live stream, detecting your current hand gesture
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.clock = pygame.time.Clock()
        self.running = False

    def runLoop(self):
        gd = GestureDetector(10)
        gd.initStream()
        self.running = True

        gap = 10
        width = (((gd.height / 4) + gap) * len(gd.possibleGestures)) - gap  # 7 gap sizes and 8 icon sizes

        streamArea = pygame.Surface((gd.width, gd.height))
        gestureIconLayout = pygame.Surface((width, gd.height / 4))
        gestureIconLayout.fill("green")

        iconOffset = gap + (gd.height / 4)


        while self.running:
            addedOffset = 0
            for gesture in gd.possibleGestures:
                color = "purple"
                if gd.gestures != []:
                    if gd.gestures[-1]["Name"] == gesture:
                        color = "red" # red means detected

                pygame.draw.rect(gestureIconLayout, color, pygame.Rect(addedOffset, 0, gd.height / 4, gd.height / 4))

                addedOffset += iconOffset


            currentFrame = gd.getCurrentFrame()

            # code from https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
            img = pygame.image.frombuffer(currentFrame.tostring(), currentFrame.shape[1::-1],
                                          "BGR")

            self.screen.fill("white")
            self.screen.blit(gestureIconLayout, (0, gd.height + 10))
            self.screen.blit(streamArea, (0, 0))

            streamArea.blit(img, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            pygame.display.flip()
            self.clock.tick(60)

        gd.cam.release()
        pygame.quit()
