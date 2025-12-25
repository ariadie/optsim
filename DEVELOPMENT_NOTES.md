# Development Notes

This document captures design decisions, architectural considerations, and development rationale that informed the evolution of the OptSim framework.

---

## Project Philosophy

**Goal**: Create a modular, educational optimization framework that demonstrates multiple algorithmic approaches while maintaining clean OOP principles.

**Target Audience**: Students, researchers, and developers learning about optimization algorithms.

---

## Architectural Decisions

### 1. Object-Oriented Design (v0.1.0)

**Decision**: Use four core classes: `Problem`, `Solver`, `Logger`, and `Visualizer`.

**Rationale**:
- **Separation of Concerns**: Each class has a single, well-defined responsibility.
- **Extensibility**: New problems and solvers can be added without modifying existing code.
- **Testability**: Individual components can be tested in isolation.

**Trade-offs**:
- More boilerplate compared to procedural approach.
- Slight performance overhead (negligible for educational purposes).

---

### 2. Problem Abstraction Layer (v0.5.0)

**Decision**: Create abstract `Problem` base class with required methods: `create_individual()`, `evaluate()`, `mutate()`, `crossover()`.

**Rationale**:
- **Algorithm-Problem Decoupling**: Solvers don't need to know problem-specific details.
- **Consistency**: All problems implement the same interface.
- **Flexibility**: Different problems can use different representations (binary, permutation, real-valued).

**Implementation Notes**:
- Initially had `Problem` in single file with `OneMaxProblem`.
- Refactored to `problems/` package when adding Knapsack (v0.5.0).
- Each problem encapsulates its own genetic operators (mutation/crossover) since optimal strategies vary by problem type.

---

### 3. Multi-Solver Architecture (v0.4.0)

**Decision**: Support multiple optimization algorithms (GA, RL, SA) through a unified CLI.

**Rationale**:
- **Educational Value**: Users can compare different approaches on the same problem.
- **Real-world Relevance**: Different problems favor different algorithms.

**Solver Characteristics**:

| Solver | Best For | Scalability | Exploration/Exploitation |
|--------|----------|-------------|--------------------------|
| **GA** | General-purpose, large search spaces | Excellent (pop-based) | Balanced (tunable) |
| **RL** | Sequential decision problems | Poor (state explosion) | High exploration early |
| **SA** | Continuous/local search | Good (single-solution) | High exploration → exploitation |

**Implementation Notes**:
- RL limited to small problems (≤12 bits) due to tabular Q-learning's $O(2^N)$ state space.
- SA uses exponential cooling schedule: `T = T * cooling_rate`.
- GA uses tournament selection (size=3) for balance between selection pressure and diversity.

---

### 4. Logging Strategy (v0.2.0 → v0.6.0)

**Evolution**:
1. **v0.2.0**: Basic generation-level statistics (best/avg fitness).
2. **v0.6.0**: Added population snapshots for diversity analysis.

**Decision**: Store entire population in history (not just statistics).

**Rationale**:
- Enables post-hoc analysis (heatmaps, diversity metrics).
- Memory cost is acceptable for educational use cases (typically <100 generations, <100 individuals).

**Trade-offs**:
- **Pro**: Rich visualization capabilities.
- **Con**: CSV export becomes impractical (population data is nested). Solution: Exclude population from CSV, keep in-memory only.

**Implementation Detail**:
```python
# Logger stores population as list reference
self.logger.log(gen, best_fitness, avg_fitness, best_ind, population=self.population[:])
#                                                                                    ^^^ Copy to avoid mutation
```

---

### 5. Visualization Philosophy (v0.6.0)

**Decision**: Use Matplotlib over Pygame for visualization.

**Comparison**:

| Aspect | Matplotlib | Pygame |
|--------|------------|--------|
| **Use Case** | Post-processing analysis | Real-time interactive visualization |
| **Dependencies** | Already required | New heavy dependency |
| **Output** | Static publication-quality images | Live animated windows |
| **Headless Support** | Yes (servers, CI/CD) | No (requires display) |
| **Learning Curve** | Low (familiar to scientists) | Medium (game dev concepts) |

