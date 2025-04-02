import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.data import Data
from torch_geometric.nn import GATConv
import math
import heapq

class GATHeuristic(nn.Module):
    def __init__(self, in_channels, hidden_channels, heads=2):
        super().__init__()
        self.gat1 = GATConv(in_channels, hidden_channels, heads=heads, concat=True)
        self.gat2 = GATConv(hidden_channels * heads, 1, heads=1, concat=False)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.elu(self.gat1(x, edge_index))
        return self.gat2(x, edge_index).view(-1)

def update_heuristics(grid, goal):
    for row in grid:
        for node in row:
            dx = node.row - goal.row
            dy = node.col - goal.col
            node.heuristic = round(math.sqrt(dx ** 2 + dy ** 2), 1)

def astar_path(grid, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))
    g_score = {start: 0}
    f_score = {start: heuristic_cost_estimate(start, goal)}
    came_from = {}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        visited.add(current)
        for neighbor in current.neighbors:
            if neighbor.is_barrier() or neighbor in visited:
                continue
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic_cost_estimate(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []

def heuristic_cost_estimate(node1, node2):
    dx = node1.row - node2.row
    dy = node1.col - node2.col
    return math.sqrt(dx ** 2 + dy ** 2)

def grid_to_graph(grid, path):
    nodes, edges, y = [], [], []
    idx_map, idx = {}, 0
    ROWS = len(grid)

    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            if not node.is_barrier():
                idx_map[(i, j)] = idx
                idx += 1

    path_set = set(path)

    def min_distance_to_path(node):
        return min(math.sqrt((node.row - p.row) ** 2 + (node.col - p.col) ** 2) for p in path_set)

    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            if not node.is_barrier():
                node_id = idx_map[(i, j)]
                nodes.append([i / ROWS, j / ROWS, node.heuristic])
                for neighbor in node.neighbors:
                    if not neighbor.is_barrier():
                        neighbor_id = idx_map[(neighbor.row, neighbor.col)]
                        edges.append([node_id, neighbor_id])
                distance = min_distance_to_path(node)
                y.append(distance)

    x = torch.tensor(nodes, dtype=torch.float)
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    y = torch.tensor(y, dtype=torch.float)
    return Data(x=x, edge_index=edge_index, y=y)

def train_gnn(data, model, epochs=50):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()

    for _ in range(epochs):
        model.train()
        optimizer.zero_grad()
        out = model(data)
        loss = loss_fn(out, data.y)
        loss.backward()
        optimizer.step()

    return model(data).detach()

def gnn_learn_and_update(grid, start, goal):
    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    path = astar_path(grid, start, goal)
    if not path:
        return

    update_heuristics(grid, goal)
    data = grid_to_graph(grid, path)
    model = GATHeuristic(3, 16, heads=2)
    predictions = train_gnn(data, model, epochs=50)

    SCALE = 1.0
    idx = 0
    for row in grid:
        for node in row:
            if not node.is_barrier():
                node.heuristic = round(node.heuristic + float(predictions[idx]) * SCALE, 1)
                idx += 1
