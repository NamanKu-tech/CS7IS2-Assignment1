# ============================================================
#  04_race_sizes.py  —  BFS vs DFS vs A* Race on Preset Sizes
# ============================================================
#  HOW TO RUN:
#    pip install pyamaze        (first time only)
#    python 04_race_sizes.py
#
#  Choose from preset maze sizes: 10, 20, 25, 100
#  All 3 algorithms race simultaneously on the SAME maze.
#  Watch how they explore differently and compare stats!
#
#  COLOUR KEY:
#    Blue  agent  → BFS  (shortest path guaranteed)
#    Red   agent  → DFS  (goes deep, may not be shortest)
#    Green agent  → A*   (guided by heuristic, very efficient)
# ============================================================

from pyamaze import maze, agent, COLOR, textLabel
from collections import deque
import heapq
import time


# ── Algorithm Implementations ────────────────────────────────

def BFS(m):
    start = (m.rows, m.cols)
    goal  = (1, 1)
    frontier  = deque([start])
    came_from = {start: None}

    while frontier:
        current = frontier.popleft()
        if current == goal:
            break
        for d in 'ESNW':
            if m.maze_map[current][d]:
                r, c = current
                nb = (r-1,c) if d=='N' else (r+1,c) if d=='S' else (r,c+1) if d=='E' else (r,c-1)
                if nb not in came_from:
                    came_from[nb] = current
                    frontier.append(nb)

    path = {}
    cell = goal
    while cell != start:
        path[came_from[cell]] = cell
        cell = came_from[cell]
    return path, len(came_from)


def DFS(m):
    start = (m.rows, m.cols)
    goal  = (1, 1)
    stack     = [start]
    came_from = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            break
        for d in 'ESNW':
            if m.maze_map[current][d]:
                r, c = current
                nb = (r-1,c) if d=='N' else (r+1,c) if d=='S' else (r,c+1) if d=='E' else (r,c-1)
                if nb not in came_from:
                    came_from[nb] = current
                    stack.append(nb)

    path = {}
    cell = goal
    while cell != start:
        path[came_from[cell]] = cell
        cell = came_from[cell]
    return path, len(came_from)


def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def AStar(m):
    start = (m.rows, m.cols)
    goal  = (1, 1)
    heap      = [(manhattan(start, goal), start)]
    came_from = {start: None}
    g_score   = {start: 0}

    while heap:
        _, current = heapq.heappop(heap)
        if current == goal:
            break
        for d in 'ESNW':
            if m.maze_map[current][d]:
                r, c = current
                nb = (r-1,c) if d=='N' else (r+1,c) if d=='S' else (r,c+1) if d=='E' else (r,c-1)
                tg = g_score[current] + 1
                if nb not in g_score or tg < g_score[nb]:
                    g_score[nb]  = tg
                    came_from[nb] = current
                    heapq.heappush(heap, (tg + manhattan(nb, goal), nb))

    path = {}
    cell = goal
    while cell != start:
        path[came_from[cell]] = cell
        cell = came_from[cell]
    return path, len(came_from)


# ── Main ─────────────────────────────────────────────────────

PRESET_SIZES = [10, 20, 25, 100]

def main():
    print("=" * 50)
    print("   BFS vs DFS vs A*  —  Preset Size Race")
    print("=" * 50)
    print("\nAvailable maze sizes:")
    for i, s in enumerate(PRESET_SIZES, 1):
        print(f"  [{i}]  {s} x {s}")

    try:
        choice = int(input("\nChoose a size (1–4): ").strip())
        if choice not in range(1, 5):
            raise ValueError
        size = PRESET_SIZES[choice - 1]
    except ValueError:
        print("Invalid choice. Using 10 x 10.")
        size = 10

    print(f"\nGenerating {size}x{size} maze...")
    print("Running BFS, DFS, and A* simultaneously...")

    if size >= 100:
        print("(Large maze — this may take a moment to generate!)")

    # ── Create maze ─────────────────────────────────────────
    m = maze(size, size)
    m.CreateMaze(looped=False)

    # ── Run all algorithms & time them ──────────────────────
    t0 = time.perf_counter(); bfs_path, bfs_explored = BFS(m);   bfs_time  = time.perf_counter() - t0
    t0 = time.perf_counter(); dfs_path, dfs_explored = DFS(m);   dfs_time  = time.perf_counter() - t0
    t0 = time.perf_counter(); astar_path, ast_explored = AStar(m); astar_time = time.perf_counter() - t0

    # ── Console summary ─────────────────────────────────────
    print("\n" + "=" * 50)
    print(f"{'Algorithm':<12} {'Path Len':>10} {'Explored':>10} {'Time (ms)':>12}")
    print("-" * 50)
    print(f"{'BFS':<12} {len(bfs_path):>10} {bfs_explored:>10} {bfs_time*1000:>11.2f}")
    print(f"{'DFS':<12} {len(dfs_path):>10} {dfs_explored:>10} {dfs_time*1000:>11.2f}")
    print(f"{'A*':<12} {len(astar_path):>10} {ast_explored:>10} {astar_time*1000:>11.2f}")
    print("=" * 50)

    # ── Agents (colour-coded) ────────────────────────────────
    bfs_agent   = agent(m, footprints=True, shape='arrow', color=COLOR.blue,  filled=True)
    dfs_agent   = agent(m, footprints=True, shape='arrow', color=COLOR.red,   filled=True)
    astar_agent = agent(m, footprints=True, shape='arrow', color=COLOR.green, filled=True)

    # ── Labels ──────────────────────────────────────────────
    textLabel(m, 'Maze Size',              f'{size} x {size}')
    textLabel(m, 'BFS  — path / explored', f'{len(bfs_path)} / {bfs_explored}')
    textLabel(m, 'DFS  — path / explored', f'{len(dfs_path)} / {dfs_explored}')
    textLabel(m, 'A*   — path / explored', f'{len(astar_path)} / {ast_explored}')
    textLabel(m, 'Colour Key',             'Blue=BFS  Red=DFS  Green=A*')

    # ── Race! ────────────────────────────────────────────────
    m.tracePath(
        {bfs_agent: bfs_path, dfs_agent: dfs_path, astar_agent: astar_path},
        delay=150
    )

    m.run()


if __name__ == '__main__':
    main()