**Rationale**:
- Current architecture is "batch optimization → analysis" (not real-time).
- Matplotlib aligns with scientific computing ecosystem.
- Static plots are easier to share in reports/papers.

**Visualization Types**:

1. **Fitness Progression**: Standard convergence analysis.
2. **Population Heatmap**: Novel contribution showing gene-level convergence.
   - Inspired by phylogenetic heatmaps in bioinformatics.
   - Reveals premature convergence and diversity loss.
3. **Problem-Specific Charts**: Tailored insights (e.g., Knapsack item selection).
4. **Animated Evolution (v0.7.0)**: GIF showing best individual evolution over generations.
   - Uses `matplotlib.animation.FuncAnimation` with `PillowWriter`.
   - Visual design: colored squares (green=1, red=0), generation counter, fitness display, progress bar.
   - Educational value: Shows convergence pattern intuitively.

**Design Pattern**:
```python
# Visualizer methods are problem-agnostic where possible
visualizer.plot_fitness(history)  # Works for any problem

# Problem-specific methods accept problem instance
visualizer.plot_knapsack_solution(problem, solution)  # Accesses problem.items, problem.capacity
```

---

## Problem-Specific Design Notes

### OneMax Problem

**Representation**: Binary string (list of 0s and 1s).

**Fitness**: Sum of bits (trivial, but excellent for teaching).

**Why Include?**:
- Simplest possible optimization problem.
- Convergence is easy to verify (optimal = all 1s).
- Ideal for testing new solvers/visualizations.

**Genetic Operators**:
- **Mutation**: Bit-flip with probability `mutation_rate`.
- **Crossover**: Single-point crossover.

---

### Knapsack Problem (0/1)

**Representation**: Binary string (1 = item included, 0 = excluded).

**Fitness**: Sum of values if weight ≤ capacity, else 0 (hard constraint).

**Design Decision**: Use penalty approach (fitness = 0) rather than repair.

**Rationale**:
- **Simplicity**: No complex repair logic.
- **Exploration**: Allows GA to explore infeasible regions.
- **Trade-off**: May slow convergence if capacity is tight.

**Alternative Considered**: Repair operator that removes items until feasible.
- **Rejected**: Adds complexity; penalty approach works well in practice.

**Genetic Operators**:
- **Mutation**: Same as OneMax (bit-flip).
- **Crossover**: Single-point crossover (preserves item groupings).

**Random Instance Generation**:
```python
# Each item: weight and value in [1, 20]
# Capacity = size * 10 * 0.5 (tunable via capacity_ratio)
```
- Ensures feasible solutions exist.
- Capacity ratio of 0.5 creates moderately constrained problems.

---

## Solver Implementation Details

### Genetic Algorithm (GA)

**Selection**: Tournament selection (size=3).
- **Why not roulette wheel?** Tournament is simpler and avoids fitness scaling issues.
- **Why size=3?** Balance between selection pressure (size=2 too weak, size=5+ too strong).

**Elitism**: Always preserve best individual.
- Guarantees monotonic improvement in best fitness.

**Reproduction**:
1. Select two parents via tournament.
2. Apply crossover → two children.
3. Apply mutation to each child.
4. Repeat until population is full.

**Population Size**: Default 50.
- Small enough for fast iterations.
- Large enough to maintain diversity.

---

### Reinforcement Learning (Q-Learning)

**State Representation**: Tuple of current bit string.
- **Limitation**: $2^N$ states → only works for N ≤ 12.

**Action Space**: Flip bit at position $i$ (N actions).

**Reward**: Change in fitness after action.

**Why RL for OneMax?**:
- Educational demonstration of RL on discrete optimization.
- Shows RL's strength in sequential decision-making.

**Why Not for Knapsack?**:
- State space would need to include current weight → even larger state space.
- GA is more practical for this problem class.

---

### Simulated Annealing (SA)

**Temperature Schedule**: Exponential cooling.
```python
T = initial_temp * (cooling_rate ** iteration)
```

