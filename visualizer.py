"""Visualization Utility"""

__version__ = "0.6.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-25"

import matplotlib.pyplot as plt
from typing import List, Dict, Any

class Visualizer:
    """Class for visualizing evolutionary progress."""

    def plot_fitness(self, history: List[Dict[str, Any]], filename: str = "evolution_plot.png"):
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
        print(f"Fitness plot saved to {filename}")
        plt.close()

    def plot_population_heatmap(self, history: List[Dict[str, Any]], filename: str = "population_heatmap.png"):
        """
        Plot a heatmap showing the convergence of genes/bits over generations.
        X-axis: Generation
        Y-axis: Gene Position
        Color: Average value of that gene in the population (0.0 to 1.0)
        """
        if not history or 'population' not in history[0]:
            print("No population data available for heatmap.")
            return

        # Prepare grid: rows=Gene Position, cols=Generation
        # Assuming all individuals have same length
        ind_length = len(history[0]['population'][0])
        grid = []

        for entry in history:
            pop = entry['population']
            # Calculate average for each gene position
            gene_avgs = [0.0] * ind_length
            for ind in pop:
                for i, gene in enumerate(ind):
                    gene_avgs[i] += gene
            
            gene_avgs = [x / len(pop) for x in gene_avgs]
            grid.append(gene_avgs)
        
        # Transpose so X is generation (currently grid is [gen][gene])
        # We want matrix [gene][gen] for imshow where X is col index
        grid_t = list(zip(*grid))

        plt.figure(figsize=(12, 6))
        plt.imshow(grid_t, aspect='auto', cmap='RdYlGn', vmin=0, vmax=1, origin='lower')
        plt.colorbar(label='Gene Frequency (0=None, 1=All)')
        plt.title('Population Convergence Heatmap')
        plt.xlabel('Generation')
        plt.ylabel('Gene Index')
        plt.savefig(filename)
        print(f"Heatmap saved to {filename}")
        plt.close()

    def plot_knapsack_solution(self, problem, solution: List[int], filename: str = "knapsack_solution.png"):
        """
        Visualize the knapsack solution.
        Bar chart of all items, colored by selection status.
        Reference line for item weight vs capacity?
        Actually simpler: Bar chart of weights of selected items.
        """
        # Data prep
        items = problem.items
        capacity = problem.capacity
        
        indices = range(len(items))
        weights = [item['w'] for item in items]
        values = [item['v'] for item in items]
        
        # Colors: Green if selected, Gray if not
        colors = ['green' if bit == 1 else 'lightgray' for bit in solution]
        
        plt.figure(figsize=(12, 6))
        
        # Plot Weights
        plt.subplot(2, 1, 1)
        bars = plt.bar(indices, weights, color=colors)
        plt.axhline(y=0, color='black', linewidth=0.5)
        plt.ylabel('Weight')
        plt.title(f'Knapsack Solution (Capacity: {capacity}) - Green = Selected')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Plot Values
        plt.subplot(2, 1, 2)
        plt.bar(indices, values, color=colors)
        plt.ylabel('Value')
        plt.xlabel('Item Index')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(filename)
        print(f"Knapsack solution plot saved to {filename}")
        plt.close()
