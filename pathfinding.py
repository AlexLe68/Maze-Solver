import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A8 Pathfinding Algorithm")
#Color's RGB data
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

class Node:
    def __init__(self, row, col, node_width, total_rows):
        self.row = row
        self.col = col
        self.width = node_width
        self.total_rows = total_rows
        self.neighbors = []
        self.x = row * node_width
        self.y = col * node_width
        self.color = WHITE

    def get_pos(self):
        return self.row, self.col
    def get_pos(self):
        return self.col, self.row  
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
    def is_empty(self):
        return self.color == WHITE
    def make_closed(self):
        self.color = RED 
    def make_open(self):
        self.color = GREEN   
    def make_barrier(self):
        self.color = BLACK  
    def make_start(self):
        self.color = ORANGE
    def make_end(self):
        self.color = TURQUOISE
    def make_path(self):
        self.color = PURPLE
    def delete(self):
        self.color = WHITE
    def draw(self, win):
        pygame.draw.rect(win, self.color,(self.x,self.y,self.width,self.width))
    def update_neighbors(self, grid):
        self.neighbors = []
        #DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        #TOP
        if self.row > 1 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        #RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        #LEFT
        if self.col > 1 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def make_grid(rows,width):
    grid = []
    gap = width//rows
    for r in range(rows):
        grid.append([])
        for c in range(rows):
            node = Node(r,c,gap,rows)
            grid[r].append(node)
    return grid

def draw_grid(win,rows,width):
    gap = width // rows
    for r in range(rows):
        pygame.draw.line(win,BLACK,(0,r*gap),(width, r*gap))
        for c in range(rows):
            pygame.draw.line(win,BLACK,(c*gap,0), (c*gap,width))

def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win,rows,width)
    pygame.display.update()


def get_clicked_pos(pos,rows,width):
    gap = width//rows
    x,y = pos
    row = x//gap
    col = y//gap
    return row,col

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()
                
def algorithm(draw,grid,start,end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

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
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    return False

def main(win,width):
    ROWS = 50
    grid = make_grid(ROWS,width)
    start = end = None
    run = True
    algo_started = False
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if algo_started:
                continue
            if pygame.mouse.get_pressed()[0]: #left click
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                if not start:
                    start = node
                    node.make_start()
                elif not end and node != start:
                    end = node
                    node.make_end()
                elif node != start and node != end:
                    node.make_barrier()
            if pygame.mouse.get_pressed()[2]: #right click
                pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(pos,ROWS,width)
                node = grid[row][col]
                if node.is_start():
                    start = None
                    node.delete()
                elif node.is_end():
                    end = None
                    node.delete()
                else:
                    node.delete()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for rows in grid:
                        for node in rows:
                            start = end = None
                            node.delete()
                if event.key == pygame.K_SPACE and not algo_started:
                    for rows in grid:
                        for node in rows:
                            node.update_neighbors(grid)
                    
                    algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)


    pygame.quit()
main(WIN,WIDTH)