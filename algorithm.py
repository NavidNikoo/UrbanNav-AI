import pygame
import heapq
import time
import tracemalloc
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

def AStar(draw, grid, start, end):
    tracemalloc.start()
    start_time = time.time()
    count = 0
    explored_count = 0
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
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return True, time.time() - start_time, explored_count, peak / 1024 #(true for finding end, algo exec time)


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
            explored_count +=1
    peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return False, time.time() - start_time, explored_count, peak / 1024

def UCS(draw, grid, start, end):
    tracemalloc.start()
    start_time = time.time()
    count = 0
    explored_count = 0
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
            peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return True, time.time() - start_time, explored_count, peak[1] / 1024

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
            explored_count +=1

    peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return False, time.time() - start_time, explored_count, peak[1] / 1024

def DLS(node, end, came_from, draw, depth, visited):
    if node == end:
        return True
    if depth == 0:
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
    tracemalloc.start()
    start_time = time.time()
    max_depth = len(grid) * len(grid[0])
    came_from = {}

    for depth in range(max_depth):
        visited = set()
        if DLS(start, end, came_from, draw, depth, visited):
            reconstruct_path(came_from, end, draw)
            end.make_end()
            peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return True, time.time() - start_time, len(visited), peak[1] / 1024
    peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return False, time.time() - start_time, 0, peak[1] / 1024

WIDTH = 700
HEIGHT = 850

def show_stats_pygame(screen, algo, exec_time, explored_count, memory_usage_kb, history_log):
    font = pygame.font.SysFont('arial', 22, bold=True)
    small_font = pygame.font.SysFont('arial', 18)

    history_line_height = 20
    visible_entries = len(history_log)

    overlay_width = 560
    overlay_x = (WIDTH - overlay_width) // 2

    top_padding = 20
    line_height = 30
    stat_lines = 3
    section_gap = 20

    base_section_height = stat_lines * line_height + section_gap
    history_section_height = visible_entries * history_line_height + section_gap
    close_button_height = 50

    overlay_height = base_section_height + history_section_height + close_button_height + top_padding
    overlay_y = (HEIGHT - overlay_height) // 2

    overlay_rect = pygame.Rect(overlay_x, overlay_y, overlay_width, overlay_height)

    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if close_button.collidepoint(event.pos):
                    showing = False

        # Dim background
        dim_surface = pygame.Surface((WIDTH, HEIGHT))
        dim_surface.set_alpha(180)
        dim_surface.fill((255, 255, 255))
        screen.blit(dim_surface, (0, 0))

        # Draw modal background
        pygame.draw.rect(screen, (220, 220, 220), overlay_rect, border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), overlay_rect, 3, border_radius=10)

        # Draw current stats
        y_cursor = overlay_y + top_padding
        screen.blit(font.render(f"Algorithm: {algo}", True, BLACK), (overlay_x + 20, y_cursor))
        y_cursor += line_height
        screen.blit(font.render(f"Execution Time: {exec_time:.6f} seconds", True, BLACK), (overlay_x + 20, y_cursor))
        y_cursor += line_height
        screen.blit(font.render(f"Explored Nodes: {explored_count}", True, BLACK), (overlay_x + 20, y_cursor))
        y_cursor += line_height
        screen.blit(font.render(f"Peak Memory: {memory_usage_kb:.2f} KB", True, BLACK), (overlay_x + 20, y_cursor))
        y_cursor += section_gap

        # History section
        screen.blit(small_font.render("Previous Runs:", True, (60, 60, 60)), (overlay_x + 20, y_cursor))
        y_cursor += section_gap

        for i, (h_algo, h_time, h_explored, h_memory) in enumerate(history_log):
            entry = small_font.render(f"{i + 1}. {h_algo} – {h_time:.3f}s – {h_explored} nodes - {h_memory:.2f} KB", True, (50, 50, 50))
            screen.blit(entry, (overlay_x + 20, y_cursor + i * history_line_height))

        # Close button at bottom
        close_button_y = overlay_y + overlay_height - close_button_height
        close_button = pygame.Rect(overlay_x + (overlay_width - 100) // 2, close_button_y + 5, 100, 40)
        pygame.draw.rect(screen, (180, 180, 180), close_button, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), close_button, 2, border_radius=6)
        close_text = font.render("Close", True, BLACK)
        screen.blit(close_text, close_text.get_rect(center=close_button.center))

        pygame.display.update()

