"""Main entry point for OptSim"""

__version__ = "0.5.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-24"

import os
import argparse
from datetime import datetime
from problems import OneMaxProblem, KnapsackProblem
from logger import Logger
from visualizer import Visualizer
from solvers import GASolver, RLSolver, SASolver
from rl_env import OneMaxEnv
import version

def run_ga(problem_name="onemax", problem_size=100):
    print(f"Genetic Algorithm Optimizer v{version.__version__}")
    
    # 1. Define the problem
    if problem_name == "knapsack":
        problem = KnapsackProblem(size=problem_size)
    else:
        problem = OneMaxProblem(size=problem_size)
        
    # 2. Setup logging
    logger = Logger()
    
    # 3. Initialize Visualizer
    visualizer = Visualizer()
    
    # 4. Setup Solver
    solver = GASolver(
        problem=problem, 
        logger=logger, 
        pop_size=50, 
        mutation_rate=0.01, 
        generations=50
    )
    
    # 5. Run optimization
    print(f"Starting optimization for {problem_name}...")
    best_solution = solver.solve()
    print("Optimization complete.")
    
    # 6. Show results
    print(f"Best solution fitness: {problem.evaluate(best_solution)}")
    
    # 7. Visualization
    if not os.path.exists("plots"):
        os.makedirs("plots")
        
    visualizer.plot(logger.get_history(), f"plots/ga_{problem_name}_{problem_size}.png")

    # 8. Save Logs
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/ga_{problem_name}_log_{timestamp}.csv"
    logger.save_to_csv(log_filename)
    print(f"Logs saved to {log_filename}")

def run_rl(problem_size=8):
    # RL example currently hardcoded for OneMax for simplicity of state representation
    # Could be extended for Knapsack if state representation is adapted (e.g. current weight + item index)
    print(f"RL Optimizer v{version.__version__}")
    
    if problem_size > 12:
        print("Warning: RL Q-Learning scales poorly with problem size. Capping at 12.")
        problem_size = 12
        
    problem = OneMaxProblem(size=problem_size)
    env = OneMaxEnv(problem)
    
    actions = list(range(problem_size)) 
    
    solver = RLSolver(env, actions=actions, alpha=0.5, gamma=0.9, epsilon=0.2)
    
    solver.train(episodes=500, max_steps=problem_size * 2)
    final_state, path = solver.solve(max_steps=problem_size * 2)
    
    print(f"Final Solution: {final_state}")
    print(f"Fitness: {problem.evaluate(list(final_state))}/{problem_size}")
    print(f"Steps taken: {len(path) - 1}")

def run_sa(problem_name="onemax", problem_size=100):
    print(f"Simulated Annealing Optimizer v{version.__version__}")
    
    if problem_name == "knapsack":
        problem = KnapsackProblem(size=problem_size)
    else:
        problem = OneMaxProblem(size=problem_size)
        
    logger = Logger()
    visualizer = Visualizer()
    
    solver = SASolver(
        problem=problem,
        logger=logger,
        initial_temp=100.0,
        cooling_rate=0.95,
        min_temp=0.01,
        max_steps=500
    )
    
    print(f"Starting optimization for {problem_name}...")
    best_solution = solver.solve()
    print("Optimization complete.")
    
    print(f"Best solution fitness: {problem.evaluate(best_solution)}")
    
    if not os.path.exists("plots"):
        os.makedirs("plots")
    
    visualizer.plot(logger.get_history(), f"plots/sa_{problem_name}_{problem_size}.png")
    
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/sa_{problem_name}_log_{timestamp}.csv"
    logger.save_to_csv(log_filename)
    print(f"Logs saved to {log_filename}")

def main():
    parser = argparse.ArgumentParser(description="OptSim Optimizer")
    parser.add_argument("--solver", choices=["ga", "rl", "sa"], default="ga", help="Solver to use")
    parser.add_argument("--problem", choices=["onemax", "knapsack"], default="onemax", help="Problem to solve")
    parser.add_argument("--size", type=int, default=0, help="Problem size")
    
    args = parser.parse_args()
    
    if args.solver == "ga":
        size = args.size if args.size > 0 else 100
        run_ga(args.problem, size)
    elif args.solver == "rl":
        if args.problem != "onemax":
            print("RL currently only supports OneMax.")
            return
        size = args.size if args.size > 0 else 8
        run_rl(size)
    elif args.solver == "sa":
        size = args.size if args.size > 0 else 100
        run_sa(args.problem, size)

if __name__ == "__main__":
    main()
