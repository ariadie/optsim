"""Problems Package"""

__version__ = "0.5.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-24"

from .base import Problem
from .onemax import OneMaxProblem
from .knapsack import KnapsackProblem

__all__ = ['Problem', 'OneMaxProblem', 'KnapsackProblem']
