import pygame


class Grid(pygame.Surface):

    def __init__(self, size: (), shrinkRatio):
        super().__init__(size)
        self.states = []

        for v in range(int(self.get_height()/shrinkRatio)):
            self.states.append([])
            for h in range(int(self.get_width()/shrinkRatio)):
                self.states[v].append("black")

        self.shrinkRatio = shrinkRatio
        self.generateGrid()

    def generateGrid(self):  # shrinkRatio is how many pixels per grid space
        # ex: if a 1000x400 pixel Surface has shrinkRatio=10, the dimensions of the grid squares will be 100x40
        # https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame <-- drawing grids

        width = self.get_width()
        height = self.get_height()

        for v_layer in range(int(height / self.shrinkRatio)):  # self.states[y][x] (y increases down, x increases to the left)
            for h_layer in range(int(width / self.shrinkRatio)):
                rect = pygame.Rect(h_layer * self.shrinkRatio, v_layer * self.shrinkRatio, self.shrinkRatio, self.shrinkRatio)
                pygame.draw.rect(self, self.states[v_layer][h_layer], rect)

    # def get(self, pos : ()):
    #     pass

    def set(self, pos: (int, int), color: str):
        self.states[pos[1]][pos[0]] = color
        self.generateGrid()
