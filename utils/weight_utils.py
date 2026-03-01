import random


class WeightedMaze:
    """
    Wraps a pyamaze maze with cell weights (1–9).
    Handles weight generation, drawing, cost calculation.
    """

    def __init__(self, m, seed=42):
        self.m       = m
        self.start   = (m.rows, m.cols)
        self.weights = self._generate(seed)

    def _generate(self, seed):
        """Assign random cost 1–9 to each cell (deterministic with seed)."""
        rng = random.Random(seed)
        return {cell: rng.randint(1, 9) for cell in self.m.maze_map}

    def draw(self):
        """Show small grey weight numbers in each cell."""
        m   = self.m
        w   = m._cell_width
        lab = m._LabWidth
        font_size = max(6, int(w * 0.3))
        for cell, cost in self.weights.items():
            cx, cy = cell
            x = cx * w - w + lab
            y = cy * w - w + lab
            m._canvas.create_text(y + w/2, x + w/2, text=str(cost),
                                  fill='gray70',
                                  font=('Helvetica', font_size),
                                  tag='weighttxt')
        m._canvas.tag_raise('weighttxt')

    def keep_text_on_top(self):
        """Periodically raise weight text above agent footprints."""
        try:
            self.m._canvas.tag_raise('weighttxt')
            self.m._win.after(50, self.keep_text_on_top)
        except Exception:
            pass

    def path_cost(self, path):
        """Sum weights along the path (including start cell)."""
        total = self.weights[self.start]
        cell  = self.start
        while cell in path:
            cell   = path[cell]
            total += self.weights[cell]
        return total

    def path_cells_list(self, path):
        """Return ordered list of cells in the path."""
        cells = [self.start]
        cell  = self.start
        while cell in path:
            cell = path[cell]
            cells.append(cell)
        return cells
