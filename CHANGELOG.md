# Changelog

All notable changes to this project will be documented in this file.

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
