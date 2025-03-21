import pygame
import math
from queue import PriorityQueue
from algorithms import AStar, Node
from visualization import draw, make_grid, get_clicked_position

#pygame window
WIDTH = 700
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Car")
pygame.init()
pygame.font.init()

#pygame colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
TURQUOISE = (48, 213, 200)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (160, 160, 160)

BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50

class Button:
    def __init__(self, x, y, text):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = text
        self.color = LIGHT_GRAY
        self.active = False

    def draw(self, win):
        color = DARK_GRAY if self.active else self.color
        pygame.draw.rect(win, color, self.rect, border_radius=8)
        font = pygame.font.SysFont('arial', 22, bold=True)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        win.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def main(SCREEN, width):
    mode = None
    ROWS = 25
    grid = make_grid(ROWS, width)

    start = None
    end = None

    running = True

    button_y = HEIGHT - 80  # Move buttons to the bottom
    buttons = {
        'block': Button(10, button_y, "Block"),
        'open': Button(100, button_y, "Open"),
        'start': Button(200, button_y, "Start"),
        'goal': Button(300, button_y, "Goal"),
        'run': Button(400, button_y, "Run A*"),
        #'learn': Button(500, HEIGHT-700, "Learning"),
        'reset': Button(600, button_y, "Reset")
    }

    while running:
        SCREEN.fill(WHITE)  # Clear screen before redrawing
        draw(SCREEN, grid, ROWS, width)


        for key, button in buttons.items():
            button.active = (mode == key)
            button.draw(SCREEN)

        pygame.display.update()  # Ensure buttons are displayed


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                button_clicked = False
                for key, button in buttons.items():
                    if button.is_clicked(pos):
                        mode = key
                        button_clicked = True

                        if mode == 'run' and start and end:
                            AStar(lambda: draw(SCREEN, grid, ROWS, width), grid, start, end)
                        elif mode == 'reset':
                            start = None
                            end = None
                            grid = make_grid(ROWS, width)

                if button_clicked:
                    continue

            if pygame.mouse.get_pressed()[0]: #Left click, these will just be changed to buttons later
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()


            elif pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end: #start for algorithm
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                        AStar(lambda: draw(SCREEN, grid, ROWS, width), grid, start, end) #lambda is so we can pass the draw function to the algorithm

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()


main(SCREEN, WIDTH)