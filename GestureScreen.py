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

        streamArea = pygame.Surface((gd.width, gd.height))
        streamArea.fill("green")  # will only paint once

        while self.running:
            currentFrame = gd.getCurrentFrame()

            # code from https://stackoverflow.com/questions/19306211/opencv-cv2-image-to-pygame-image
            img = pygame.image.frombuffer(currentFrame.tostring(), currentFrame.shape[1::-1],
                                          "BGR")

            self.screen.fill("white")
            self.screen.blit(streamArea, (0, 0))

            streamArea.blit(img, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            pygame.display.flip()
            self.clock.tick(60)

        gd.cam.release()
        pygame.quit()
