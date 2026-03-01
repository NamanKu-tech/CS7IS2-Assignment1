from utils.maze_utils import DIRECTION_MAP


class Solver:
    """
    Base class for all maze-solving algorithms.

    Subclasses must implement solve() which returns:
        (path, stats_dict)
    where path is {parent: child} for pyamaze tracePath.
    """

    def __init__(self, m):
        self.m     = m
        self.start = (m.rows, m.cols)
        self.goal  = (1, 1)

    def neighbours(self, cell):
        """Return list of reachable neighbour cells."""
        r, c = cell
        result = []
        for d, (dr, dc) in DIRECTION_MAP.items():
            if self.m.maze_map[cell][d]:
                result.append((r + dr, c + dc))
        return result

    def neighbours_dict(self, cell):
        """Return {direction: neighbour} dict."""
        r, c = cell
        nb = {}
        for d, (dr, dc) in DIRECTION_MAP.items():
            if self.m.maze_map[cell][d]:
                nb[d] = (r + dr, c + dc)
        return nb

    def reconstruct_path(self, came_from):
        """Backtrack from goal to start, return {parent: child} dict."""
        path = {}
        cell = self.goal
        while cell != self.start:
            path[came_from[cell]] = cell
            cell = came_from[cell]
        return path

    def solve(self):
        """
        Run the algorithm. Must be implemented by subclasses.
        Returns: (path_dict, stats_dict)
        """
        raise NotImplementedError("Subclasses must implement solve()")
