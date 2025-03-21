import pygame
from algorithms import UCS, Node
from visualization import draw, make_grid, get_clicked_position

# Initialize Pygame
pygame.init()
pygame.font.init()

# pygame window
WIDTH = 800
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UCS Pathfinding")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)

BUTTON_HEIGHT = 40
PADDING = 10
FPS = 60  # Set FPS for smooth UI rendering

def main(SCREEN, width):
    clock = pygame.time.Clock()  # Controls frame rate for smooth rendering
    ROWS = 25
    grid = make_grid(ROWS, width)
    start = None
    end = None
    running = True

    while running:
        clock.tick(FPS)  # Limits FPS for smooth UI updates
        SCREEN.fill(WHITE)  # Ensures smooth rendering

        #Draw grid
        draw(SCREEN, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:  # Left Click - Set Start, End, or Barrier
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                if row < len(grid) and col < len(grid[0]):
                    spot = grid[row][col]
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                    elif spot != start and spot != end:
                        spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right Click - Reset Node
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u and start and end:  # Press "U" to start UCS
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    UCS(lambda: draw(SCREEN, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:  # Press "C" to clear the grid
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

        pygame.display.flip()  # Smooth rendering using double buffering

    pygame.quit()


main(SCREEN, WIDTH)