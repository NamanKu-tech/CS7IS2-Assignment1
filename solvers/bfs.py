from collections import deque
from .base import Solver


class BFSSolver(Solver):
    """
    Breadth-First Search.
    Explores all cells at distance d before distance d+1.
    Guarantees fewest-steps path.
    """

    def solve(self):
        q = deque([self.start])
        came_from = {self.start: None}
        cells_processed = 0

        while q:
            current = q.popleft()
            cells_processed += 1

            if current == self.goal:
                break

            for neighbour in self.neighbours(current):
                if neighbour not in came_from:
                    came_from[neighbour] = current
                    q.append(neighbour)

        path = self.reconstruct_path(came_from)
        return path, {'cells_explored': cells_processed}
