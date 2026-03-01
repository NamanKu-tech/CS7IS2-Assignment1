import csv
import math
import os
from datetime import datetime
from pyamaze import maze as _Maze

DIRECTION_MAP = {
    'N': (-1,  0),
    'S': ( 1,  0),
    'E': ( 0,  1),
    'W': ( 0, -1),
}


def get_maze_size(prompt='Maze size (e.g. 15): ', default=15):
    """Ask user for maze size with a fallback default. Maze size can't be 1."""
    try:
        size = int(input(prompt).strip())
        if size < 2:
            raise ValueError
    except ValueError:
        size = default
    return size


def manhattan(a, b):
    """
    Manhattan distance.
    h = |Δrow| + |Δcol|
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a, b):
    """
    Euclidean (straight-line) distance.
    h = sqrt(Δrow² + Δcol²)
    """
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


HEURISTICS = {
    'manhattan': manhattan,
    'euclidean': euclidean,
}


def _save_maze_csv(maze_map, filepath):
    """Save maze layout in pyamaze-compatible CSV format."""
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['  cell  ', 'E', 'W', 'N', 'S'])
        for cell, walls in maze_map.items():
            writer.writerow([str(cell),
                             int(walls['E']), int(walls['W']),
                             int(walls['N']), int(walls['S'])])


def get_or_create_maze(size: int, loop_percent: int = 0, maze_dir: str = None):
    """
    Return a pyamaze maze of the given size.
    Generates a new maze and saves it to temp/maze_{size}.csv.
    Subsequent calls with the same size reuse the saved maze.
    """
    save_dir = os.path.join(os.path.dirname(__file__), '..', 'temp')
    os.makedirs(save_dir, exist_ok=True)
    csv_path = os.path.join(save_dir, f'maze_{size}.csv')

    m = _Maze(size, size)
    if os.path.exists(csv_path):
        m.CreateMaze(loadMaze=csv_path)
        print(f'[maze] Loaded saved {size}x{size} maze from {os.path.basename(csv_path)}')
    else:
        m.CreateMaze(loopPercent=loop_percent)
        _save_maze_csv(m.maze_map, csv_path)
        print(f'[maze] Generated new {size}x{size} maze → saved to {os.path.basename(csv_path)}')
    return m


_DEFAULT_CSV = os.path.join(os.path.dirname(__file__), '..', 'temp', 'results.csv')

_CSV_FIELDS = [
    'timestamp', 'algorithm', 'maze_size',
    'path_length', 'cells_explored', 'iterations',
    'time_ms', 'scenario', 'path_cost', 'extra',
]


def save_stats(algorithm: str, maze_size: int, path_length: int,
               time_ms: float, cells_explored: int = None,
               iterations: int = None, scenario: str = 'unweighted',
               path_cost: float = None, extra: str = '',
               csv_path: str = None) -> str:
    """Append one result row to a shared CSV for later comparison / graphing."""
    path = os.path.abspath(csv_path or _DEFAULT_CSV)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    write_header = not os.path.exists(path) or os.path.getsize(path) == 0

    with open(path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_FIELDS)
        if write_header:
            writer.writeheader()
        writer.writerow({
            'timestamp':      datetime.now().isoformat(timespec='seconds'),
            'algorithm':      algorithm,
            'maze_size':      maze_size,
            'path_length':    path_length,
            'cells_explored': cells_explored if cells_explored is not None else '',
            'iterations':     iterations     if iterations     is not None else '',
            'time_ms':        f'{time_ms:.4f}',
            'scenario':       scenario,
            'path_cost':      f'{path_cost:.1f}' if path_cost is not None else '',
            'extra':          extra,
        })

    return path
