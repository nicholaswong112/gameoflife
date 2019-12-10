import pygame
from board import Board

### CONSTANTS ###
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (200, 200, 200)

GRID_SIZE = 20
WIDTH, HEIGHT = 700, 800  # TODO make this dynamic

### SET UP ###
# stuff for pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game of Life')
# TODO add an icon?
clock = pygame.time.Clock()

# helper to create text


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

# helper to make a button (rect with text and optional action)


def button(msg, dimensions, color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(window, color, dimensions)
    x, y, w, h = dimensions
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        # if left click on the button, do the action (if any)
        if click[0] == 1 and action != None:
            action()
    font = pygame.font.SysFont("Arial", 18)
    text, pos = text_objects(msg, font)
    pos.center = ((x + (w / 2)), (y + (h / 2)))
    window.blit(text, pos)


# creating the cell grid
board = Board(GRID_SIZE)
# loop variables
loop = True
running = False  # whether the simulation is running
# helper function for step() -- counts number of neighbors alive + accounts for bounds


def draw_cells():
    unitLen = WIDTH / GRID_SIZE
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            dimensions = (c * unitLen + 1, r * unitLen +
                          1, unitLen - 2, unitLen - 2)
            pygame.draw.rect(
                window, BLACK if board.get(r, c) else WHITE, dimensions)

# clears the cells matrix, sets `running` to False - called by Reset button


def reset():
    global running
    board.reset()
    running = False

# toggles `running` state - called by Start/stop button


def toggle():
    global running
    running = not running


# game loop
while loop:
    # clears screen
    window.fill(LIGHTGRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.MOUSEBUTTONUP and not running:
            # account for clicking the grid
            pos = pygame.mouse.get_pos()
            # figure out which square was clicked
            unitLen = int(WIDTH / GRID_SIZE)

            c = pos[0] // unitLen
            r = pos[1] // unitLen
            if r < GRID_SIZE and c < GRID_SIZE:
                board.flipCell(r, c)

    # if start was pressed, automatically perform a step
    if running:
        board.step()

    draw_cells()

    # draw the buttons at the bottom
    button('Stop' if running else 'Start', ((WIDTH - 300) / 4,
                                            HEIGHT - 60, 100, 40), RED if running else GREEN, toggle)
    button('Step', (100 + (WIDTH - 300) / 2,
                    HEIGHT - 60, 100, 40), BLUE, board.step)
    button('Reset', (200 + 3 * (WIDTH - 300) /
                     4, HEIGHT - 60, 100, 40), BLUE, reset)

    # updates whole screen, TODO optimize with dirty rectss
    pygame.display.update()
    # cap at 10 fps TODO make this user-regulated through a slider
    clock.tick(10)
