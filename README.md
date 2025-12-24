# Genetic Algorithm Optimizer

A modular Python implementation of a Genetic Algorithm designed to solve optimization problems. This project currently includes an implementation for the **OneMax** problem but is designed to be extensible for other optimization tasks.

## Features

- **Modular Architecture**: Separated concerns into Problem, Solver, Logger, and Visualizer components.
- **Genetic Algorithm**: Implements tournament selection, uniform crossover (via child generation), mutation, and elitism.
- **Logging**:
  - Real-time console output of generation statistics.
  - CSV logging of best fitness, average fitness, and the best solution string for every generation.
- **Visualization**: Generates a plot of the evolutionary progress (Best vs. Average Fitness) using Matplotlib.

## Project Structure

- **`main.py`**: The entry point of the application. Orchestrates the setup of the problem, solver, logger, and visualizer.
- **`solver.py`**: Contains the `Solver` class which implements the core Genetic Algorithm logic.
- **`problem.py`**: Defines the `Problem` abstract base class and the `OneMaxProblem` concrete implementation.
- **`logger.py`**: Handles logging of statistics to both the console and CSV files.
- **`visualizer.py`**: Uses `matplotlib` to generate fitness plots from the log history.
- **`version.py`**: Contains the version information.

## Requirements

- Python 3.x
- Matplotlib

You can install the necessary dependencies using pip:

```bash
pip install matplotlib
```

## Usage

To run the optimizer with the default OneMax problem:

```bash
python main.py
```

### Output

1. **Console Output**: Shows progress for each generation.
   ```text
   Gen 1: Best Fitness = 62, Avg Fitness = 50.28, Best Sol = [1, 1, ... 0]
   ...
   Optimization complete.
   Best solution fitness: 100
   ```

2. **Plots**: A plot image (e.g., `onemax_plot.png`) is saved to the project root, showing the convergence of fitness over generations.

3. **Logs**: A CSV file (e.g., `logs/log_YYYYMMDD_HHMMSS.csv`) is created in the `logs` directory containing detailed statistics for each generation.

## Extensibility

To solve a new problem:
1. Create a new class that inherits from the `Problem` class in `problem.py`.
2. Implement the abstract methods: `create_individual`, `evaluate`, `mutate`, and `crossover`.
3. Instantiate your new problem class in `main.py` and pass it to the `Solver`.
