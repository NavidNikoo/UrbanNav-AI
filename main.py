import pygame
import math
from queue import PriorityQueue

#pygame window
WIDTH = 800
HEIGHT = 800
WINDOW = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("AI Car")

#pygame colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
TURQUOISE = (48, 213, 200)

#Class for nodes in graph
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    #Below are our methods to tell us the state of the node

    #getters
    def get_position(self):
        return self.row, self.col #(row, col)

    def is_explored(self): #red square
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == GRAY

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == ORANGE

    def reset(self):
        self.color == WHITE

    #setters
    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = GRAY

    def make_end(self):
        self.color = ORANGE

    def make_path(self):
        self.color = TURQUOISE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other): #lt = 'less than', for comparing two different nodes, will expand later
        return False


def heuristics(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    GAP = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, GAP, rows)
            grid[i].append(node)

    return grid

def draw_grid(window, rows, width):
    GAP = width // rows
    # horizontal lines
    for i in range(rows):
        pygame.draw.line(window, BLACK, (0, i * GAP), (width, i * GAP))
    #vertical lines
        for j in range(rows):
            pygame.draw.line(window, BLACK, (j * GAP, 0), (j * GAP, width))


def draw(window, grid, rows, width):
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()

def get_clicked_position(position, rows, width):
    GAP = width // rows
    y, x = position

    row = y // GAP
    col = x // GAP

    return row, col


def main(window, width):
    ROWS = 10
    grid = make_grid(ROWS, width)

    start = None
    end = None

    running = True
    started = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pass



    pygame.quit()

















