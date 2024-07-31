import pygame


class Screen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        self.clock = pygame.time.Clock()
        self.running = False

    def runLoop(self):
        self.running = True
        while self.running:
            self.screen.fill("white")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()