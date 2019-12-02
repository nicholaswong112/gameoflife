import pygame

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTGRAY = (200, 200, 200)

GRID_SIZE = 20
WIDTH, HEIGHT = 700, 800 # TODO make this dynamic

# set up
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
cells = [[False for i in range(GRID_SIZE)] for j in range(GRID_SIZE)] # all False (dead) initially
# loop variables
loop = True
running = False # whether the simulation is running
# helper function for step() -- accounts for bounds
def neighborCount(row, col):
    count = 0
    for r in range(row - 1, row + 2):
        for c in range(col - 1, col + 2):
            # skip itself
            if r == row and c == col: continue
            # check out of bounds
            if r < 0 or c < 0 or r >= GRID_SIZE or c >= GRID_SIZE: continue
            if cells[r][c]:
                count += 1
    return count
# runs a step of the simulation
# governed by these rules
# dead -> alive if exactly 3 neighbors
# alive -> dead if not exactly 2 or 3 neighbors
def step():
    global cells
    tmp = [[False for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            tmp[r][c] = cells[r][c]
            neighbors = neighborCount(r, c)
            if cells[r][c]:
                # alive
                if neighbors < 2 or neighbors > 3:
                    tmp[r][c] = False
            else:
                # dead
                if neighbors == 3:
                    tmp[r][c] = True
    cells = tmp

def draw_cells():
    unitLen = WIDTH / GRID_SIZE
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            dimensions = (c * unitLen, r * unitLen, unitLen, unitLen)
            pygame.draw.rect(window, BLACK if cells[r][c] else WHITE, dimensions)
def reset():
    global cells
    global running
    cells = [[False for i in range(GRID_SIZE)] for j in range(GRID_SIZE)] # reset to all dead
    running = False
def toggle():
    global running
    running = not running

# game loop
while loop:

    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        elif event.type == pygame.MOUSEBUTTONUP and not running:
            pos = pygame.mouse.get_pos()
            # figure out which square was clicked
            unitLen = int(WIDTH / GRID_SIZE)
            c = pos[0] // unitLen
            r = pos[1] // unitLen
            if r < GRID_SIZE and c < GRID_SIZE:
                cells[r][c] = not cells[r][c]
    
    if running:
        step()
    
    draw_cells()

    # draw the toolbar at the bottom
    pygame.draw.rect(window, LIGHTGRAY, (0, HEIGHT - 80, WIDTH, 80))
    button('Stop' if running else 'Start', ((WIDTH - 300) / 4, HEIGHT - 60, 100, 40), RED if running else GREEN, toggle)
    button('Step', (100 + (WIDTH - 300) / 2, HEIGHT - 60, 100, 40), BLUE, step)
    button('Reset', (200 + 3 * (WIDTH - 300) / 4, HEIGHT - 60, 100, 40), BLUE, reset)
    
    # updates whole screen, TODO optimize with dirty rectss
    pygame.display.update()
    clock.tick(10) # cap at 10 fps TODO make this user-regulated through a slider
