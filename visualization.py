import pygame
from algorithms import Node

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_grid(SCREEN, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(SCREEN, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(SCREEN, BLACK, (j * gap, 0), (j * gap, width))

def draw(SCREEN, grid, rows, width):
    SCREEN.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(SCREEN)
    draw_grid(SCREEN, rows, width)
    pygame.display.update()

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def get_clicked_position(position, rows, width):
    gap = width // rows
    y, x = position
    row = y // gap
    col = x // gap
    return row, col