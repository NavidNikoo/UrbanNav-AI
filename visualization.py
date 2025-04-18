import pygame
from algorithm import Node

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
TURQUOISE = (48, 213, 200)

def draw_grid(SCREEN, rows, width):
    GAP = width // rows
    # horizontal lines
    for i in range(rows):
        pygame.draw.line(SCREEN, BLACK, (0, i * GAP), (width, i * GAP))
    #vertical lines
        for j in range(rows):
            pygame.draw.line(SCREEN, BLACK, (j * GAP, 0), (j * GAP, width))


def draw(SCREEN, grid, rows, width, show_icons=False, stop_img=None, traffic_img=None):
    SCREEN.fill(WHITE)
    font = pygame.font.SysFont("segoeuiemoji", 10)
    icon_font = pygame.font.SysFont("segoeuiemoji", 14)

    for row in grid:
        for node in row:
            node.draw(SCREEN)
            if node.heuristic > 0:
                text = font.render(f"{node.heuristic:.1f}", True, BLACK)
                SCREEN.blit(text, (node.x + 3, node.y + 3))

            if show_icons:
                if getattr(node, 'has_stop_sign', False) and stop_img:
                    SCREEN.blit(stop_img, (node.x + node.width // 4, node.y + node.width // 4))
                elif getattr(node, 'traffic_light', None) == 'red' and traffic_img:
                    SCREEN.blit(traffic_img, (node.x + node.width // 4, node.y + node.width // 4))

    draw_grid(SCREEN, rows, width)

def make_grid(rows, width):
    grid = []
    GAP = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, GAP, rows)
            grid[i].append(node)

    return grid

def get_clicked_position(position, rows, width):
    GAP = width // rows
    y, x = position

    row = y // GAP
    col = x // GAP

    return row, col