import pygame
import math
import heapq
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

pygame.init()

WIDTH = 800
HEIGHT = 700
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("AI Car 5x5 Grid with A* + Learning")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (160, 160, 160)
YELLOW = (255, 255, 0)

ROWS = 5
BUTTON_WIDTH = 120
BUTTON_HEIGHT = 50

class Node:
    def __init__(self, row, col, x, y):
        self.row = row
        self.col = col
        self.x = x
        self.y = y
        self.color = BLACK
        self.h = 0

    def draw(self, win, gap):
        pygame.draw.circle(win, self.color, (self.x, self.y), gap // 10)

    def set_start(self):
        self.color = GREEN

    def set_goal(self):
        self.color = RED

    def set_path(self):
        self.color = BLUE

    def reset(self):
        self.color = BLACK

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return isinstance(other, Node) and self.row == other.row and self.col == other.col

class Edge:
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.blocked = False

    def draw(self, win):
        color = GRAY if self.blocked else BLACK
        pygame.draw.line(win, color, (self.start_node.x, self.start_node.y), (self.end_node.x, self.end_node.y), 4)

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

class SimpleGNN(nn.Module):
    def __init__(self):
        super(SimpleGNN, self).__init__()
        self.fc = nn.Linear(2, 1)

    def forward(self, x):
        return self.fc(x)

def heuristic(a, b):
    return math.sqrt((a.row - b.row) ** 2 + (a.col - b.col) ** 2)

def update_heuristic_with_gnn(nodes, start_node, goal_node):
    model = SimpleGNN()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.MSELoss()

    train_data = []
    target_data = []

    for row in nodes:
        for node in row:
            train_data.append([node.row / ROWS, node.col / ROWS])
            target_data.append([heuristic(node, goal_node) / ROWS])

    train_tensor = torch.tensor(train_data, dtype=torch.float32)
    target_tensor = torch.tensor(target_data, dtype=torch.float32)

    for epoch in range(200):
        optimizer.zero_grad()
        output = model(train_tensor)
        loss = criterion(output, target_tensor)
        loss.backward()
        optimizer.step()

    learned_h = model(train_tensor).detach().numpy().flatten()

    idx = 0
    for row in nodes:
        for node in row:
            node.h = round(learned_h[idx] * ROWS, 2)
            idx += 1
    
    print("Learning complete")

def update_heuristic_euclidean(nodes, goal_node):
    for row in nodes:
        for node in row:
            node.h = round(heuristic(node, goal_node), 2)
    print("Heuristic initialized with Euclidean distance")

def reset_grid(nodes, edges):
    for row in nodes:
        for node in row:
            node.reset()
            node.h = 0
    for edge in edges:
        edge.blocked = False
    print("Grid reset")

def a_star(start, goal, edges):
    open_set = []
    count = 0
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current == goal:
            reconstruct_path(came_from, goal)
            return True

        for edge in edges:
            if edge.blocked:
                continue
            if edge.start_node == current:
                neighbor = edge.end_node
            elif edge.end_node == current:
                neighbor = edge.start_node
            else:
                continue

            temp_g = g_score[current] + 1

            if neighbor not in g_score or temp_g < g_score[neighbor]:
                g_score[neighbor] = temp_g
                f_score = temp_g + neighbor.h
                count += 1
                heapq.heappush(open_set, (f_score, count, neighbor))
                came_from[neighbor] = current

    return False

def reconstruct_path(came_from, current):
    while current in came_from:
        current = came_from[current]
        if current:
            current.set_path()

def main(win):
    global WIDTH, HEIGHT
    mode = None
    start_node = None
    goal_node = None

    gap = min(WIDTH - 200, HEIGHT - 150) // ROWS
    nodes = [[Node(i, j, 100 + j*gap, 100 + i*gap) for j in range(ROWS)] for i in range(ROWS)]
    edges = []
    for i in range(ROWS):
        for j in range(ROWS):
            if j < ROWS-1:
                edges.append(Edge(nodes[i][j], nodes[i][j+1]))
            if i < ROWS-1:
                edges.append(Edge(nodes[i][j], nodes[i+1][j]))

    buttons = {
        'block': Button(WIDTH-150, 100, "Block"),
        'open': Button(WIDTH-150, 170, "Open"),
        'start': Button(WIDTH-150, 240, "Start"),
        'goal': Button(WIDTH-150, 310, "Goal"),
        'run': Button(WIDTH-150, 380, "Run A*"),
        'learn': Button(WIDTH-150, 450, "Learning"),
        'reset': Button(WIDTH-150, 520, "Reset")
    }

    while True:
        win.fill(WHITE)
        WIDTH, HEIGHT = win.get_size()
        
        gap = min(WIDTH-200, HEIGHT-150) // ROWS
        for i in range(ROWS):
            for j in range(ROWS):
                nodes[i][j].x = 100 + j*gap
                nodes[i][j].y = 100 + i*gap

        for row in nodes:
            for node in row:
                node.draw(win, gap)

        for edge in edges:
            edge.draw(win)

        for key, button in buttons.items():
            button.active = (mode == key)
            button.draw(win)

        font = pygame.font.SysFont(None, 20)
        for i, row in enumerate(nodes):
            for j, node in enumerate(row):
                text_surface = font.render(f"({i},{j}): {node.h}", True, BLUE)
                win.blit(text_surface, (100 + j * gap, HEIGHT - 120 + i * 15))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # 버튼 클릭 처리
                button_clicked = False
                for key, button in buttons.items():
                    if button.is_clicked(pos):
                        mode = key
                        button_clicked = True
                        if mode == 'learn' and start_node and goal_node:
                            update_heuristic_with_gnn(nodes, start_node, goal_node)
                        elif mode == 'run' and start_node and goal_node:
                            a_star(start_node, goal_node, edges)
                        elif mode == 'reset':
                            start_node, goal_node = None, None
                            reset_grid(nodes, edges)
                        continue
                if button_clicked: continue

                # 엣지 클릭 처리
                edge_clicked = False
                for edge in edges:
                    line_center = pygame.math.Vector2(edge.start_node.x, edge.start_node.y).lerp(
                        (edge.end_node.x, edge.end_node.y), 0.5)
                    if pygame.math.Vector2(pos).distance_to(line_center) < 15:
                        if mode == 'block':
                            edge.blocked = True
                        elif mode == 'open':
                            edge.blocked = False
                        edge_clicked = True
                        break
                if edge_clicked: continue

                # 노드 클릭 처리
                for row in nodes:
                    for node in row:
                        if pygame.math.Vector2(pos).distance_to((node.x, node.y)) < gap//4:
                            if mode == 'start':
                                if start_node: start_node.reset()
                                start_node = node
                                node.set_start()
                            elif mode == 'goal':
                                if goal_node: goal_node.reset()
                                goal_node = node
                                node.set_goal()

                            if start_node and goal_node:
                                update_heuristic_euclidean(nodes, goal_node)
                            break

        pygame.display.update()

main(WINDOW)
