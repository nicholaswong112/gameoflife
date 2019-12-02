import pygame

# constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
LIGHTGRAY = (200, 200, 200)

GRID_SIZE = 20
WIDTH, HEIGHT = 700, 700

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

# game loop
loop = True
running = False # whether the simulation is running
while loop:

    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False
        # elif event.type == pygame.MOUSE:
        #     pass

    # draw the toolbar at the bottom
    pygame.draw.rect(window, LIGHTGRAY, (0, HEIGHT - 80, WIDTH, 80))
    button('Start/Stop', ((WIDTH - 300) / 4, HEIGHT - 60, 100, 40), BLUE)
    button('Step', (100 + (WIDTH - 300) / 2, HEIGHT - 60, 100, 40), BLUE)
    button('Reset', (200 + 3 * (WIDTH - 300) / 4, HEIGHT - 60, 100, 40), BLUE)
    
    # updates whole screen, TODO optimize with dirty rectsds
    pygame.display.update()
    clock.tick(20) # cap at 20 fps
