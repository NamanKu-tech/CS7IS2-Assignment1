# Maze Solver AI

CS7IS2 Artificial Intelligence — Assignment 1, Trinity College Dublin (2025–2026)

Compares classical search algorithms against Markov Decision Process solvers on randomly generated mazes from 5×5 to 100×100.

## Quick Start

```bash
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python demos/01_bfs.py
```

Each demo asks for a maze size and whether to run in unweighted or weighted mode, then opens a pyamaze window that animates the solver's path.

## Project Structure

```
assignment_1/
├── solvers/
│   ├── base.py            # Solver base class (neighbour lookup, path reconstruction)
│   ├── bfs.py             # Breadth-First Search
│   ├── dfs.py             # Depth-First Search
│   ├── astar.py           # A* Search (Manhattan / Euclidean / Weighted A*)
│   └── mdp.py             # Value Iteration + Policy Iteration
├── utils/
│   ├── maze_utils.py      # Maze generation, heuristics, CSV stat logging
│   └── weight_utils.py    # Weighted maze wrapper (random cell costs 1–9)
├── demos/
│   ├── 01_bfs.py
│   ├── 02_dfs.py
│   ├── 03_astar_manhattan.py
│   ├── 04_astar_euclidean.py
│   ├── 05_mdp_value_iteration.py
│   └── 06_mdp_policy_iteration.py
├── docs/
│   ├── report_final.tex                          # LaTeX report source
│   ├── ai_assignment_final_report.pdf            # Compiled report
│   ├── CS7IS2-Search-MDP-Report-Assignment1.pdf  # Submitted report
│   ├── video_script.md                           # Script for the code walkthrough video
│   ├── Screen Recording 2026-03-01 at 22.34.48.mov  # Demo recording
│   └── Assignment 1 2025-2026.pdf                # Assignment brief
├── temp/                  # Generated mazes (CSV) and benchmark results
└── requirements.txt
```

## Algorithms

All solvers inherit from `solvers/base.py`, which provides neighbour lookup via the maze's wall map and a shared `reconstruct_path` method that builds the `{parent: child}` dict pyamaze expects.

**Search algorithms** find a single start-to-goal path:

| Algorithm | File | Strategy | Optimal? |
|---|---|---|---|
| BFS | `bfs.py` | FIFO deque, expands layer by layer | Yes (step-optimal) |
| DFS | `dfs.py` | LIFO stack, dives deep then backtracks | No |
| A* (Manhattan) | `astar.py` | Min-heap on f = g + h, Manhattan heuristic | Yes |
| A* (Euclidean) | `astar.py` | Min-heap on f = g + h, Euclidean heuristic | Yes |
| Weighted A* | `astar.py` | Same as A* but g accumulates cell weights | Yes (cost-optimal) |

**MDP solvers** compute a policy for every cell in the maze:

| Algorithm | Class | Method |
|---|---|---|
| Value Iteration | `MDPSolver` | Bellman updates until convergence (max 500 iters, θ = 10⁻⁶) |
| Policy Iteration | `MDPPolicyIterationSolver` | Alternates policy evaluation (up to 200 inner sweeps) and greedy improvement |

Both use γ = 0.9, noise = 0.2 (80% intended direction, 10% each perpendicular), living reward = −0.04.

## How the Maze Works

Mazes are generated with `pyamaze`'s `CreateMaze(loopPercent=50)`. The maze is stored as a dictionary `maze_map[(row, col)][direction]` where 1 = open passage and 0 = wall. Setting `loopPercent=50` removes half the internal walls from the default perfect maze, creating cycles and multiple paths so different algorithms can find genuinely different routes.

Once generated, a maze is saved to `temp/maze_{size}.csv` and reused on subsequent runs, so all algorithms solve the exact same maze for fair comparison.

The start is always the bottom-right corner (N, N) and the goal is the top-left (1, 1).

## Running the Demos

Each demo script in `demos/` is standalone:

```bash
python demos/01_bfs.py              
python demos/03_astar_manhattan.py  
python demos/05_mdp_value_iteration.py
```

All demos accept `--save` to append results to `temp/results.csv`:

```bash
python demos/01_bfs.py --save
```

You'll be prompted for maze size and unweighted/weighted mode. The pyamaze window then animates the agent following the solved path, with stats displayed as text labels.

To batch-run all algorithms across all sizes and save results (unweighted):

```bash
for demo in demos/0*.py; do
    for size in 5 10 15 25 50 100; do
        printf "u\n%s\n" "$size" | python "$demo" --save
    done
done
```

To batch-run weighted benchmarks (search algorithms only):

```bash
for demo in demos/01_bfs.py demos/02_dfs.py demos/03_astar_manhattan.py demos/04_astar_euclidean.py; do
    for size in 5 10 15 25 50 100; do
        printf "w\n%s\n" "$size" | python "$demo" --save
    done
done
```

## Key Files Explained

**`solvers/base.py`** — The `Solver` class every algorithm extends. `neighbours(cell)` checks which walls are open and returns reachable adjacent cells. `reconstruct_path(came_from)` backtracks from goal to start using the parent pointers.

**`solvers/bfs.py`** — Pops from a deque (FIFO). First time the goal is popped, that's the shortest path. Tracks `cells_explored` count.

**`solvers/dfs.py`** — Pops from a list (LIFO stack). Uses a `closed` set to skip already-expanded nodes. Finds a path fast but it won't be shortest.

**`solvers/astar.py`** — Uses Python's `heapq` as a priority queue sorted by f = g + h. The `weights` parameter switches between unit-cost A* and Weighted A* (g accumulates cell weights instead of 1 per step).

**`solvers/mdp.py`** — Two classes. `MDPSolver` (Value Iteration) sweeps all N² cells per iteration, computing Q(s,a) = R(s) + γ Σ P(s'|s,a)V(s') for each action. `_transition_probs` implements the stochastic model. `_extract_path` follows the converged policy from start to goal with a wall-collision fallback. `MDPPolicyIterationSolver` inherits from it and adds `_evaluate_policy` for the inner evaluation loop.

**`utils/maze_utils.py`** — `DIRECTION_MAP` maps N/S/E/W to (row, col) deltas. `get_or_create_maze` generates or loads a maze. `manhattan` and `euclidean` are the heuristic functions. `save_stats` logs results to CSV.

**`utils/weight_utils.py`** — `WeightedMaze` assigns random costs 1–9 to each cell (seeded for reproducibility). `path_cost` sums weights along a solved path.

## Documentation

| Document | Description |
|---|---|
| `docs/ai_assignment_final_report.pdf` | Final compiled report with all benchmarks, charts, and analysis |
| `docs/Screen Recording 2026-03-01 at 22.34.48.mov` | Screen recording of the demo |
| `docs/Assignment 1 2025-2026.pdf` | Original assignment brief |
