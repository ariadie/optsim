# OptSim Optimizer

A modular Python framework for optimization problems. This project includes implementations for **Genetic Algorithm (GA)** and **Reinforcement Learning (RL)** solvers, using the **OneMax** problem as a demonstration.

## Features

- **Multi-Solver Architecture**: modular design supporting different optimization strategies (GA, RL, SA).
- **Genetic Algorithm**: Tournament selection, uniform crossover, mutation, elitism.
- **Reinforcement Learning**: Tabular Q-Learning integration for smaller problem spaces.
- **Simulated Annealing**: Temperature-based probabilistic search for escaping local optima.
- **Multiple Problem Types**: OneMax (bit optimization) and Knapsack (combinatorial optimization).
- **Enhanced Visualization**: 
  - Fitness progression plots (best/average over generations)
  - Population diversity heatmaps (gene convergence analysis)
  - Problem-specific visualizations (e.g., Knapsack item selection charts)
- **Logging**: Real-time console output and CSV export for detailed analysis.

## Project Structure

- **`main.py`**: Entry point. Orchestrates the problem, solver selection, logging, and visualization.
- **`solvers/`**:
  - **`ga_solver.py`**: Genetic Algorithm implementation.
  - **`rl_solver.py`**: Q-Learning implementation.
  - **`sa_solver.py`**: Simulated Annealing implementation.
- **`problems/`**:
  - **`base.py`**: Abstract base class for optimization problems.
  - **`onemax.py`**: OneMax problem implementation.
  - **`knapsack.py`**: 0/1 Knapsack problem implementation.
- **`rl_env.py`**: OpenAI Gym-like wrapper for RL solvers.
- **`logger.py`**: Statistics and population logging.
- **`visualizer.py`**: Advanced plotting utilities (fitness, heatmaps, problem-specific charts).

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
- **Output**: All files saved to `logs/` directory with timestamps:
  - `logs/ga_onemax_100_fitness_YYYYMMDD_HHMMSS.png` - Fitness progression
  - `logs/ga_onemax_100_heatmap_YYYYMMDD_HHMMSS.png` - Population diversity
  - `logs/ga_onemax_log_YYYYMMDD_HHMMSS.csv` - Detailed statistics

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
- **Output**: All files saved to `logs/` directory with timestamps.

## Visualization Features

The framework generates multiple visualizations to help understand algorithm behavior:

### Fitness Progression Plot
Shows best and average fitness over generations. Useful for:
- Detecting convergence speed
- Identifying premature convergence (plateau)
- Comparing solver performance

### Population Diversity Heatmap
Color-coded visualization of gene convergence:
- **X-axis**: Generation number
- **Y-axis**: Gene/bit position
- **Color**: Average gene value across population (0.0 = all zeros, 1.0 = all ones)

Useful for:
- Detecting diversity loss
- Identifying which genes converge early vs. late
- Tuning mutation rates and population sizes

### Problem-Specific Visualizations
**Knapsack Solution Chart**: Two-panel bar chart showing selected items (green) vs. unselected (gray), with weight and value distributions.

Example for Knapsack problem:
```bash
python main.py --problem knapsack --size 20
```
Generates (all in `logs/` directory with timestamp):
- `ga_knapsack_20_fitness_YYYYMMDD_HHMMSS.png` - Fitness progression
- `ga_knapsack_20_heatmap_YYYYMMDD_HHMMSS.png` - Population diversity
- `ga_knapsack_20_solution_YYYYMMDD_HHMMSS.png` - Item selection visualization
- `ga_knapsack_log_YYYYMMDD_HHMMSS.csv` - Detailed statistics


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
