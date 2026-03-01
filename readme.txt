CS7IS2 Assignment 1 - Maze Solver AI
Naman Kumar | 25340053 | Trinity College Dublin

============================================
SETUP
============================================

    python3 -m venv venv
    source venv/bin/activate        # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

Only dependency is pyamaze.

============================================
RUNNING EACH ALGORITHM
============================================

Each script prompts for maze size and unweighted/weighted mode,
then opens a pyamaze window animating the solved path.

BFS (Breadth-First Search):
    python demos/01_bfs.py

DFS (Depth-First Search):
    python demos/02_dfs.py

A* with Manhattan heuristic:
    python demos/03_astar_manhattan.py

A* with Euclidean heuristic:
    python demos/04_astar_euclidean.py

MDP Value Iteration:
    python demos/05_mdp_value_iteration.py

MDP Policy Iteration:
    python demos/06_mdp_policy_iteration.py

To save results to temp/results.csv, add --save:
    python demos/01_bfs.py --save

Batch-run all algorithms (unweighted) across all maze sizes:

    for demo in demos/0*.py; do
        for size in 5 10 15 25 50 100; do
            printf "u\n%s\n" "$size" | python "$demo" --save
        done
    done

Batch-run weighted benchmarks (search algorithms only):

    for demo in demos/01_bfs.py demos/02_dfs.py demos/03_astar_manhattan.py demos/04_astar_euclidean.py; do
        for size in 5 10 15 25 50 100; do
            printf "w\n%s\n" "$size" | python "$demo" --save
        done
    done

============================================
PROJECT STRUCTURE
============================================

solvers/
    base.py          - Solver base class (neighbour lookup, path reconstruction)
    bfs.py           - Breadth-First Search
    dfs.py           - Depth-First Search
    astar.py         - A* Search (Manhattan / Euclidean / Weighted A*)
    mdp.py           - Value Iteration + Policy Iteration

utils/
    maze_utils.py    - Maze generation, heuristics, CSV stat logging
    weight_utils.py  - Weighted maze wrapper (random cell costs 1-9)

demos/
    01_bfs.py through 06_mdp_policy_iteration.py - Visual demo scripts

docs/
    report_final.tex                    - LaTeX report source
    ai_assignment_final_report.pdf      - Compiled report (PDF)

temp/
    results.csv                         - Benchmark results
    maze_*.csv                          - Saved maze layouts

============================================
NOTES
============================================

- Mazes are generated with pyamaze (loopPercent=50) and saved to temp/
  so all algorithms run on the same maze for fair comparison.
- Start: bottom-right (N,N). Goal: top-left (1,1).
- MDP parameters: gamma=0.9, noise=0.2, living_reward=-0.04.
- Code runs on any maze size (not hardcoded).
