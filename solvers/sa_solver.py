"""Solver for Simulated Annealing"""

__version__ = "0.5.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-24"

import random
import math
from typing import List, Any
from problems import Problem
from logger import Logger

class SASolver:
    """Simulated Annealing Solver."""

    def __init__(self, problem: Problem, logger: Logger, 
                 initial_temp: float = 100.0, cooling_rate: float = 0.95, 
                 min_temp: float = 0.01, max_steps: int = 1000):
        self.problem = problem
        self.logger = logger
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_steps = max_steps
        self.current_solution = None
        self.best_solution = None

    def solve(self):
        """Run the Simulated Annealing algorithm."""
        # Initialize
        self.current_solution = self.problem.create_individual()
        self.best_solution = self.current_solution
        
        current_fitness = self.problem.evaluate(self.current_solution)
        best_fitness = current_fitness
        
        temp = self.initial_temp
        step = 0
        
        print(f"Starting SA: T={temp}, Max Steps={self.max_steps}")

        while temp > self.min_temp and step < self.max_steps:
            step += 1
            
            # Generate neighbor (mutate 1 bit effectively)
            # For SA we typically want a small change. The mutation rate for OneMax 
            # usually flips bits with a prob. Here we'll ensure at least one change or use standard mutation behavior.
            # Let's use the problem's mutate with a rate equivalent to 1/size to flip ~1 bit.
            mutation_rate = 1.0 / len(self.current_solution)
            neighbor = self.problem.mutate(self.current_solution, mutation_rate)
            neighbor_fitness = self.problem.evaluate(neighbor)
            
            # Calculate energy delta (we want to maximize fitness, so E = -Fitness)
            # Delta E = E_new - E_old = (-f_new) - (-f_old) = f_old - f_new
            # If f_new > f_old, delta E < 0 (improvement), we accept.
            # P = exp(-delta E / T) = exp((f_new - f_old) / T)
            
            delta_fitness = neighbor_fitness - current_fitness
            
            if delta_fitness > 0 or random.random() < math.exp(delta_fitness / temp):
                self.current_solution = neighbor
                current_fitness = neighbor_fitness
                
                if current_fitness > best_fitness:
                    self.best_solution = self.current_solution
                    best_fitness = current_fitness
            
            # Logging (log every step or periodically? existing logger expects generations)
            # We'll treat 'step' as 'generation' for consistency with visualizer
            self.logger.log(step, best_fitness, current_fitness, self.best_solution)
            
            # Cool down
            temp *= self.cooling_rate
            
        return self.best_solution
