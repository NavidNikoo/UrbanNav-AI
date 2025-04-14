import math
import heapq

# Euclidiean Heuristic initial setting
def heuristic_cost_estimate(node1, node2):
    dx = node1.row - node2.row
    dy = node1.col - node2.col
    return math.sqrt(dx ** 2 + dy ** 2)

def update_heuristics(grid, goal):
    for row in grid:
        for node in row:
            dx = node.row - goal.row
            dy = node.col - goal.col
            base_heuristic = math.sqrt(dx ** 2 + dy ** 2)

            # weights 
            if getattr(node, 'has_stop_sign', False):
                base_heuristic += 0.5
            if getattr(node, 'traffic_light', None) == 'red':
                base_heuristic += 0.5

            node.heuristic = round(base_heuristic, 1)

# True value from A* Path
def get_astar_path(grid, start, end):
    open_set = []
    heapq.heappush(open_set, (start.heuristic, 0, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = start.heuristic
    open_set_hash = {start}

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in current.neighbors:
            if neighbor.is_barrier():
                continue
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + neighbor.heuristic
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], temp_g_score, neighbor))
                    open_set_hash.add(neighbor)
    return []

# Feedback updates
def feedback_learn_and_update(grid, start, goal, iterations=5, alpha=0.2, beta=1.0):
    for _ in range(iterations):
        path = get_astar_path(grid, start, goal)
        if not path:
            print("No path found during learning iteration.")
            return
        path_set = set(path)

        for row in grid:
            for node in row:
                if node.is_barrier():
                    continue

                base_penalty = beta
                if getattr(node, 'has_stop_sign', False):
                    base_penalty += 0.5
                if getattr(node, 'traffic_light', None) == 'red':
                    base_penalty += 0.5

                if node in path_set:
                    node.heuristic = max(0.0, node.heuristic - alpha)
                else:
                    node.heuristic += base_penalty*5
