#!/usr/bin/env python3
# ============================================================
#  demos/05_mdp_value_iteration.py  —  MDP Value Iteration
# ============================================================
#  Bellman update sweeps ALL states repeatedly until V converges.
#  V(s) = max_a [ R(s) + γ Σ P(s'|s,a) V(s') ]
# ============================================================
import sys, os, time, argparse
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pyamaze import agent, COLOR, textLabel
from solvers import MDPSolver
from utils  import get_maze_size, save_stats, get_or_create_maze, WeightedMaze

GAMMA         = 0.9
NOISE         = 0.2
LIVING_REWARD = -0.04


def main():
    parser = argparse.ArgumentParser(description='MDP Value Iteration maze solver')
    parser.add_argument('--save', action='store_true',
                        help='Append stats to temp/results.csv')
    args = parser.parse_args()

    print('=' * 50)
    print('   MDP  —  Value Iteration')
    print('=' * 50)

    mode = input('Enter mode — [u]nweighted / [w]eighted: ').strip().lower()
    weighted = mode.startswith('w')

    size = get_maze_size()
    m    = get_or_create_maze(size, loop_percent=50)
    wm   = WeightedMaze(m, seed=42) if weighted else None

    solver = MDPSolver(m, gamma=GAMMA, noise=NOISE, living_reward=LIVING_REWARD)

    t0 = time.perf_counter()
    path, stats = solver.solve()
    elapsed = time.perf_counter() - t0
    cost = wm.path_cost(path) if wm else None

    print(f"Converged in  : {stats['iterations']} iterations")
    print(f"Path length   : {len(path)} steps")
    if cost is not None:
        print(f"Path cost     : {cost}")
    print(f"Total cells   : {stats['total_cells']}")
    print(f"Time          : {elapsed*1000:.2f} ms")
    print(f"V(start)      : {stats['V'].get((m.rows, m.cols), 0):.4f}")

    if args.save:
        csv_path = save_stats(
            algorithm='MDP-VI', maze_size=size,
            path_length=len(path), time_ms=elapsed*1000,
            iterations=stats['iterations'],
            scenario='weighted' if weighted else 'unweighted',
            path_cost=cost,
        )
        print(f"Stats saved → {csv_path}")

    a = agent(m, footprints=True, shape='arrow', color=COLOR.yellow, filled=True)
    if wm:
        wm.draw()
        wm.keep_text_on_top()

    textLabel(m, 'Algorithm',   'MDP Value Iteration')
    textLabel(m, 'Mode',        'weighted' if weighted else 'unweighted')
    textLabel(m, 'Maze Size',   f'{size} x {size}')
    textLabel(m, 'Iterations',  stats['iterations'])
    textLabel(m, 'Path Length', len(path))
    if cost is not None:
        textLabel(m, 'Path Cost', cost)
    textLabel(m, 'Gamma',       GAMMA)
    textLabel(m, 'Noise',       NOISE)

    m.tracePath({a: path}, delay=100)
    m.run()


if __name__ == '__main__':
    main()
