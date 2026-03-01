from .base import Solver


class DFSSolver(Solver):
    """
    Depth-First Search.
    Dives as deep as possible before backtracking.
    No shortest-path guarantee.
    """

    def solve(self):
        stack           = [self.start]
        came_from       = {self.start: None}
        closed          = set()
        cells_processed = 0

        while stack:
            current = stack.pop()

            if current in closed:
                continue
            closed.add(current)
            cells_processed += 1

            if current == self.goal:
                break

            for neighbour in self.neighbours(current):
                if neighbour not in came_from:
                    came_from[neighbour] = current
                    stack.append(neighbour)

        path = self.reconstruct_path(came_from)
        return path, {'cells_explored': cells_processed}
