import os
from datetime import datetime
from problem import OneMaxProblem
from logger import Logger
from visualizer import Visualizer
from solver import Solver
import version

__version__ = "0.2.0"

def main():
    print(f"Genetic Algorithm Optimizer v{version.__version__}")
    # 1. Define the problem
    problem = OneMaxProblem(size=100)
    
    # 2. Setup logging
    logger = Logger()
    
    # 3. Initialize Visualizer
    visualizer = Visualizer()
    
    # 4. Setup Solver
    solver = Solver(
        problem=problem, 
        logger=logger, 
        pop_size=50, 
        mutation_rate=0.01, 
        generations=50
    )
    
    # 5. Run optimization
    print("Starting optimization...")
    best_solution = solver.solve()
    print("Optimization complete.")
    
    # 6. Show results
    print(f"Best solution fitness: {problem.evaluate(best_solution)}")
    
    # 7. Visualization
    visualizer.plot(logger.get_history(), "d:/Projects/optsim/onemax_plot.png")

    # 8. Save Logs
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/log_{timestamp}.csv"
    logger.save_to_csv(log_filename)
    print(f"Logs saved to {log_filename}")

if __name__ == "__main__":
    main()
