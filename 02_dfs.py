# ============================================================
#  02_dfs.py  —  Depth-First Search on a pyamaze Maze
# ============================================================
#  HOW TO RUN:
#    pip install pyamaze        (first time only)
#    python 02_dfs.py
#
#  DFS does NOT guarantee the shortest path — it dives deep
#  and backtracks. You'll see it explore many dead ends!
# ============================================================

from pyamaze import maze, agent, COLOR, textLabel


def DFS(m):
    """
    Depth-First Search on a pyamaze maze.
    Returns:
        path        : dict {cell -> next_cell} for tracePath (start → goal)
        search_path : dict showing DFS exploration footprint
        cells_explored: total cells DFS visited before finding goal
    """
    start = (m.rows, m.cols)   # bottom-right
    goal  = (1, 1)             # top-left

    stack = [start]
    came_from = {start: None}  # cell -> parent

    while stack:
        current = stack.pop()   # LIFO — this is what makes it DFS

        if current == goal:
            break

        # Explore neighbours in all 4 directions
        for direction in 'ESNW':
            if m.maze_map[current][direction]:
                r, c = current
                if   direction == 'E': neighbour = (r,     c + 1)
                elif direction == 'W': neighbour = (r,     c - 1)
                elif direction == 'N': neighbour = (r - 1, c    )
                elif direction == 'S': neighbour = (r + 1, c    )

                if neighbour not in came_from:
                    came_from[neighbour] = current
                    stack.append(neighbour)

    # Reconstruct the path DFS found (start → goal)
    path = {}
    cell = goal
    while cell != start:
        path[came_from[cell]] = cell
        cell = came_from[cell]

    # Build exploration footprint for visualisation
    search_path = {}
    for cell, parent in came_from.items():
        if parent is not None:
            search_path[parent] = cell

    return path, search_path, len(came_from)


def main():
    print("=" * 45)
    print("   DFS Maze Solver  —  pyamaze")
    print("=" * 45)

    try:
        size = int(input("Enter maze size (e.g. 10, 15, 20): ").strip())
        if size < 2:
            raise ValueError
    except ValueError:
        print("Invalid input. Using default size 10.")
        size = 10

    print(f"\nGenerating {size}x{size} maze and solving with DFS...")

    # Create and generate maze
    m = maze(size, size)
    m.CreateMaze(looped=False)

    # Run DFS
    path, search_path, cells_explored = DFS(m)

    # ── Agents ──────────────────────────────────────────────
    # Agent 1: shows all cells DFS explored (orange — shows the chaos!)
    explorer = agent(
        m,
        footprints=True,
        shape='square',
        color=COLOR.yellow,
        filled=False
    )

    # Agent 2: draws the path DFS found (not necessarily shortest)
    solver = agent(
        m,
        footprints=True,
        shape='arrow',
        color=COLOR.red,
        filled=True
    )

    # ── Labels ──────────────────────────────────────────────
    textLabel(m, 'Algorithm',      'DFS (Depth-First Search)')
    textLabel(m, 'Maze Size',      f'{size} x {size}')
    textLabel(m, 'Cells Explored', cells_explored)
    textLabel(m, 'Path Length (not guaranteed shortest)', len(path))

    # ── Animate ─────────────────────────────────────────────
    m.tracePath(
        {explorer: search_path, solver: path},
        delay=100
    )

    m.run()


if __name__ == '__main__':
    main()
