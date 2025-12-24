import random
from abc import ABC, abstractmethod
from typing import List, Any, Tuple

__version__ = "0.4.0"

class Problem(ABC):
    """Abstract base class for optimization problems."""

    @abstractmethod
    def create_individual(self) -> Any:
        """Create a random individual."""
        pass

    @abstractmethod
    def evaluate(self, individual: Any) -> float:
        """Evaluate the fitness of an individual."""
        pass

    @abstractmethod
    def mutate(self, individual: Any, rate: float) -> Any:
        """Mutate an individual."""
        pass

    @abstractmethod
    def crossover(self, parent1: Any, parent2: Any) -> Tuple[Any, Any]:
        """Perform crossover between two parents."""
        pass

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
