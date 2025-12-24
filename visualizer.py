import matplotlib.pyplot as plt
from typing import List, Dict, Any

__version__ = "0.2.0"

class Visualizer:
    """Class for visualizing evolutionary progress."""

    def plot(self, history: List[Dict[str, Any]], filename: str = "evolution_plot.png"):
        """Plot the fitness history."""
        generations = [entry['generation'] for entry in history]
        best_fitness = [entry['best_fitness'] for entry in history]
        avg_fitness = [entry['avg_fitness'] for entry in history]

        plt.figure(figsize=(10, 6))
        plt.plot(generations, best_fitness, label='Best Fitness', color='green')
        plt.plot(generations, avg_fitness, label='Average Fitness', color='blue', linestyle='--')
        
        plt.title('Evolutionary Progress')
        plt.xlabel('Generation')
        plt.ylabel('Fitness')
        plt.legend()
        plt.grid(True)
        plt.savefig(filename)
        print(f"Plot saved to {filename}")
        plt.close()
