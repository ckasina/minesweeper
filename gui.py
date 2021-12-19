import pygame
import os.path as path
from logic import Grid

class GUI:
    def __init__(self):
        pygame.init()
        easy = (9, 9, 10)
        medium = (16, 16, 40)
        hard = (16, 30, 99)
        self.difficulty = easy
        self.initSizes()
        self.initFormatting()
        self.initSpeed()
        self.initGame()
        self.mainloop()


    def initSizes(self):
        self.squareSize = 50
        self.rows, self.cols, self.noOfMines = self.difficulty
        self.width = self.cols * self.squareSize
        self.height = self.rows * self.squareSize


    def initGame(self):
        self.grid = None


    def initFormatting(self):
        self.title = "Minesweeper"
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.iconNames = ["clock", "flag", "unexplored"]
        self.iconNames += [str(i) for i in range(11)]
        self.filenames = {i: path.join("images", i + ".png") for i in self.iconNames}
        self.images = {i: pygame.transform.scale(
            pygame.image.load(self.filenames[i]).convert_alpha(), 
            (self.squareSize, self.squareSize)) for i in self.iconNames}

    def initSpeed(self):
        self.clock = pygame.time.Clock()
        self.fps = 60

    def leftClick(self):
        x, y = pygame.mouse.get_pos()
        r = y // self.squareSize
        c = x // self.squareSize

        if self.grid == None:
            self.grid = Grid((r, c), self.difficulty)

        self.grid.uncover((r, c))
        if self.grid.checkLost((r, c)):
            pygame.display.set_caption("You lost!")
            self.grid.lost()
            self.draw()
            pygame.time.delay(2000)
            pygame.display.set_caption(self.title)
            self.initGame()

        elif self.grid.checkWon((r, c)):
            pygame.display.set_caption("You won!")
            self.grid.revealAll()
            self.draw()
            pygame.time.delay(2000)
            pygame.display.set_caption(self.title)
            self.initGame()


    def rightClick(self):
        x, y = pygame.mouse.get_pos()
        r = y // self.squareSize
        c = x // self.squareSize

        if self.grid == None:
            self.grid = Grid((r, c), self.difficulty)
            
        self.grid.flag((r, c))
        if self.grid.checkWon((r, c)):
            pygame.display.set_caption("You won!")
            self.grid.revealAll()
            self.draw()
            pygame.time.delay(2000)
            pygame.display.set_caption(self.title)
            self.initGame()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                self.leftClick()

            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                self.rightClick()

    def draw(self):    
        for r in range(self.rows):
            for c in range(self.cols):
                x = c * self.squareSize
                y = r * self.squareSize
                
                if self.grid == None:
                    self.window.blit(self.images["unexplored"], (x, y))
                
                elif (r, c) in self.grid.flagged:
                    self.window.blit(self.images["flag"], (x, y))
                    
                elif (r, c) in self.grid.uncovered:
                    self.window.blit(self.images[str(self.grid.getCell(r, c))], (x, y))

                else:
                    self.window.blit(self.images["unexplored"], (x, y))


        pygame.display.update()

    def mainloop(self):
        while True:
            self.clock.tick(self.fps)
            self.draw()
            self.handleEvents()

gui = GUI()
