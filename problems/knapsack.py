"""Knapsack Problem Definition"""

__version__ = "0.5.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-24"

import random
from typing import List, Tuple
from .base import Problem

class KnapsackProblem(Problem):
    """0/1 Knapsack Problem: maximize value without exceeding weight capacity."""

    def __init__(self, size: int = 50, capacity_ratio: float = 0.5):
        self.size = size
        self.capacity = int(size * 10 * capacity_ratio)  # Example capacity logic
        
        # Generate random items (value, weight)
        # Using a fixed seed for reproducibility across runs if needed, but here random is fine for demonstration
        # To make it fair/testable, we normally might load from file. Here we generate random instances.
        self.items = []
        for _ in range(size):
            weight = random.randint(1, 20)
            value = random.randint(1, 20)
            self.items.append({'w': weight, 'v': value})

    def create_individual(self) -> List[int]:
        return [random.randint(0, 1) for _ in range(self.size)]

    def evaluate(self, individual: List[int]) -> float:
        total_value = 0
        total_weight = 0
        for i, included in enumerate(individual):
            if included:
                total_value += self.items[i]['v']
                total_weight += self.items[i]['w']
        
        if total_weight > self.capacity:
            # Penalty for exceeding capacity. 
            # Simple approach: Return 0 or penalize heavily. 
            # A common penalty is keeping value but reducing it, or setting to 0.
            return 0  # Invalid solution
            
        return total_value

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
