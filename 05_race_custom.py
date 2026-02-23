# ============================================================
#  05_race_custom.py  —  BFS vs DFS vs A* Race (Custom Size)
# ============================================================
#  HOW TO RUN:
#    pip install pyamaze        (first time only)
#    python 05_race_custom.py
#
#  Type ANY maze size you want. All 3 algorithms race on the
#  SAME maze at the SAME time — closest to a finish line wins!
#
#  COLOUR KEY:
#    Blue  → BFS  (guaranteed shortest path, explores level by level)
#    Red   → DFS  (dives deep, fast to find A path, not always shortest)
#    Green → A*   (smart — uses heuristic, usually wins the race!)
#
#  TIP: Try sizes like 5, 15, 30, 50, 75, 100 to see how
#       each algorithm scales with maze complexity.
# ============================================================

from pyamaze import maze, agent, COLOR, textLabel
from collections import deque
import heapq
import time


# ── Algorithm Implementations ────────────────────────────────

def BFS(m):
    """Breadth-First Search — guaranteed shortest path."""
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
    """Depth-First Search — explores deep, not guaranteed shortest."""
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
    """A* Search — heuristic-guided, finds shortest path efficiently."""
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
                    g_score[nb]   = tg
                    came_from[nb] = current
                    heapq.heappush(heap, (tg + manhattan(nb, goal), nb))

    path = {}
    cell = goal
    while cell != start:
        path[came_from[cell]] = cell
        cell = came_from[cell]
    return path, len(came_from)


# ── Helpers ──────────────────────────────────────────────────

def get_winner(bfs_e, dfs_e, astar_e):
    """Determine race winner by fewest cells explored."""
    scores = {'BFS': bfs_e, 'DFS': dfs_e, 'A*': astar_e}
    winner = min(scores, key=scores.get)
    return winner, scores[winner]


def print_banner(size):
    print("\n" + "🏁" * 22)
    print(f"     BFS  vs  DFS  vs  A*  RACE!   {size}x{size} Maze")
    print("🏁" * 22)


# ── Main ─────────────────────────────────────────────────────

def main():
    print("=" * 50)
    print("   BFS vs DFS vs A*  —  Custom Size Race")
    print("=" * 50)
    print("\nEnter any maze size to race on.")
    print("Recommended range: 5 to 100 (>100 may be slow)\n")

    while True:
        try:
            size = int(input("Enter maze size: ").strip())
            if size < 2:
                print("Minimum size is 2. Try again.")
                continue
            if size > 200:
                confirm = input(f"Size {size} is very large and may be slow. Continue? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            break
        except ValueError:
            print("Please enter a valid integer.")

    print_banner(size)
    print(f"\nGenerating {size}x{size} maze...")

    # ── Create maze ─────────────────────────────────────────
    m = maze(size, size)
    m.CreateMaze(looped=False)

    # ── Run all algorithms ───────────────────────────────────
    print("Running all 3 algorithms on the same maze...\n")

    t0 = time.perf_counter(); bfs_path,   bfs_explored   = BFS(m);   bfs_time   = time.perf_counter() - t0
    t0 = time.perf_counter(); dfs_path,   dfs_explored   = DFS(m);   dfs_time   = time.perf_counter() - t0
    t0 = time.perf_counter(); astar_path, astar_explored = AStar(m); astar_time = time.perf_counter() - t0

    # ── Console race results ─────────────────────────────────
    winner, winner_explored = get_winner(bfs_explored, dfs_explored, astar_explored)

    print(f"{'Algorithm':<12} {'Path':>8} {'Explored':>10} {'Time (ms)':>12}  {'':>6}")
    print("-" * 55)
    for name, path, explored, t in [
        ('BFS',  bfs_path,   bfs_explored,   bfs_time),
        ('DFS',  dfs_path,   dfs_explored,   dfs_time),
        ('A*',   astar_path, astar_explored, astar_time),
    ]:
        trophy = '🏆 WINNER' if name == winner else ''
        print(f"{name:<12} {len(path):>8} {explored:>10} {t*1000:>11.2f}   {trophy}")

    print("-" * 55)
    print(f"\n🏆 {winner} wins! (fewest cells explored: {winner_explored})")
    print("\nOpening maze window... watch them race!\n")

    # ── Agents ──────────────────────────────────────────────
    bfs_agent   = agent(m, footprints=True, shape='arrow', color=COLOR.blue,  filled=True)
    dfs_agent   = agent(m, footprints=True, shape='arrow', color=COLOR.red,   filled=True)
    astar_agent = agent(m, footprints=True, shape='arrow', color=COLOR.green, filled=True)

    # ── Labels ──────────────────────────────────────────────
    textLabel(m, 'Maze Size',              f'{size} x {size}')
    textLabel(m, 'BFS  — path / explored', f'{len(bfs_path)} / {bfs_explored}')
    textLabel(m, 'DFS  — path / explored', f'{len(dfs_path)} / {dfs_explored}')
    textLabel(m, 'A*   — path / explored', f'{len(astar_path)} / {astar_explored}')
    textLabel(m, 'Winner',                 f'{winner}  (explored fewest cells)')
    textLabel(m, 'Colour Key',             'Blue=BFS  Red=DFS  Green=A*')

    # ── Race! ────────────────────────────────────────────────
    # All 3 agents move simultaneously — the visual race!
    delay = max(50, min(200, 2000 // size))   # auto-scale delay by maze size
    m.tracePath(
        {bfs_agent: bfs_path, dfs_agent: dfs_path, astar_agent: astar_path},
        delay=delay
    )

    m.run()


if __name__ == '__main__':
    main()
