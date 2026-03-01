from .base import Solver

PERPENDICULAR = {
    'N': ['E', 'W'],
    'S': ['E', 'W'],
    'E': ['N', 'S'],
    'W': ['N', 'S'],
}

ACTIONS = ['N', 'S', 'E', 'W']


class MDPSolver(Solver):
    """
    MDP Value Iteration.

    Repeatedly sweeps all cells applying the Bellman update:
        V(s) = max_a [ R(s) + γ Σ P(s'|s,a) V(s') ]
    until the value function changes by less than theta.
    """

    def __init__(self, m, gamma=0.9, noise=0.2, living_reward=-0.04,
                 theta=1e-6, max_iters=500):
        super().__init__(m)
        self.gamma         = gamma
        self.noise         = noise
        self.living_reward = living_reward
        self.theta         = theta
        self.max_iters     = max_iters

    def _transition_probs(self, cell, action):
        """
        Stochastic transition model.
        P(intended direction) = 1 - noise
        P(each perpendicular) = noise / 2
        Walls → agent stays in place.
        """
        nb = self.neighbours_dict(cell)
        outcomes = {}

        intended = nb.get(action, cell)
        outcomes[intended] = outcomes.get(intended, 0) + (1 - self.noise)

        for perp in PERPENDICULAR[action]:
            slip = nb.get(perp, cell)
            outcomes[slip] = outcomes.get(slip, 0) + self.noise / 2

        return outcomes

    def _reward(self, cell):
        """Living reward per step."""
        return self.living_reward

    def _q_value(self, cell, action, V):
        """Q(s, a) = R(s) + γ Σ P(s'|s,a) V(s')"""
        q = self._reward(cell)
        for next_cell, prob in self._transition_probs(cell, action).items():
            q += prob * self.gamma * V[next_cell]
        return q

    def _best_action(self, cell, V):
        """Return (best_q_value, best_action) for a cell given V."""
        best_val = float('-inf')
        best_a   = None
        for a in ACTIONS:
            q = self._q_value(cell, a, V)
            if q > best_val:
                best_val = q
                best_a   = a
        return best_val, best_a

    def _extract_path(self, policy, V=None):
        """Follow the policy deterministically from start to goal."""
        path    = {}
        cell    = self.start
        visited = set()
        while cell != self.goal and cell not in visited:
            visited.add(cell)
            a = policy[cell]
            if a is None:
                break
            nb        = self.neighbours_dict(cell)
            next_cell = nb.get(a, cell)
            if next_cell == cell and V is not None:
                ranked = sorted(ACTIONS,
                                key=lambda act: self._q_value(cell, act, V),
                                reverse=True)
                for alt in ranked:
                    cand = nb.get(alt, cell)
                    if cand != cell:
                        next_cell = cand
                        break
            if next_cell == cell:
                break
            path[cell] = next_cell
            cell       = next_cell
        return path

    def solve(self):
        all_cells = list(self.m.maze_map.keys())

        V      = {c: 0.0 for c in all_cells}
        V[self.goal] = 1.0
        policy = {c: None for c in all_cells}

        iterations = 0
        for i in range(self.max_iters):
            delta = 0.0
            new_V = dict(V)

            for cell in all_cells:
                if cell == self.goal:
                    continue
                best_val, best_a    = self._best_action(cell, V)
                new_V[cell]         = best_val
                policy[cell]        = best_a
                delta = max(delta, abs(new_V[cell] - V[cell]))

            V = new_V
            iterations = i + 1
            if delta < self.theta:
                break

        path = self._extract_path(policy, V)
        return path, {
            'iterations':  iterations,
            'total_cells': len(all_cells),
            'V':           V,
        }


class MDPPolicyIterationSolver(MDPSolver):
    """
    MDP Policy Iteration.

    Alternates between:
      1. Policy Evaluation  — compute V for the current fixed policy
      2. Policy Improvement — greedily update each action using new V

    Stops when the policy doesn't change (policy_stable = True).
    """

    def __init__(self, m, gamma=0.9, noise=0.2, living_reward=-0.04,
                 theta=1e-6, max_eval_iters=200):
        super().__init__(m, gamma=gamma, noise=noise,
                         living_reward=living_reward, theta=theta)
        self.max_eval_iters = max_eval_iters

    def _evaluate_policy(self, policy, V):
        """
        Policy Evaluation step.
        Fix the policy and compute V(s) = R(s) + γ Σ P(s'|s,π(s)) V(s')
        until values converge.
        """
        all_cells = list(self.m.maze_map.keys())
        for _ in range(self.max_eval_iters):
            delta = 0.0
            new_V = dict(V)
            for cell in all_cells:
                if cell == self.goal:
                    continue
                a           = policy[cell]
                new_V[cell] = self._q_value(cell, a, V)
                delta = max(delta, abs(new_V[cell] - V[cell]))
            V = new_V
            if delta < self.theta:
                break
        return V

    def solve(self):
        all_cells = list(self.m.maze_map.keys())

        policy = {c: 'N' for c in all_cells}
        policy[self.goal] = None

        V = {c: 0.0 for c in all_cells}
        V[self.goal] = 1.0

        iterations = 0
        while True:
            V = self._evaluate_policy(policy, V)

            policy_stable = True
            for cell in all_cells:
                if cell == self.goal:
                    continue
                old_action      = policy[cell]
                _, best_a       = self._best_action(cell, V)
                policy[cell]    = best_a
                if best_a != old_action:
                    policy_stable = False

            iterations += 1
            if policy_stable:
                break

        path = self._extract_path(policy, V)
        return path, {
            'iterations':  iterations,
            'total_cells': len(all_cells),
            'V':           V,
        }
