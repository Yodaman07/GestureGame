from game_elements.grid import Grid
import random


# https://en.wikipedia.org/wiki/Maze_generation_algorithm
# https://github.com/john-science/mazelib/blob/main/docs/MAZE_GEN_ALGOS.md
# https://stackoverflow.com/questions/38502/whats-a-good-algorithm-to-generate-a-maze
# Good resources for maze generation algorithms
# This is going to implement a depth-first maze generation algorithm configured to work with pygame


class MazeGen:
    def __init__(self, grid: Grid):
        # width and height in grid spaces
        self.grid = grid
        self.coordinates = []
        self.width = self.grid.grid_w
        self.height = self.grid.grid_h
        print(f"Grid Width: {self.width}, Grid Height: {self.height}")

    def plotStart(self):
        xCoord, yCoord = 0, 0
        if random.randint(0, 1) == 1:  # 1 = Find starting point on the left or right
            # 0 = Find starting point on the top or bottom
            possibleX = [0, self.width - 1]
            xCoord = possibleX[random.randint(0, 1)]
            yCoord = random.randint(0, self.height)
        else:
            possibleY = [0, self.height - 1]
            xCoord = random.randint(0, self.width)
            yCoord = possibleY[random.randint(0, 1)]
        coords = (xCoord, yCoord)
        print(f"Starting point: {coords}")

        self.coordinates.append(coords)
        self.grid.set(coords, "White")
        return coords

    # Order:
    # 1. find available locations (is the square in front available, if so check if the one in front of that is, then take it)
    # 2. Randomly choose available location to move to, and move
    # 3. Continue, if there are no available locations, backtrack, slowly move down the list, constantly checking for available locations

    def findAvailableLocations(self, pos):
        directionVectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        availablePositions = []
        ahead = 1  # to check 1 ahead, to check 2 ahead, etc

        while ahead < 3:

            for direction in directionVectors:
                newPos = (pos[0] + direction[0] * ahead, pos[1] + direction[1] * ahead)
                try:
                    color = self.grid.get(newPos)
                    if color == "Black":
                        if ahead == 1:
                            self.grid.set(newPos, "Green")
                            availablePositions.append(newPos)
                        else:
                            self.grid.set(newPos, "Purple")
                except IndexError:
                    continue
                    # print("NONE")

            ahead += 1
        print(f"Possible next moves (green): {availablePositions}")
