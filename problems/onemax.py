"""OneMax Problem Definition"""

__version__ = "0.5.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-24"

import random
from typing import List, Tuple
from .base import Problem

class OneMaxProblem(Problem):
    """OneMax problem: maximize the number of 1s in a bitstring."""

    def __init__(self, size: int = 100):
        self.size = size

    def create_individual(self) -> List[int]:
        return [random.randint(0, 1) for _ in range(self.size)]

    def evaluate(self, individual: List[int]) -> float:
        return sum(individual)

    def mutate(self, individual: List[int], rate: float) -> List[int]:
        new_ind = individual[:]
        for i in range(len(new_ind)):
            if random.random() < rate:
                new_ind[i] = 1 - new_ind[i]
        return new_ind

    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        point = random.randint(1, self.size - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
