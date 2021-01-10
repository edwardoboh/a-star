import pygame
import math
from queue import PriorityQueue

# pygame.init()

width = 600
height = 600
n_of_rows = 40

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("A* Algorithm")

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
orange = (255, 165, 0)
black = (0, 0, 0)
purple = (128, 0, 128)
turquoise = (64, 224, 208)

class Spot:
    def __init__(self, row, col, spot_width, total_rows):
        self.row = row
        self.col = col
        self.x = col * spot_width
        self.y = row * spot_width
        self.spot_width = spot_width
        self.color = white
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == red
    
    def is_open(self):
        return self.color == green
    
    def is_obstacle(self):
        return self.color == black
    
    def is_start(self):
        return self.color == orange

    def is_end(self):
        return self.color == turquoise


    
    def reset(self):
        self.color = white

    def make_start(self):
        self.color = orange

    def make_end(self):
        self.color = turquoise
    
    def make_closed(self):
        self.color = red
    
    def make_open(self):
        self.color = green
    
    def make_barrier(self):
        self.color = black
    
    def make_path(self):
        self.color = purple
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.y, self.x, self.spot_width, self.spot_width))

    def update_neighbors(self, grid):
        # self.neighbors = []
        # Add lower spot to neighbors
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.col])
        
        # Add upper spot to neighbors
        if self.row > 0 and not grid[self.row - 1][self.col].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        # Add left spot to neighbors
        if self.col > 0 and not grid[self.row][self.col - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col - 1])
        
        # Add right spot to neighbors
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.col + 1])


    def __lt__(self, other):
        return False


def h(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

def make_grid(total_rows, grid_width):
    grid = []
    line_gap = grid_width // total_rows

    for i in range(total_rows):
        grid.append([])
        for j in range(total_rows):
            spot = Spot(i, j, line_gap, total_rows)
            grid[i].append(spot)
    return grid

def draw_grid(window, grid):
    for row in grid:
        for spot in row:
            spot.draw(window)

def draw_grid_lines(window, total_rows, grid_width):
    line_gap = grid_width // total_rows

    for i in range(total_rows):
        pygame.draw.line(window, blue, ( 0, i * line_gap), (grid_width, i * line_gap))
    
    for j in range(total_rows):
        pygame.draw.line(window, blue, ( j * line_gap, 0), ( j * line_gap, grid_width))

def draw_grid_and_lines(window, grid, total_rows, grid_width):
    window.fill(white)

    draw_grid(window, grid)
    draw_grid_lines(window, total_rows, grid_width)

    pygame.display.update()

# helper function to help us get which spot was clicked by mouse

def get_clicked_pos(position, total_rows, grid_width):
    line_gap = grid_width // total_rows
    y, x = position
    row = y // line_gap
    col = x // line_gap
    return row, col

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw_grid_n_lines, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set_hash = {start}
    open_set.put((0, count, start))
    # open_set_hash.add(start)
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    while not open_set.empty():
        draw_grid_n_lines()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            current.make_end()
            reconstruct_path(came_from, current, draw_grid_n_lines)
            return True
        
        for neighbor in current.neighbors:
            temp_gscore = g_score[current] + 1
            if temp_gscore < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_gscore
                f_score[neighbor] = temp_gscore + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        if current != start:
            current.make_closed()

def main(window, grid_width):
    rows = n_of_rows
    grid = make_grid(rows, grid_width)

    start = None
    end = None

    run = True
    is_start = False

    while run:
        draw_grid_and_lines(window, grid, n_of_rows, grid_width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if is_start:
                continue

            if pygame.mouse.get_pressed()[0]:   #check if the left mouse button was pressed. middle mouse is [1]
                position = pygame.mouse.get_pos()
                row, col = get_clicked_pos(position, rows, grid_width)
                spot = grid[row][col]
                if not start:
                    start = spot
                    spot.make_start()
                elif not end and spot != start:
                    end = spot
                    spot.make_end()
                elif spot != start and spot != end:
                # elif not spot.is_start() and not spot.is_end():
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]: #check if the right mouse button was pressed
                position = pygame.mouse.get_pos()
                row, col = get_clicked_pos(position, n_of_rows, grid_width)
                spot = grid[row][col]
                if spot.is_start():
                    spot.reset()
                    start = None
                elif spot.is_end():
                    spot.reset()
                    end = None
                else:
                    spot.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for spot in row:
                            grid[spot.row][spot.col].update_neighbors(grid)
                algorithm(lambda: draw_grid_and_lines(window, grid, n_of_rows, width), grid, start, end)
                    

main(window, width)