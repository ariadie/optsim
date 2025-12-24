"""Optimization Problem Definitions - Base Class"""

__version__ = "0.5.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-24"

from abc import ABC, abstractmethod
from typing import Any, Tuple

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
