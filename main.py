import pyglet
from pyglet import image
from pyglet import clock
from pyglet import gl
import sys
import random

wall = image.load('images/Wall.jpg')
empty = image.load('images/Empty.jpg')
visited = image.load('images/Visited.jpg')
path = image.load('images/FinalPath.jpg')
home = image.load('images/Start.jpg')
worm = image.load('images/End.jpg')
to_worm = image.load('images/to_worm.jpg')

width = height = 0

home_x = home_y = 0

finish_x = finish_y = 0
finishes = []

maze = [[]]

neighbors = [(-1, 0), (0, -1), (0, 1), (1, 0)]

nodes_to_redraw = []
nodes_to_clear = [[]]

queues = [[]]

visited_arrs = [[]]

worms = []
worm_to_pick_up = 0
n_of_worms = 15
n_of_robots = 5
finished_robot = 0

at_homes = []
at_worms = []
going_homes = []
going_worms = []

redraw_state = 0
redraw_states = 0

n_of_pixels = 10
n_steps = 1
timer = 1 / 10


class Node:
    def __init__(self, type_node, x, y, image_node, h_cost=0):
        self.type_node = type_node
        self.x = x
        self.y = y
        self.image_node = image_node
        self.parent = None
        self.h_cost = h_cost

    def __str__(self):
        return "{ Type: " + str(self.type) + " h_cost: " + str(self.h_cost)


def find_worms(t):
    for x in range(n_of_robots):
        find_worm(x)


def find_worm(n_of_robot):
    global redraw_state, redraw_states, queues, home_x, home_y, finishes, worm_to_pick_up, at_homes, at_worms, visited_arrs, going_worms, going_homes, nodes_to_clear, finished_robot
    if at_homes[n_of_robot]:
        if len(worms) <= worm_to_pick_up:
            return
        queues[n_of_robot].append((maze[home_x][home_y].h_cost, home_x, home_y))
        finishes[n_of_robot][0] = worms[worm_to_pick_up][0]
        finishes[n_of_robot][1] = worms[worm_to_pick_up][1]
        worm_to_pick_up += 1
        at_homes[n_of_robot] = False
        going_worms[n_of_robot] = True
        visited_arrs[n_of_robot].clear()
    elif at_worms[n_of_robot]:
        queues[n_of_robot].append((maze[finishes[n_of_robot][0]][finishes[n_of_robot][1]].h_cost, finishes[n_of_robot][0], finishes[n_of_robot][1]))
        finishes[n_of_robot][0] = home_x
        finishes[n_of_robot][1] = home_y
        at_worms[n_of_robot] = False
        going_homes[n_of_robot] = True
        visited_arrs[n_of_robot].clear()
    current = min(queues[n_of_robot], key=lambda o: o[0])
    q_x, q_y = current[1], current[2]
    if q_x == finishes[n_of_robot][0] and q_y == finishes[n_of_robot][1]:
        if going_worms[n_of_robot]:
            at_worms[n_of_robot] = True
            going_homes[n_of_robot] = True
            going_worms[n_of_robot] = False
        elif going_homes[n_of_robot]:
            at_homes[n_of_robot] = True
            going_worms[n_of_robot] = True
            going_homes[n_of_robot] = False
        queues[n_of_robot].clear()
        finished_robot = n_of_robot
        redraw_state = 2
        return
    queues[n_of_robot].remove(current)
    visited_arrs[n_of_robot].append(maze[q_x][q_y])
    for x, y in neighbors:
        neigh_x = q_x + x
        neigh_y = q_y + y
        if abs(x) == abs(y):
            continue
        my_node = maze[neigh_x][neigh_y]
        if (q_x, q_y) != (home_x, home_y):
            nodes_to_redraw.append((maze[q_x][q_y].x, maze[q_x][q_y].y))
            nodes_to_clear[n_of_robot].append((maze[q_x][q_y].x, maze[q_x][q_y].y))
        if my_node.type_node == "W":
            continue
        if my_node in visited_arrs[n_of_robot]:
            continue
        visited_arrs[n_of_robot].append(my_node)
        my_node.h_cost = heuristic(neigh_x, finishes[n_of_robot][0], neigh_y, finishes[n_of_robot][1])
        queues[n_of_robot].append((my_node.h_cost, neigh_x, neigh_y))


def heuristic(x0, x1, y0, y1):
    return abs(x0 - x1) + abs(y0 - y1)


def load_maze():
    global maze, width, height, home_x, home_y, worms
    f = open("dataset/" + input("Input file name: ") + '.txt', 'r')
    lines = f.readlines()
    width, height = map(int, lines[0].split())
    maze = [[None for x in range(width)] for x in range(height)]

    int_w = 0
    int_h = 0

    for h in lines[1:]:
        for w in h:
            if w.upper() == "X":
                maze[int_h][int_w] = Node("W", int_w, (height - int_h - 1), wall)
            elif w == " ":
                maze[int_h][int_w] = Node("E", int_w, (height - int_h - 1), empty)
            int_w += 1
        int_w = 0
        int_h += 1
    for a in range(n_of_worms + 1):
        x = random.randint(1, height - 2)
        y = random.randint(1, width - 2)
        if a == n_of_worms:
            maze[x][y].type_node = "H"
            maze[x][y].image_node = home
            home_x = x
            home_y = y
            tmp_arr = []
            for z in worms:
                tmp_arr.append((heuristic(x, z[0], y, z[1]), [z[0], z[1]]))
            tmp_arr.sort(key=lambda tup: tup[0])
            worms.clear()
            for g in tmp_arr:
                worms.append(g[1])
            break
        maze[x][y].type_node = "R"
        maze[x][y].image_node = worm
        worms.append([x, y])
    init_robots()
    return


def init_robots():
    global at_homes, going_homes, at_worms, going_worms, finishes, queues, visited_arrs, nodes_to_clear
    at_homes = [True for x in range(n_of_robots)]
    at_worms = [False for x in range(n_of_robots)]
    going_homes = [False for x in range(n_of_robots)]
    going_worms = [True for x in range(n_of_robots)]
    finishes = [[0, 0] for x in range(n_of_robots)]
    queues = [[] for x in range(n_of_robots)]
    visited_arrs = [[] for x in range(n_of_robots)]
    nodes_to_clear = [[] for x in range(n_of_robots)]


def on_draw():
    global redraw_state, nodes_to_redraw, nodes_to_clear, finished_robot
    if redraw_state == 0:
        for lines in maze:
            for columns in lines:
                columns.image_node.blit(columns.x * n_of_pixels, columns.y * n_of_pixels)
        redraw_state = 1
    elif redraw_state == 1:
        for z in nodes_to_redraw:
            x, y = z
            visited.blit(x * n_of_pixels, y * n_of_pixels)
        nodes_to_redraw.clear()
    elif redraw_state == 2:
        for x, y in nodes_to_clear[finished_robot]:
            to_worm.blit(x * n_of_pixels, y * n_of_pixels)
        nodes_to_clear[finished_robot].clear()
        redraw_state = 1
    pyglet.gl.glFlush()


if __name__ == '__main__':
    load_maze()
    callback = find_worms
    config = gl.Config(double_buffer=False)
    window = pyglet.window.Window(height=height * n_of_pixels, width=width * n_of_pixels, resizable=False, config=config)
    clock.schedule_interval(callback, timer)
    window.push_handlers(on_draw=on_draw)
    pyglet.app.run()
