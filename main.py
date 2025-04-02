import pygame
import math
from queue import PriorityQueue
from visualization import draw, make_grid, get_clicked_position
from torch_geometric.nn import GCNConv
import torch
import torch.nn as nn
import torch.nn.functional as F
from heuristic_update import update_heuristics, gnn_learn_and_update


# Initialize pygame
pygame.init()
pygame.font.init()

# Window settings
WIDTH = 700
HEIGHT = 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Car with GNN")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (160, 160, 160)

# Button dimensions
BUTTON_WIDTH = 100
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

def animated_draw(screen, grid, rows, width):
    draw(screen, grid, rows, width)
    pygame.display.update()

def main(SCREEN, width):
    mode = None
    ROWS = 25
    grid = make_grid(ROWS, width)
    start = None
    end = None
    running = True
    clock = pygame.time.Clock()
    BUTTON_WIDTH = 90
    BUTTON_HEIGHT = 40
    BUTTON_SPACING = 10
    START_X = 10
    BUTTON_Y = HEIGHT - 60

    buttons = {
        'block': Button(START_X + 0 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Block"),
        'runA*': Button(START_X + 1 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Run A*"),
        'runUCS': Button(START_X + 2 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Run UCS"),
        'start': Button(START_X + 3 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Start"),
        'goal': Button(START_X + 4 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Goal"),
        'learn': Button(START_X + 5 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Learn"),
        'reset': Button(START_X + 6 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Reset"),
}

    while running:
        clock.tick(60)
        SCREEN.fill(WHITE)
        draw(SCREEN, grid, ROWS, width)
        for key, button in buttons.items():
            button.active = (mode == key)
            button.draw(SCREEN)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for key, button in buttons.items():
                    if button.is_clicked(pos):
                        mode = key
                        if mode == 'runA*' and start and end:
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            from algorithm import AStar
                            AStar(lambda: animated_draw(SCREEN, grid, ROWS, width), grid, start, end)
                        elif mode == 'runUCS' and start and end:
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            from algorithm import UCS
                            UCS(lambda: animated_draw(SCREEN, grid, ROWS, width), grid, start, end)
                        elif mode == 'reset':
                            start = None
                            end = None
                            grid = make_grid(ROWS, width)
                            
                        # perform machine learning to update heuristic
                        elif mode == 'learn' and start and end:
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            gnn_learn_and_update(grid,start, end) # pass start and end

            if pygame.mouse.get_pressed()[0]:
                row, col = get_clicked_position(pygame.mouse.get_pos(), ROWS, width)
                if row < ROWS and col < ROWS:
                    node = grid[row][col]
                    if mode == 'block' and node != start and node != end:
                        node.make_barrier()
                    elif mode == 'start' and not start and node != end:
                        start = node
                        start.make_start()
                    elif mode == 'goal' and not end and node != start:
                        end = node
                        end.make_end()
                        update_heuristics(grid, end)

            elif pygame.mouse.get_pressed()[2]:
                row, col = get_clicked_position(pygame.mouse.get_pos(), ROWS, width)
                if row < ROWS and col < ROWS:
                    node = grid[row][col]
                    node.reset()
                    if node == start:
                        start = None
                    elif node == end:
                        end = None

    pygame.quit()

main(SCREEN, WIDTH)