import pygame
import sys
from typing import Tuple, Dict
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
from math import floor, sqrt
from min_heap import MinHeap


class Map():
    def __init__(self, width, height):
        self.map = [(0, 0, 0) for i in range(width * height)]
        self.width = width
        self.height = height
        pass

    def neighbors(self, point):
        x, y = point
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i == x and j == y:
                    continue
                if i < 0 or j < 0 or i >= self.width or j >= self.height:
                    continue
                yield (i, j)
        pass

    def render_map(self):
        for i in range(self.width * self.height):
            x = i % self.width
            y = floor(i / self.width)
            pygame.draw.rect(screen, self.map[i], (x * 16, y * 16, 16, 16))
        pass

    def reconstruct_path(self, came_from: Dict[Tuple[int, int],
                                               Tuple[int, int]],
                         current: Tuple[int, int]):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    def xy_idx(self, x, y):
        return x + y * self.width

    def render_path(self, path):
        incr = 200 / len(path)
        i = 0
        for p in path:
            pygame.draw.rect(screen,
                             (0, 55 + i*incr, 0),
                             (p[0] * 16, p[1] * 16, 16, 16))
            i += 1

    def walk_from_astar(self,
                        point_1: Tuple[int, int],
                        point_2: Tuple[int, int], h):

        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}

        g_score = {}
        g_score[point_1] = 0.0

        f_score = {}
        f_score[point_1] = h(point_1)

        def get_default_infinity(x, m):
            return m[x] if x in m else sys.maxsize

        def min_heap_cmp(a, b):
            a_v = get_default_infinity(a, f_score)
            b_v = get_default_infinity(b, f_score)
            return a_v < b_v

        # Max element in this heap is just a
        # point that doesn't exist since it'll return sys.maxsize

        open_set = MinHeap(min_heap_cmp, max_v=(999, 999))
        open_set.insert(point_1)

        while True:
            current = open_set.pop()

            if current is None:
                return None

            if current == point_2:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.neighbors(current):
                # Square grid implies 1.0 distance
                tentative_g_score = get_default_infinity(current, g_score) + 1.0

                if tentative_g_score >= get_default_infinity(neighbor, g_score):
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + h(neighbor)

                if neighbor not in open_set:
                    open_set.insert(neighbor)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('A*')
    clock = pygame.time.Clock()
    running = True

    map = Map(16, 16)

    #Calculate the distance between point x and (15, 15)
    def distance(x):
        return sqrt(pow(abs(x[0] - 15), 2) + pow(abs(x[1] - 15), 2))

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        screen.fill((128, 128, 200))
        map.render_map()
        map.render_path(map.walk_from_astar((0, 0), (15, 15), distance))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

