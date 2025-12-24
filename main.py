import os
import argparse
from datetime import datetime
from problem import OneMaxProblem
from logger import Logger
from visualizer import Visualizer
from solvers import GASolver, RLSolver, SASolver
from rl_env import OneMaxEnv
import version

__version__ = "0.4.0"

def run_ga(problem_size=100):
    print(f"Genetic Algorithm Optimizer v{version.__version__}")
    # 1. Define the problem
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
    print("Starting optimization...")
    best_solution = solver.solve()
    print("Optimization complete.")
    
    # 6. Show results
    print(f"Best solution fitness: {problem.evaluate(best_solution)}")
    
    # 7. Visualization
    if not os.path.exists("plots"):
        os.makedirs("plots")
        
    visualizer.plot(logger.get_history(), f"plots/ga_onemax_{problem_size}.png")

    # 8. Save Logs
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/ga_log_{timestamp}.csv"
    logger.save_to_csv(log_filename)
    print(f"Logs saved to {log_filename}")

def run_rl(problem_size=8):
    print(f"RL Optimizer v{version.__version__}")
    
    # Use smaller size for Q-learning to avoid massive state space
    # 8 bits = 256 states
    if problem_size > 12:
        print("Warning: RL Q-Learning scales poorly with problem size. Capping at 12.")
        problem_size = 12
        
    problem = OneMaxProblem(size=problem_size)
    env = OneMaxEnv(problem)
    
    actions = list(range(problem_size)) # Actions are indices 0..size-1
    
    solver = RLSolver(env, actions=actions, alpha=0.5, gamma=0.9, epsilon=0.2)
    
    # Train
    solver.train(episodes=500, max_steps=problem_size * 2)
    
    # Solve
    final_state, path = solver.solve(max_steps=problem_size * 2)
    
    print(f"Final Solution: {final_state}")
    print(f"Fitness: {problem.evaluate(list(final_state))}/{problem_size}")
    print(f"Steps taken: {len(path) - 1}")
    print("Path trajectory (last 5 steps):")
    for s in path[-5:]:
        print(s)

def run_sa(problem_size=100):
    print(f"Simulated Annealing Optimizer v{version.__version__}")
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
    
    print("Starting optimization...")
    best_solution = solver.solve()
    print("Optimization complete.")
    
    print(f"Best solution fitness: {problem.evaluate(best_solution)}")
    
    if not os.path.exists("plots"):
        os.makedirs("plots")
    
    visualizer.plot(logger.get_history(), f"plots/sa_onemax_{problem_size}.png")
    
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs/sa_log_{timestamp}.csv"
    logger.save_to_csv(log_filename)
    print(f"Logs saved to {log_filename}")

def main():
    parser = argparse.ArgumentParser(description="OptSim Optimizer")
    parser.add_argument("--solver", choices=["ga", "rl", "sa"], default="ga", help="Solver to use: ga, rl, or sa")
    parser.add_argument("--size", type=int, default=0, help="Problem size (default: 100 for GA/SA, 8 for RL)")
    
    args = parser.parse_args()
    
    if args.solver == "ga":
        size = args.size if args.size > 0 else 100
        run_ga(size)
    elif args.solver == "rl":
        size = args.size if args.size > 0 else 8
        run_rl(size)
    elif args.solver == "sa":
        size = args.size if args.size > 0 else 100
        run_sa(size)

if __name__ == "__main__":
    main()
