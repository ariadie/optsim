# OptSim Optimizer

A modular Python framework for optimization problems. This project includes implementations for **Genetic Algorithm (GA)** and **Reinforcement Learning (RL)** solvers, using the **OneMax** problem as a demonstration.

## Features

- **Multi-Solver Architecture**: modular design supporting different optimization strategies (GA, RL).
- **Genetic Algorithm**: Tournament selection, uniform crossover, mutation, elitism.
- **Reinforcement Learning**: Tabular Q-Learning integration for smaller problem spaces.
- **Logging & Visualization**: Real-time console output, CSV logging, and fitness history plotting.

## Project Structure

- **`main.py`**: Entry point. Orchestrates the problem, solver selection, logging, and visualization.
- **`solvers/`**:
  - **`ga_solver.py`**: Genetic Algorithm implementation.
  - **`rl_solver.py`**: Q-Learning implementation.
- **`problem.py`**: Abstract base class and `OneMaxProblem` implementation.
- **`rl_env.py`**: OpenAI Gym-like wrapper for RL solvers.
- **`logger.py`**: Statistics logging.
- **`visualizer.py`**: Plotting utilities.

## Requirements

- Python 3.x
- Matplotlib

Install dependencies:
```bash
pip install matplotlib
```

## Usage

Run the optimizer with your preferred solver:

### Genetic Algorithm (Default)
Suitable for larger problem sizes (e.g., 100 bits).
```bash
python main.py --solver ga --problem onemax --size 100
```
- **Output**: Plot saved to `plots/ga_onemax_100.png`, logs to `logs/ga_onemax_log_....csv`.

### Reinforcement Learning
Suitable for small problem sizes (e.g., 8-12 bits) due to state space explosion ($2^N$). Currently supports OneMax only.
```bash
python main.py --solver rl --size 8
```
- **Output**: Console description of the solution path.

### Simulated Annealing
Suitable for various problem sizes, provides a good balance between exploration and exploitation.
```bash
python main.py --solver sa --problem knapsack --size 50
```
- **Output**: Plot saved to `plots/sa_knapsack_50.png`, logs to `logs/sa_knapsack_log_....csv`.

## Extensibility

### Adding a New Problem
1. Inherit from `Problem` in `problem.py`.
2. Implement `create_individual`, `evaluate`, `mutate`, and `crossover`.
3. Use it in `main.py`.

### Adding a New Solver
1. Create a new file in `solvers/` (e.g., `sa_solver.py`).
2. Implement your solver class.
3. Import and add a new branch in `main.py` to handle the new solver.

## Future Recommendations

To further enhance this framework, consider adding:
1.  **Simulated Annealing (SA)**: Good for local search and escaping local optima.
2.  **Particle Swarm Optimization (PSO)**: Effective for continuous optimization problems (would require adapting `Problem` for continuous domains).
3.  **Deep Q-Network (DQN)**: Replace tabular Q-Learning with a neural network to scale RL to larger problem sizes.
