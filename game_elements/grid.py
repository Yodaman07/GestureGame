import pygame


class Grid(pygame.Surface):

    def __init__(self, size: (), shrinkRatio):
        super().__init__(size)
        self.states = []
        self.grid_w = int(self.get_width() / shrinkRatio)
        self.grid_h = int(self.get_height() / shrinkRatio)

        for v in range(self.grid_h):
            self.states.append([])
            for h in range(self.grid_w):
                self.states[v].append("Black") # default grid color

        self.shrinkRatio = shrinkRatio
        self.generateGrid()

    def generateGrid(self):  # shrinkRatio is how many pixels per grid space
        # ex: if a 1000x400 pixel Surface has shrinkRatio=10, the dimensions of the grid squares will be 100x40
        # https://stackoverflow.com/questions/33963361/how-to-make-a-grid-in-pygame <-- drawing grids

        for v_layer in range(self.grid_h):  # self.states[y][x] (y increases down, x increases to the left)
            for h_layer in range(self.grid_w):
                rect = pygame.Rect(h_layer * self.shrinkRatio, v_layer * self.shrinkRatio, self.shrinkRatio,
                                   self.shrinkRatio)
                pygame.draw.rect(self, self.states[v_layer][h_layer], rect)

    def set(self, pos: (int, int), color: str): # increasing x is to the right, and increasing y is going down
        if pos[0] < 0 or pos[1] < 0:
            return

        self.states[pos[1]][pos[0]] = color
        self.generateGrid()

    def get(self, pos: (int, int)):
        if pos[0] < 0 or pos[1] < 0:
            raise IndexError
        return self.states[pos[1]][pos[0]]
