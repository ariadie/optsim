# Changelog

All notable changes to this project will be documented in this file.


## [0.6.0] - 2025-12-25
### Added
- **Enhanced Visualization System**: Major upgrade to `visualizer.py` with three specialized plotting methods:
  - `plot_fitness()`: Standard fitness progression charts (renamed from `plot()`).
  - `plot_population_heatmap()`: Gene convergence visualization showing population diversity over generations.
  - `plot_knapsack_solution()`: Problem-specific bar charts for Knapsack item selection.
- Population data collection: `Logger` now captures population snapshots for diversity analysis.
- Updated `GASolver` to pass population data to logger.
- Updated `main.py` to generate multiple visualization types per run.

### Changed
- **Output Structure Reorganization**: All plots now saved to `logs/` directory (previously `plots/`).
- **Timestamped Filenames**: Plot filenames now include timestamps matching CSV log format (e.g., `ga_onemax_10_fitness_20251225_074411.png`).
- Bumped `visualizer.py` version to 0.6.0.
- Plot filenames now include visualization type suffix (e.g., `_fitness.png`, `_heatmap.png`).

## [0.5.0] - 2025-12-24
### Added
- Implemented **0/1 Knapsack Problem** (`problems/knapsack.py`) as a new optimization challenge.
- Added `--problem` argument to CLI to switch between `onemax` and `knapsack`.
- Refactored `problem.py` into a modular `problems/` package with `base.py` and `onemax.py`.

## [0.4.1] - 2025-12-24
### Changed
- Standardized file headers with docstrings, author, and version information.

## [0.4.0] - 2025-12-24
### Added
- Implemented Simulated Annealing (SA) solver.
- Refactored project structure: solvers moved to `solvers/` package.
- Added command line interface with `--solver` argument.

## [0.3.0] - 2025-12-24
### Added
- Implemented identifying and logging the best solution string for each generation.
- Added new Reinforcement Learning (Q-Learning) solver module: `rl_solver.py`, `rl_env.py`, `main_rl.py`.
- Added `README.md` with project documentation.
- Updated console output to show the best solution string.

## [0.2.0] - 2025-12-24
### Added
- Implemented log saving to `logs` directory with timestamped filenames.
- Added versioning system (`version.py` and `__version__` in files).
- Created `CHANGELOG.md`.

## [0.1.0] - 2025-12-24
### Added
- Initial implementation of Genetic Algorithm with OOP.
- `Problem` abstract base class and `OneMaxProblem`.
- `Logger` for tracking statistics.
- `Visualizer` for plotting results.
- `Solver` for executing the algorithm.
- `main.py` entry point.
