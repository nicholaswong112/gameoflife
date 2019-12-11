import pygame
from board import Board

### CONSTANTS ###
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
LIGHTGRAY = (200, 200, 200)

GRID_SIZE = 20
STARTING_SPEED = 10  # fps
WIDTH, HEIGHT = 700, 800  # TODO make this dynamic

### SET UP ###
# stuff for pygame
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game of Life')
# TODO add an icon?
clock = pygame.time.Clock()

# helper to create (text, pos)
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

board = Board(GRID_SIZE)
speed = STARTING_SPEED

# buttons
startStopBtn = pygame.Rect(28, 740, 140, 30)
downPts = [(196, 755), (236, 740), (236, 770)]
downBtn = pygame.Rect(0, 0, 0, 0)
upPts = [(296, 740), (296, 770), (336, 755)]
upBtn = pygame.Rect(0, 0, 0, 0)
stepBtn = pygame.Rect(364, 740, 140, 30)
resetBtn = pygame.Rect(532, 740, 140, 30)
buttonFont = pygame.font.SysFont("dejavusansmono", 24)

# loop variables
loop = True  # pygame loop switch
running = False  # whether the simulation is running

def draw_cells():
    unitLen = WIDTH / GRID_SIZE
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            # slight offsets to create grid effect
            dimensions = (c * unitLen + 1, r * unitLen +
                          1, unitLen - 2, unitLen - 2)
            pygame.draw.rect(
                window, BLACK if board.get(r, c) else WHITE, dimensions)

def draw_buttons():
    global downBtn, upBtn

    # Start/Stop button and text
    pygame.draw.rect(window, RED if running else GREEN, startStopBtn)
    ssText, ssPos = text_objects(
        'Stop' if running else 'Start', buttonFont, WHITE)
    ssPos.center = (28 + 70, 740 + 15)
    window.blit(ssText, ssPos)

    # speed fdisplay and controls
    speedText, speedPos = text_objects(
        str(speed) + 'fps', pygame.font.SysFont("dejavusansmono", 18), BLACK)
    speedPos.center = (246 + 20, 740 + 15)
    window.blit(speedText, speedPos)
    downBtn = pygame.draw.polygon(window, RED, downPts)
    upBtn = pygame.draw.polygon(window, GREEN, upPts)

    # Step button
    pygame.draw.rect(window, BLUE, stepBtn)
    stepText, stepPos = text_objects('Step', buttonFont, WHITE)
    stepPos.center = (364 + 70, 740 + 15)
    window.blit(stepText, stepPos)

    # Reset button
    pygame.draw.rect(window, RED, resetBtn)
    resetText, resetPos = text_objects('Reset', buttonFont, WHITE)
    resetPos.center = (532 + 70, 740 + 15)
    window.blit(resetText, resetPos)

# clears the cells matrix, sets `running` to False - called by Reset button
def reset():
    global running
    board.reset()
    running = False

# toggles `running` state - called by Start/stop button
def toggle():
    global running
    running = not running

# increases animation speed by 1, caps at 20fps - called by UP button
def incSpeed():
    global speed
    speed += 1
    if speed > 20:
        speed = 20

# decreases animation speed by 1, caps at 1fps - called by DOWN button
def decSpeed():
    global speed
    speed -= 1
    if speed < 1:
        speed = 1

### GAME LOOP ###
while loop:
    # clears screen
    window.fill(LIGHTGRAY)

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.MOUSEBUTTONUP:
            if startStopBtn.collidepoint(event.pos):
                toggle()
            elif downBtn.collidepoint(event.pos):
                decSpeed()
            elif upBtn.collidepoint(event.pos):
                incSpeed()
            elif stepBtn.collidepoint(event.pos):
                board.step()
            elif resetBtn.collidepoint(event.pos):
                reset()
            else:
                # account for clicking the grid
                pos = event.pos
                # figure out which square was clicked
                unitLen = int(WIDTH / GRID_SIZE)

                c = pos[0] // unitLen
                r = pos[1] // unitLen
                if r < GRID_SIZE and c < GRID_SIZE:
                    board.flipCell(r, c)

    # if running, automatically perform a step
    if running:
        board.step()

    draw_cells()

    draw_buttons()

    # updates whole screen, TODO optimize with dirty rectss
    pygame.display.update()

    # regulates FPS
    clock.tick(speed)
