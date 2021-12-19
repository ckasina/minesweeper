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
        self.gridWidth = self.cols * self.squareSize
        self.gridHeight = self.rows * self.squareSize
        self.width = self.gridWidth
        self.height = self.gridHeight + self.squareSize


    def initGame(self):
        self.grid = None

    def initFormatting(self):
        self.title = "Minesweeper"
        self.window = pygame.display.set_mode((self.width, self.height))
        self.gridSurf = pygame.Surface((self.gridWidth, self.gridHeight))
        self.statusSurf = pygame.Surface((self.width, self.squareSize))

        pygame.display.set_caption(self.title)
        self.iconNames = ["clock", "flag", "unexplored"]
        self.iconNames += [str(i) for i in range(11)]
        self.filenames = {i: path.join("images", i + ".png") for i in self.iconNames}
        self.images = {i: pygame.transform.scale(
            pygame.image.load(self.filenames[i]).convert_alpha(), 
            (self.squareSize, self.squareSize)) for i in self.iconNames}

        
        self.font = pygame.font.Font(pygame.font.get_default_font(), int(self.width / 20))
        self.statusBG = (255, 255, 255)
        self.statusFG = (0, 0, 0)


    def initSpeed(self):
        self.clock = pygame.time.Clock()
        self.fps = 60

    def endOfGame(self):
        self.updateDisplay()
        pygame.time.delay(2000)
        self.initGame()


    def leftClick(self):
        x, y = pygame.mouse.get_pos()
        r = y // self.squareSize
        c = x // self.squareSize

        if self.grid == None:
            self.grid = Grid((r, c), self.difficulty)

        self.grid.uncover((r, c))
        if self.grid.lost or self.grid.won:
            self.endOfGame()


    def rightClick(self):
        x, y = pygame.mouse.get_pos()
        r = y // self.squareSize
        c = x // self.squareSize

        if self.grid == None:
            self.grid = Grid((r, c), self.difficulty)
            
        self.grid.flag((r, c))
        if self.grid.won:
            self.endOfGame()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                self.leftClick()

            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                self.rightClick()

    def updateGridSurf(self):
        for r in range(self.rows):
            for c in range(self.cols):
                x = c * self.squareSize
                y = r * self.squareSize
                
                if self.grid == None:
                    self.gridSurf.blit(self.images["unexplored"], (x, y))
                
                elif (r, c) in self.grid.flagged:
                    self.gridSurf.blit(self.images["flag"], (x, y))
                    
                elif (r, c) in self.grid.uncovered:
                    self.gridSurf.blit(self.images[str(self.grid.getCell(r, c))], (x, y))

                else:
                    self.gridSurf.blit(self.images["unexplored"], (x, y))

    def updateStatusSurf(self):
        self.statusSurf.fill(self.statusBG)
        pygame.draw.rect(self.statusSurf, self.statusFG, (0, 0, self.width, self.squareSize), width=5)
        
        if self.grid != None:
            text = ""
            if not (self.grid.lost or self.grid.won):
                text = f"Mines flagged: {len(self.grid.flagged)} / {self.noOfMines}"

            elif self.grid.lost:
                text = "You lost!"

            elif self.grid.won:
                text = "You won!"


            flagText = self.font.render(text, True, self.statusFG)
            flagTextRect = flagText.get_rect()

            flagX = (self.width // 2) - flagTextRect.centerx
            flagY = (self.squareSize // 2) - flagTextRect.centery
            
            self.statusSurf.blit(flagText, (flagX, flagY))

    def updateDisplay(self):    
        self.updateGridSurf()
        self.updateStatusSurf()
        self.window.blit(self.gridSurf, (0, 0))
        self.window.blit(self.statusSurf, (0, self.gridHeight))
        pygame.display.update()

    def mainloop(self):
        while True:
            self.clock.tick(self.fps)
            self.updateDisplay()
            self.handleEvents()

gui = GUI()
