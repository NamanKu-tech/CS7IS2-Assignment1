import heapq
from .base import Solver
from utils.maze_utils import DIRECTION_MAP, HEURISTICS


class AStarSolver(Solver):
    """
    A* Search with a configurable heuristic.

    Args:
        m:          pyamaze maze object
        heuristic:  'manhattan' (default) or 'euclidean'
        weights:    optional dict of cell weights for Weighted A*
    """

    def __init__(self, m, heuristic='manhattan', weights=None):
        super().__init__(m)
        if heuristic not in HEURISTICS:
            raise ValueError(f"Unknown heuristic '{heuristic}'. "
                             f"Choose from: {list(HEURISTICS)}")
        self.heuristic_name = heuristic
        self.h = HEURISTICS[heuristic]
        self.weights = weights

    def solve(self):
        open_set  = [(self.h(self.start, self.goal), self.start)]
        came_from = {self.start: None}
        g_score   = {self.start: 0}
        closed    = set()
        cells_processed = 0

        while open_set:
            _, current = heapq.heappop(open_set)

            if current in closed:
                continue

            closed.add(current)
            cells_processed += 1

            if current == self.goal:
                break

            for neighbour in self.neighbours(current):
                if neighbour in closed:
                    continue

                step_cost   = self.weights[neighbour] if self.weights else 1
                tentative_g = g_score[current] + step_cost

                if neighbour not in g_score or tentative_g < g_score[neighbour]:
                    g_score[neighbour]   = tentative_g
                    f_score              = tentative_g + self.h(neighbour, self.goal)
                    came_from[neighbour] = current
                    heapq.heappush(open_set, (f_score, neighbour))

        path = self.reconstruct_path(came_from)
        return path, {
            'cells_explored': cells_processed,
            'heuristic':      self.heuristic_name,
        }