**Acceptance Probability**:
```python
if delta_fitness > 0:
    accept = True
else:
    accept = random.random() < exp(delta_fitness / T)
```

**Neighbor Generation**: Single bit-flip (same as mutation).

**Tuning Notes**:
- `initial_temp=100`: High enough to accept most moves initially.
- `cooling_rate=0.95`: Slow cooling for thorough exploration.
- `min_temp=0.01`: Effectively becomes greedy hill-climbing at end.

---

## Code Quality Practices

### Version Management

**Strategy**: Semantic versioning (MAJOR.MINOR.PATCH).
- **MAJOR**: Breaking API changes.
- **MINOR**: New features (backward compatible).
- **PATCH**: Bug fixes.

**File-Level Versions**: Each module has `__version__` in header.
- Helps track which files changed in each release.
- Bumped together for consistency (all files share project version).

### Documentation Standards

**Docstrings**: Google-style docstrings for all classes and public methods.

**File Headers**:
```python
"""Module Description"""

__version__ = "0.6.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-25"
```

**Markdown Files**:
- `README.md`: User-facing documentation (installation, usage, examples).
- `CHANGELOG.md`: Version history (what changed, when).
- `DEVELOPMENT_NOTES.md`: Design rationale and technical decisions (this file).

---

## Future Considerations

### Potential Enhancements

1. **Additional Solvers**:
   - **Particle Swarm Optimization (PSO)**: Requires continuous problem representation.
   - **Ant Colony Optimization (ACO)**: Good for TSP-like problems.
   - **Deep Q-Network (DQN)**: Scale RL to larger problems via function approximation.

2. **Additional Problems**:
   - **Traveling Salesman Problem (TSP)**: Permutation representation.
   - **Function Optimization**: Continuous domains (Rastrigin, Rosenbrock).
   - **Multi-Objective**: Pareto front visualization.

3. **Advanced Visualizations**:
   - ~~**Real-time Animation**: Pygame or Matplotlib `FuncAnimation`.~~ ✅ **Implemented in v0.7.0** (GIF animation)
   - **3D Fitness Landscapes**: For 2D continuous problems.
   - **Diversity Metrics**: Shannon entropy, Hamming distance distributions.
   - **Knapsack Animation**: Animated item selection with weight gauge.

4. **Performance Optimization**:
   - **Parallelization**: Evaluate population in parallel (multiprocessing).
   - **Numba/Cython**: JIT compilation for fitness functions.
   - **Sparse Logging**: Only log every Nth generation for long runs.

### Scalability Limits

**Current Bottlenecks**:
- Population storage in logger: $O(G \times P \times N)$ memory (G=generations, P=pop size, N=problem size).
- CSV export doesn't scale with large populations (excluded population data).

**Mitigation Strategies**:
- Add `--log-level` flag: `minimal` (stats only) vs. `full` (with population).
- Implement rolling window: Only keep last K generations in memory.

---

## Lessons Learned

### What Worked Well

1. **Abstract Problem Class**: Made adding Knapsack trivial.
2. **CLI Design**: `--solver` and `--problem` flags provide intuitive interface.
3. **Matplotlib Choice**: Generated publication-ready plots with minimal code.

### What Could Be Improved

1. **RL Scalability**: Tabular Q-learning is too limited. Should have started with function approximation.
2. **Logger CSV Export**: Population data breaks CSV format. Should use JSON or HDF5 for rich data.
3. **Hardcoded Parameters**: Mutation rate, population size, etc. should be CLI arguments.

### Design Patterns Applied

- **Strategy Pattern**: Interchangeable solvers.
- **Template Method**: Abstract `Problem` class defines algorithm structure.
- **Dependency Injection**: Solvers receive `Problem` and `Logger` instances.

---

## References & Inspiration

- **Genetic Algorithms**: Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization, and Machine Learning*.
- **Reinforcement Learning**: Sutton & Barto (2018). *Reinforcement Learning: An Introduction*.
- **Simulated Annealing**: Kirkpatrick et al. (1983). "Optimization by Simulated Annealing".

---

*Last Updated: 2025-12-25 (v0.7.0)*
