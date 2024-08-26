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
        self.startPos = ()
        self.endPos = [0, 0]  # coordinate pair
        self.width = self.grid.grid_w
        self.height = self.grid.grid_h
        self.startMode = ""  # horizontal or vertical
        print(f"Grid Width: {self.width}, Grid Height: {self.height}")

    def findStart(self, plot=False):  # finds the start pos and adds it to the list
        xCoord, yCoord = 0, 0
        if random.randint(0, 1) == 1:  # 1 = Find starting point on the left or right
            # 0 = Find starting point on the top or bottom
            possibleX = [0, self.width - 1]
            xCoord = possibleX[random.randint(0, 1)]
            yCoord = random.randint(0, self.height - 1)
            self.endPos[0] = 0 if xCoord == (self.width - 1) else (self.width - 1)
            self.startMode = "horizontal"
        else:
            possibleY = [0, self.height - 1]
            xCoord = random.randint(0, self.width - 1)
            yCoord = possibleY[random.randint(0, 1)]
            self.endPos[1] = 0 if yCoord == (self.height - 1) else (self.height - 1)
            self.startMode = "vertical"
        coords = (xCoord, yCoord)
        # coords = (10, 2)
        print(f"Starting point: {coords}")

        self.coordinates.append(coords)
        self.startPos = coords
        if plot: self.grid.set(coords, "white")
        return coords

    # Order:
    # 1. find available locations (is the square in front available, if so check if the one in front of that is, then take it)
    # 2. Randomly choose available location to move to, and move
    # 3. Continue, if there are no available locations, backtrack, slowly move down the list, constantly checking for available locations

    def evaluatePossibleCoord(self, coord, visualize,
                              originalVector) -> bool:  # evaluate the joined edges of each of the possible coordinates
        #     o
        #   o x o
        # x is the possible coordinate, and o is all the places that will be checked
        vector_1 = (originalVector[1], originalVector[0])  # ex, this would be the right o
        vector_2 = (-originalVector[1], -originalVector[0])  # ex, this would be the left o
        vector_3 = (originalVector[0], originalVector[1])  # ex, this would be the top o
        vectorsToCheck = [vector_1, vector_2, vector_3]

        canMove = True

        for vector in vectorsToCheck:
            posToCheck = (coord[0] + vector[0], coord[1] + vector[1])
            try:
                if self.grid.get(posToCheck) != "white":
                    if visualize:
                        self.grid.set(posToCheck, "purple")
                else:
                    canMove = False
            except IndexError:
                continue

        return canMove

    def findAvailableLocations(self, pos, visualize):
        directionVectors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        availablePositions = []

        for direction in directionVectors:
            newPos = (pos[0] + direction[0], pos[1] + direction[1])

            try:
                color = self.grid.get(newPos)
                if color == "black":  # pixel isn't taken
                    if visualize:
                        self.grid.set(newPos, "green")
                    availablePos = self.evaluatePossibleCoord(newPos, visualize, direction)
                    if availablePos: availablePositions.append(newPos)

            except IndexError:
                continue
                # print("NONE")

        print(f"At: {pos}, Possible next moves (green): {availablePositions}")
        return availablePositions

    def generate(self) -> bool:  # should be called repeatedly in a loop, returns if the generation was a success
        self.grid.resetColorMarkers()
        self.grid.set(self.coordinates[-1], "white")

        positions = self.findAvailableLocations(self.coordinates[-1], visualize=True)
        if positions == []:  # backtracking time!!!!!!
            if len(self.coordinates) == 1:
                print(self.coordinates)
                self.findEndPoints()
            self.coordinates.pop()
            if self.coordinates == []: return False
            result = self.generate()
            return result
        num = random.randint(0, len(positions) - 1)  # random number <-- PLACE BREAKPOINT HERE

        newPos = positions[num]
        self.coordinates.append(newPos)

        print(f"{newPos} Selected")
        return True

    def addStartAndEnd(self):
        # self.grid.set(self.startPos, "yellow")
        self.grid.set((self.endPos[0], self.endPos[1]), "yellow")

    def findEndPoints(self):
        if self.startMode == "horizontal":
            possibleY = []
            for i in range(self.height):
                color = self.grid.get((self.endPos[0], i))
                if color == "white": possibleY.append(i)
            index = random.randint(0, len(possibleY)) - 1
            self.endPos[1] = possibleY[index]
        else:
            possibleX = []
            for i in range(self.width):
                color = self.grid.get((i, self.endPos[1]))
                if color == "white": possibleX.append(i)
            index = random.randint(0, len(possibleX)) - 1
            self.endPos[0] = possibleX[index]