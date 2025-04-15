import pygame
from visualization import draw, make_grid, get_clicked_position
from algorithm import AStar, UCS, IterativeDeepening, show_stats_pygame
from heuristic_update import update_heuristics, feedback_learn_and_update

# Initialize pygame
pygame.init()
pygame.font.init()

# Window settings
WIDTH = 700
HEIGHT = 850  # Increased to fit all buttons
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Searching Algorithm Comparation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (160, 160, 160)

# Button dimensions
BUTTON_WIDTH = 90
BUTTON_HEIGHT = 40
BUTTON_SPACING = 10
START_X = 10
BUTTON_Y = HEIGHT - 70

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
    last_algo = None
    last_time = None
    history_log = []
    clock = pygame.time.Clock()

    buttons = {
        # Top row
        'start': Button(START_X + 0 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y - 50, "Start"),
        'goal': Button(START_X + 1 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y - 50, "Goal"),
        'runA*': Button(START_X + 2 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y - 50, "Run A*"),
        'runUCS': Button(START_X + 3 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y - 50, "Run UCS"),
        'learn': Button(START_X + 4 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y - 50, "Learn"),
        'stats': Button(START_X + 5 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y - 50, "Stats"),
        # Bottom row
        'block': Button(START_X + 0 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Block"),
        'stop': Button(START_X + 1 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Stop Sign"),
        'light': Button(START_X + 2 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Traffic"),
        'reset': Button(START_X + 3 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "Reset"),
        'runID': Button(START_X + 4 * (BUTTON_WIDTH + BUTTON_SPACING), BUTTON_Y, "runID"),
    }

    while running:
        clock.tick(60)
        SCREEN.fill(WHITE)
        draw(SCREEN, grid, ROWS, width, show_icons=True)
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
                            found, exec_time, explored_count, memory_usage_kb = AStar(lambda: animated_draw(SCREEN, grid, ROWS, width), grid, start, end)
                            last_algo = "A* Search"
                            last_time = exec_time
                            last_memory = memory_usage_kb
                            history_log.append((last_algo, last_time,explored_count, last_memory))
                        elif mode == 'runUCS' and start and end:
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            found, exec_time,explored_count, memory_usage_kb = UCS(lambda: animated_draw(SCREEN, grid, ROWS, width), grid, start, end)
                            last_algo = "Uniform Cost Search"
                            last_time = exec_time
                            last_memory = memory_usage_kb
                            history_log.append((last_algo, last_time,explored_count, last_memory))
                        elif mode == 'runID' and start and end:
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            found, exec_time,explored_count, memory_usage_kb = IterativeDeepening(lambda: animated_draw(SCREEN, grid, ROWS, width), grid, start, end)
                            last_algo = "Iterative Deepening Search"
                            last_time = exec_time
                            last_memory = memory_usage_kb
                            history_log.append((last_algo, last_time,explored_count, last_memory))
                        elif mode == 'learn' and start and end:
                            for row in grid:
                                for node in row:
                                    node.update_neighbors(grid)
                            feedback_learn_and_update(grid, start, end)
                        elif mode == 'reset':
                            start = None
                            end = None
                            grid = make_grid(ROWS, width)
                        elif mode == 'stats':
                            if last_algo and last_time and last_memory is not None:
                                show_stats_pygame(SCREEN, last_algo, last_time, history_log[-1][2], last_memory, history_log)
                                mode = None

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
                    elif mode == 'stop':
                        node.has_stop_sign = True
                        node.traffic_light = None
                    elif mode == 'light':
                        node.traffic_light = 'red'
                        node.has_stop_sign = False

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