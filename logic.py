import random

class Grid:
    def __init__(self, first, difficulty):
        # first is where the user has first clicked since first clicked can't be a mine
        self.difficulty = difficulty
        
        self.rows, self.cols, self.noOfMines = self.difficulty

        self.grid = []
        positions = []
        self.flagged = []
        self.uncovered = []

        self.mine = 9
        self.mineHit = 10

        for r in range(self.rows):
            self.grid.append([])
            for c in range(self.cols):
                self.grid[r].append(0)

                if first != (r, c):
                    positions.append((r, c))
        
        self.minePositions = random.sample(positions, self.noOfMines)
        for (r, c) in self.minePositions:
            self.grid[r][c] = self.mine

        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) in self.minePositions:
                    continue

                mineSurround = [(r1, c1) for (r1, c1) in self.getSurround((r, c)) if (r1, c1) in self.minePositions]
                self.grid[r][c] = len(mineSurround)


    def getSurround(self, pos):
        r, c = pos
        return [(r1, c1) for r1 in range(self.rows) for c1 in range(self.cols)
        if abs(r1-r) <= 1 and abs(c1-c) <= 1 and (r1, c1) != pos]

    def uncover(self, pos):
        if pos in self.uncovered + self.flagged:
            return

        else:
            self.uncovered.append(pos)
            r, c = pos
            if self.grid[r][c] == 0:
                for r1, c1 in self.getSurround(pos):
                    self.uncover((r1, c1))


    def flag(self, pos):
        if pos in self.uncovered:
            return

        elif pos in self.flagged:
            self.flagged.remove(pos)

        else:
            self.flagged.append(pos)

    def checkLost(self, pos):
        r, c = pos
        return pos in self.uncovered and self.grid[r][c] == self.mine

    def checkWon(self, pos):
        if self.checkLost(pos):
            return False

        elif set(self.flagged) == set(self.minePositions):
            return True

        elif len(self.uncovered) == self.rows*self.cols - len(self.minePositions):
            return True

    def lost(self):
        for (r, c) in self.minePositions:
            if (r, c) not in self.flagged:
                self.grid[r][c] = self.mineHit

    def revealAll(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if not ((r, c) in self.uncovered + self.flagged + self.minePositions):
                    self.uncovered.append((r, c))

                elif ((r, c) in self.minePositions) and ((r, c) not in self.flagged):
                    self.flagged.append((r, c))

    def getCell(self, r, c):
        return self.grid[r][c]

    def __str__(self):
        x = ""
        for r in range(self.rows):
            for c in range(self.cols):
                character = ""
                if (r, c) in self.flagged:
                    character = "F"


                elif (r, c) in self.uncovered:
                    if self.grid[r][c] == 9:
                        character = "M"

                    else:
                        character = str(self.grid[r][c])
                    
                else:
                    character = "X"

                x += character + " "

            x = x[:-1]
            x += "\n"

        return x[:-1]
