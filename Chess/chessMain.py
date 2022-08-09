## Responsible for handling user input
## Fixed pygame import in macOS

import pygame as p
import chessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8 # 8x8 board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # used for animation of peices
IMAGES = {}

# Initialize a global dictionary of images
# Called once since it is a heavy operation
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # saved the image for a piece in the dictionary with the name as the key

# user imput and update graphics

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    loadImages()
    running = True
    squareSelected = () # tuple to keep track of the last clip of the user
    playerClicks = [] # keeps track of player clicks
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # gets the x,y position of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if squareSelected == (row, col): # user clicked the same square twice
                    squareSelected = () # user unselected a piece
                    playerClicks = [] # clear player clicks
                else:
                    squareSelected = (row, col)
                    playerClicks.append(squareSelected)
                if len(playerClicks) == 2: # after second click
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True
                            squareSelected = () # resets user click
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [squareSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_u:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

# need to draw tiles first or else pieces will not be visible
def drawGameState(screen, gs):
    drawBoard(screen) # draws the tiles on the board
    drawPieces(screen, gs.board) # draws pieces on top of the tiles

def drawBoard(screen):
    colours = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[((r+c) % 2)]
            p.draw.rect(screen, colour, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))



def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
    
