#!/usr/bin/env python3
# ============================================================
#  demos/04_astar_euclidean.py  —  A* with Euclidean heuristic
# ============================================================
#  h(n) = sqrt(Δrow² + Δcol²)
#  Also admissible — straight-line distance never overestimates.
#  Less informed than Manhattan on grids (Euclidean ≤ Manhattan)
#  so it explores slightly more cells, but still far fewer than BFS.
# ============================================================
import sys, os, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyamaze import agent, COLOR, textLabel
from solvers import AStarSolver
from utils  import get_maze_size, save_stats, get_or_create_maze, WeightedMaze


def main():
    parser = argparse.ArgumentParser(description='A* (Euclidean) maze solver')
    parser.add_argument('--save', action='store_true',
                        help='Append stats to temp/results.csv')
    args = parser.parse_args()

    print('=' * 45)
    print('   A*  —  Euclidean Heuristic')
    print('=' * 45)

    mode = input('Enter mode — [u]nweighted / [w]eighted: ').strip().lower()
    weighted = mode.startswith('w')

    size = get_maze_size()
    m    = get_or_create_maze(size, loop_percent=50)
    wm   = WeightedMaze(m, seed=42) if weighted else None

    solver = AStarSolver(m, heuristic='euclidean',
                         weights=wm.weights if wm else None)
    t0 = time.perf_counter()
    path, stats = solver.solve()
    elapsed = time.perf_counter() - t0
    cost = wm.path_cost(path) if wm else None

    print(f"Path length   : {len(path)} steps")
    if cost is not None:
        print(f"Path cost     : {cost}")
    print(f"Cells explored: {stats['cells_explored']}")
    print(f"Heuristic     : {stats['heuristic']}")
    print(f"Time          : {elapsed*1000:.2f} ms")

    if args.save:
        csv_path = save_stats(
            algorithm='A*(Euclidean)', maze_size=size,
            path_length=len(path), time_ms=elapsed*1000,
            cells_explored=stats['cells_explored'],
            scenario='weighted' if weighted else 'unweighted',
            path_cost=cost,
        )
        print(f"Stats saved → {csv_path}")

    a = agent(m, footprints=True, shape='arrow', color=COLOR.cyan, filled=True)
    if wm:
        wm.draw()
        wm.keep_text_on_top()

    textLabel(m, 'Algorithm',      'A* (Euclidean)')
    textLabel(m, 'Mode',           'weighted' if weighted else 'unweighted')
    textLabel(m, 'Heuristic',      'h = sqrt(Δrow² + Δcol²)')
    textLabel(m, 'Maze Size',      f'{size} x {size}')
    textLabel(m, 'Path Length',    len(path))
    if cost is not None:
        textLabel(m, 'Path Cost', cost)
    textLabel(m, 'Cells Explored', stats['cells_explored'])
    textLabel(m, 'Time (ms)',      f'{elapsed*1000:.2f}')

    m.tracePath({a: path}, delay=100)
    m.run()


if __name__ == '__main__':
    main()
