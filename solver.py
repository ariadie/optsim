import random
from typing import List, Any
from problem import Problem
from logger import Logger

__version__ = "0.2.0"

class Solver:
    """Genetic Algorithm Solver."""

    def __init__(self, problem: Problem, logger: Logger, 
                 pop_size: int = 50, mutation_rate: float = 0.01, generations: int = 100):
        self.problem = problem
        self.logger = logger
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population: List[Any] = []

    def initialize_population(self):
        """Initialize the population with random individuals."""
        self.population = [self.problem.create_individual() for _ in range(self.pop_size)]

    def select_parent(self) -> Any:
        """Tournament selection."""
        tournament = random.sample(self.population, 3)
        return max(tournament, key=self.problem.evaluate)

    def solve(self):
        """Run the genetic algorithm."""
        self.initialize_population()

        for gen in range(1, self.generations + 1):
            # Evaluation
            fitness_scores = [self.problem.evaluate(ind) for ind in self.population]
            best_fitness = max(fitness_scores)
            avg_fitness = sum(fitness_scores) / self.pop_size
            best_ind = self.population[fitness_scores.index(best_fitness)]
            
            # Logging
            self.logger.log(gen, best_fitness, avg_fitness, best_ind)
            
            # Selection and Reproduction
            new_population = []
            
            # Elitism: keep the best individual
            new_population.append(best_ind)
            
            while len(new_population) < self.pop_size:
                parent1 = self.select_parent()
                parent2 = self.select_parent()
                
                child1, child2 = self.problem.crossover(parent1, parent2)
                
                child1 = self.problem.mutate(child1, self.mutation_rate)
                child2 = self.problem.mutate(child2, self.mutation_rate)
                
                new_population.extend([child1, child2])
            
            self.population = new_population[:self.pop_size]

        return max(self.population, key=self.problem.evaluate)
