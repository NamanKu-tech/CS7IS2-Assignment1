#!/usr/bin/env python3
# ============================================================
#  demos/02_dfs.py  —  Depth-First Search
# ============================================================
import sys, os, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyamaze import agent, COLOR, textLabel
from solvers import DFSSolver
from utils  import get_maze_size, save_stats, get_or_create_maze, WeightedMaze


def main():
    parser = argparse.ArgumentParser(description='DFS maze solver')
    parser.add_argument('--save', action='store_true',
                        help='Append stats to temp/results.csv')
    args = parser.parse_args()

    print('=' * 45)
    print('   DFS  —  Depth-First Search')
    print('=' * 45)

    mode = input('Enter mode — [u]nweighted / [w]eighted: ').strip().lower()
    weighted = mode.startswith('w')

    size = get_maze_size()
    m    = get_or_create_maze(size, loop_percent=50)
    wm   = WeightedMaze(m, seed=42) if weighted else None

    solver = DFSSolver(m)
    t0 = time.perf_counter()
    path, stats = solver.solve()
    elapsed = time.perf_counter() - t0
    cost = wm.path_cost(path) if wm else None

    print(f"Path length   : {len(path)} steps")
    if cost is not None:
        print(f"Path cost     : {cost}")
    print(f"Cells explored: {stats['cells_explored']}")
    print(f"Time          : {elapsed*1000:.2f} ms")

    if args.save:
        save_stats(
            algorithm='DFS', maze_size=size,
            path_length=len(path), time_ms=elapsed*1000,
            cells_explored=stats['cells_explored'],
            scenario='weighted' if weighted else 'unweighted',
            path_cost=cost,
        )

    a = agent(m, footprints=True, shape='arrow', color=COLOR.red, filled=True)
    if wm:
        wm.draw()
        wm.keep_text_on_top()

    textLabel(m, 'Algorithm',      'DFS')
    textLabel(m, 'Mode',           'weighted' if weighted else 'unweighted')
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
