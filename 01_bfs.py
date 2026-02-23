# ============================================================
#  01_bfs.py  —  Breadth-First Search on a pyamaze Maze
# ============================================================
#  HOW TO RUN:
#    pip install pyamaze        (first time only)
#    python 01_bfs.py
#
#  BFS guarantees the SHORTEST path from start (bottom-right)
#  to goal (top-left corner).
# ============================================================

from pyamaze import maze, agent, COLOR, textLabel
from collections import deque


def BFS(m):
    """
    Breadth-First Search on a pyamaze maze.
    Returns:
        path        : dict {cell -> next_cell} for tracePath (start → goal)
        visited_order: list of cells in the order BFS explored them
        search_path : dict {cell -> came_from} for showing exploration footprint
    """
    start = (m.rows, m.cols)   # bottom-right
    goal  = (1, 1)             # top-left

    frontier = deque([start])
    came_from = {start: None}  # cell -> parent

    while frontier:
        current = frontier.popleft()

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
                    frontier.append(neighbour)

    # Reconstruct the final path (start → goal) for tracePath
    path = {}
    cell = goal
    while cell != start:
        path[came_from[cell]] = cell
        cell = came_from[cell]

    # Build exploration footprint for visualisation (shows cells BFS visited)
    search_path = {}
    for cell, parent in came_from.items():
        if parent is not None:
            search_path[parent] = cell

    return path, search_path, len(came_from)


def main():
    print("=" * 45)
    print("   BFS Maze Solver  —  pyamaze")
    print("=" * 45)

    try:
        size = int(input("Enter maze size (e.g. 10, 15, 20): ").strip())
        if size < 2:
            raise ValueError
    except ValueError:
        print("Invalid input. Using default size 10.")
        size = 10

    print(f"\nGenerating {size}x{size} maze and solving with BFS...")

    # Create and generate maze
    m = maze(size, size)
    m.CreateMaze(looped=False)   # perfect maze — exactly one solution

    # Run BFS
    path, search_path, cells_explored = BFS(m)

    # ── Agents ──────────────────────────────────────────────
    # Agent 1: shows the cells BFS explored (light footprint)
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
        color=COLOR.blue,
        filled=True
    )

    # ── Labels ──────────────────────────────────────────────
    textLabel(m, 'Algorithm',       'BFS (Breadth-First Search)')
    textLabel(m, 'Maze Size',       f'{size} x {size}')
    textLabel(m, 'Cells Explored',  cells_explored)
    textLabel(m, 'Shortest Path Length', len(path))

    # ── Animate ─────────────────────────────────────────────
    # Show exploration first (slower), then the final path (faster)
    m.tracePath(
        {explorer: search_path, solver: path},
        delay=100
    )

    m.run()


if __name__ == '__main__':
    main()
