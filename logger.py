import csv
from typing import List, Dict, Any

__version__ = "0.4.0"

class Logger:
    """Class for logging evolutionary statistics."""

    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def log(self, generation: int, best_fitness: float, avg_fitness: float, best_solution: Any = None):
        """Log statistics for a generation."""
        entry = {
            "generation": generation,
            "best_fitness": best_fitness,
            "avg_fitness": avg_fitness,
            "best_solution": best_solution
        }
        self.history.append(entry)
        print(f"Gen {generation}: Best Fitness = {best_fitness}, Avg Fitness = {avg_fitness:.2f}, Best Sol = {best_solution}")

    def get_history(self) -> List[Dict[str, Any]]:
        """Return the logged history."""
        return self.history

    def save_to_csv(self, filename: str):
        """Save history to a CSV file."""
        if not self.history:
            return
        
        keys = self.history[0].keys()
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.history)
