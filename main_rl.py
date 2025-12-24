from problem import OneMaxProblem
from rl_env import OneMaxEnv
from rl_solver import RLSolver

__version__ = "0.3.0"

def main():
    print("RL Optimizer Demo for OptSim")
    
    # Use smaller size for Q-learning to avoid massive state space
    # 8 bits = 256 states
    problem_size = 8
    problem = OneMaxProblem(size=problem_size)
    env = OneMaxEnv(problem)
    
    actions = list(range(problem_size)) # Actions are indices 0..7
    
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

if __name__ == "__main__":
    main()
