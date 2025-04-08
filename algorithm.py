import pygame
import heapq
from queue import PriorityQueue

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)
TURQUOISE = (48, 213, 200)

def draw_grid(SCREEN, rows, width):
    GAP = width // rows
    # horizontal lines
    for i in range(rows):
        pygame.draw.line(SCREEN, BLACK, (0, i * GAP), (width, i * GAP))
    #vertical lines
        for j in range(rows):
            pygame.draw.line(SCREEN, BLACK, (j * GAP, 0), (j * GAP, width))


def draw(SCREEN, grid, rows, width):
    SCREEN.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(SCREEN)

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
        self.heuristic = 0

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
        self.heuristic = 0

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def get_position(self):
        return (self.row, self.col)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
    def __lt__(self, other): #lt = 'less than', for comparing two different nodes, will expand later
        return False

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def heuristics(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)

# def AStar(draw, grid, start, end): #passing
#     count = 0
#     open_set = PriorityQueue()
#     open_set.put((0, count, start)) #put equivalent to push/append, API for PriorityQueue DS
#     came_from = {} #keeps track of which node came from which node

#     g_score = {spot: float("inf") for row in grid for spot in row} #cost of the path from the starting node to a given node 'n'
#     g_score[start] = 0

#     f_score = {spot: float("inf") for row in grid for spot in row}  #f-score to determine which node to explore next. f(n) = g(n) + h(n).
#     f_score[start] = heuristics(start.get_position(), end.get_position())

#     open_set_hash = {start}

#     while not open_set.empty():
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()

#         current = open_set.get()[2]
#         open_set_hash.remove(current)

#         if current == end:
#             reconstruct_path(came_from, end, draw)
#             end.make_end()
#             return True #make path

#         for neighbor in current.neighbors:
#             temp_g_score = g_score[current] + 1

#             if temp_g_score < g_score[neighbor]:
#                 came_from[neighbor] = current
#                 g_score[neighbor] = temp_g_score
#                 f_score[neighbor] = temp_g_score + heuristics(neighbor.get_position(), end.get_position())
#                 if neighbor not in open_set_hash:
#                     count += 1
#                     open_set.put((f_score[neighbor], count, neighbor))
#                     open_set_hash.add(neighbor)
#                     neighbor.make_open()

#         draw()

#         if current != start:
#             current.make_closed()

#     return False

def AStar(draw, grid, start, end):
    count = 0
    open_set = []
    heapq.heappush(open_set, (start.heuristic, count, start))

    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = start.heuristic  # Use Heuristic learned from GNN

    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + neighbor.heuristic  # Applying Heristic

                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def UCS(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}

    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

#Depth limited Search
def DLS(node, end, came_from, draw, depth, visited):
    if depth == 0:
        if node == end:
            return True
        return False

    visited.add(node)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    for neighbor in node.neighbors:
        if neighbor not in visited and not neighbor.is_barrier():
            came_from[neighbor] = node
            neighbor.make_open()
            draw()
            pygame.time.delay(10)

            if DLS(neighbor, end, came_from, draw, depth - 1, visited):
                return True

    if not node.is_start():
        node.make_closed()
        draw()

    return False

#Iterative Deepening
def IterativeDeepening(draw, grid, start, end):
    max_depth = len(grid) * len(grid[0])
    came_from = {}

    for depth in range(max_depth):
        visited = set()
        if DLS(start, end, came_from, draw, depth, visited):
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
    return False