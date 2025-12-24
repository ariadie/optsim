import random
from abc import ABC, abstractmethod
from typing import Any, Tuple, List
from problem import Problem, OneMaxProblem

__version__ = "0.4.0"

class RLEnvironment(ABC):
    """Abstract base class for RL Environments."""
    
    @abstractmethod
    def reset(self) -> Any:
        """Reset the environment and return the initial state."""
        pass
    
    @abstractmethod
    def step(self, action: Any) -> Tuple[Any, float, bool]:
        """Apply action, return (next_state, reward, done)."""
        pass

class OneMaxEnv(RLEnvironment):
    """OneMax problem as an RL environment."""
    
    def __init__(self, problem: OneMaxProblem):
        self.problem = problem
        self.state: List[int] = []
        self.current_fitness = 0.0
        
    def reset(self) -> Tuple[int, ...]:
        self.state = self.problem.create_individual()
        self.current_fitness = self.problem.evaluate(self.state)
        return tuple(self.state)
    
    def step(self, action: int) -> Tuple[Tuple[int, ...], float, bool]:
        """
        Action: Index of the bit to flip (0 to size-1).
        Reward: Change in fitness.
        Done: If maximum fitness is reached.
        """
        # Copy state to avoid mutation if referenced elsewhere (optional safety)
        new_state = list(self.state)
        
        # Apply action: Flip bit at index 'action'
        if 0 <= action < len(new_state):
            new_state[action] = 1 - new_state[action]
            
        new_fitness = self.problem.evaluate(new_state)
        reward = new_fitness - self.current_fitness
        
        self.state = new_state
        self.current_fitness = new_fitness
        
        # Check for termination (optional, OneMax relies on reaching size)
        done = self.current_fitness == self.problem.size
        
        return tuple(self.state), reward, done
