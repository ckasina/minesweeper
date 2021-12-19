from logic import Grid
easy = (9, 9, 10)
medium = (16, 16, 40)
hard = (16, 30, 99)
difficulty = easy
grid = None
while True:
    rc = input("Enter row, col: ")
    action = input("(F)lag or (U)ncover: ")
    r, c = int(rc[0]), int(rc[1])
    if grid == None:
        grid = Grid((r, c), difficulty)
        grid.uncover((r, c))

    elif action == "U":
        grid.uncover((r, c))

    elif action == "F":
        grid.flag((r, c))


    print(grid)
    if grid.checkLost((r, c)):
        print("LOST!")
        break

    elif grid.checkWon((r, c)):
        print("WON!")
        break

    