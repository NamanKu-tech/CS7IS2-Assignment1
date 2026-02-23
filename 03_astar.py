# ============================================================
#  03_astar.py  —  A* Search on a pyamaze Maze
# ============================================================
#  HOW TO RUN:
#    pip install pyamaze        (first time only)
#    python 03_astar.py
#
#  A* uses a heuristic (Manhattan distance) to guide its search
#  intelligently toward the goal. It finds the SHORTEST path
#  like BFS but explores FAR fewer cells — much more efficient!
# ============================================================

from pyamaze import maze, agent, COLOR, textLabel
import heapq


def manhattan(cell, goal):
    """Manhattan distance heuristic — works perfectly for grid mazes."""
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def AStar(m):
    """
    A* Search on a pyamaze maze.
    Returns:
        path          : dict {cell -> next_cell} for tracePath (start → goal)
        search_path   : dict showing A* exploration footprint
        cells_explored: total cells A* visited before finding goal
    """
    start = (m.rows, m.cols)   # bottom-right
    goal  = (1, 1)             # top-left

    # Priority queue: (f_score, cell)
    open_set = []
    heapq.heappush(open_set, (0 + manhattan(start, goal), start))

    came_from = {start: None}    # cell -> parent
    g_score   = {start: 0}      # cost from start to cell

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            break

        for direction in 'ESNW':
            if m.maze_map[current][direction]:
                r, c = current
                if   direction == 'E': neighbour = (r,     c + 1)
                elif direction == 'W': neighbour = (r,     c - 1)
                elif direction == 'N': neighbour = (r - 1, c    )
                elif direction == 'S': neighbour = (r + 1, c    )

                tentative_g = g_score[current] + 1  # all edges cost 1

                if neighbour not in g_score or tentative_g < g_score[neighbour]:
                    g_score[neighbour]  = tentative_g
                    f_score             = tentative_g + manhattan(neighbour, goal)
                    came_from[neighbour] = current
                    heapq.heappush(open_set, (f_score, neighbour))

    # Reconstruct final path (start → goal)
    path = {}
    cell = goal
    while cell != start:
        path[came_from[cell]] = cell
        cell = came_from[cell]

    # Build exploration footprint
    search_path = {}
    for cell, parent in came_from.items():
        if parent is not None:
            search_path[parent] = cell

    return path, search_path, len(came_from)


def main():
    print("=" * 45)
    print("   A* Maze Solver  —  pyamaze")
    print("=" * 45)

    try:
        size = int(input("Enter maze size (e.g. 10, 15, 20): ").strip())
        if size < 2:
            raise ValueError
    except ValueError:
        print("Invalid input. Using default size 10.")
        size = 10

    print(f"\nGenerating {size}x{size} maze and solving with A*...")

    # Create and generate maze
    m = maze(size, size)
    m.CreateMaze(looped=False)

    # Run A*
    path, search_path, cells_explored = AStar(m)

    # ── Agents ──────────────────────────────────────────────
    # Agent 1: shows cells A* explored — notice how focused it is!
    explorer = agent(
        m,
        footprints=True,
        shape='square',
        color=COLOR.cyan,
        filled=False
    )

    # Agent 2: draws the final shortest path
    solver = agent(
        m,
        footprints=True,
        shape='arrow',
        color=COLOR.green,
        filled=True
    )

    # ── Labels ──────────────────────────────────────────────
    textLabel(m, 'Algorithm',       'A* (Manhattan heuristic)')
    textLabel(m, 'Maze Size',       f'{size} x {size}')
    textLabel(m, 'Cells Explored',  cells_explored)
    textLabel(m, 'Shortest Path Length', len(path))

    # ── Animate ─────────────────────────────────────────────
    m.tracePath(
        {explorer: search_path, solver: path},
        delay=100
    )

    m.run()


if __name__ == '__main__':
    main()
