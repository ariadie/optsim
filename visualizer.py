"""Visualization Utility"""

__version__ = "0.7.0"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-25"

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import numpy as np
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

    def animate_best_individual(self, history: List[Dict[str, Any]], filename: str = "best_individual_animation.gif", fps: int = 2):
        """
        Create an animated visualization showing how the best individual evolves over generations.
        
        Args:
            history: Logger history containing best_solution for each generation
            filename: Output filename (.gif or .mp4)
            fps: Frames per second (default: 2 for educational viewing)
        """
        if not history or 'best_solution' not in history[0]:
            print("No best_solution data available for animation.")
            return
        
        # Extract data
        generations = [entry['generation'] for entry in history]
        best_solutions = [entry['best_solution'] for entry in history]
        best_fitness = [entry['best_fitness'] for entry in history]
        
        # Get problem size
        problem_size = len(best_solutions[0])
        max_fitness = max(best_fitness)
        
        # Setup figure
        fig = plt.figure(figsize=(12, 6))
        gs = fig.add_gridspec(3, 1, height_ratios=[1, 3, 1], hspace=0.3)
        
        ax_title = fig.add_subplot(gs[0])
        ax_bits = fig.add_subplot(gs[1])
        ax_progress = fig.add_subplot(gs[2])
        
        # Remove axes for title and progress
        ax_title.axis('off')
        ax_progress.set_xlim(0, 1)
        ax_progress.set_ylim(0, 1)
        ax_progress.axis('off')
        
        def update(frame):
            """Update function for each animation frame."""
            gen = generations[frame]
            solution = best_solutions[frame]
            fitness = best_fitness[frame]
            
            # Clear axes
            ax_title.clear()
            ax_bits.clear()
            ax_progress.clear()
            
            ax_title.axis('off')
            ax_progress.axis('off')
            
            # Title with generation and fitness
            ax_title.text(0.5, 0.5, f'Generation: {gen}    Fitness: {int(fitness)}/{problem_size}', 
                         ha='center', va='center', fontsize=16, fontweight='bold')
            
            # Draw binary string as colored squares
            colors = ['#2ecc71' if bit == 1 else '#e74c3c' for bit in solution]
            
            # Calculate grid dimensions for better layout
            cols = min(20, problem_size)  # Max 20 columns
            rows = (problem_size + cols - 1) // cols  # Ceiling division
            
            ax_bits.set_xlim(-0.5, cols - 0.5)
            ax_bits.set_ylim(-0.5, rows - 0.5)
            ax_bits.set_aspect('equal')
            ax_bits.invert_yaxis()
            
            # Draw squares
            for i, (bit, color) in enumerate(zip(solution, colors)):
                row = i // cols
                col = i % cols
                
                # Draw square
                square = plt.Rectangle((col - 0.4, row - 0.4), 0.8, 0.8, 
                                       facecolor=color, edgecolor='black', linewidth=1)
                ax_bits.add_patch(square)
                
                # Add bit value as text
                ax_bits.text(col, row, str(bit), ha='center', va='center', 
                           fontsize=10, fontweight='bold', color='white')
            
            # Remove ticks and labels
            ax_bits.set_xticks([])
            ax_bits.set_yticks([])
            ax_bits.set_title('Best Individual (Green=1, Red=0)', fontsize=12, pad=10)
            
            # Progress bar
            progress = fitness / max_fitness if max_fitness > 0 else 0
            
            # Background bar
            ax_progress.add_patch(plt.Rectangle((0.1, 0.3), 0.8, 0.4, 
                                               facecolor='lightgray', edgecolor='black', linewidth=2))
            
            # Progress bar
            ax_progress.add_patch(plt.Rectangle((0.1, 0.3), 0.8 * progress, 0.4, 
                                               facecolor='#3498db', edgecolor='black', linewidth=2))
            
            # Progress text
            ax_progress.text(0.5, 0.5, f'{progress*100:.1f}% Optimal', 
                           ha='center', va='center', fontsize=12, fontweight='bold')
            
            return []
        
        # Create animation
        print(f"Creating animation with {len(generations)} frames...")
        anim = animation.FuncAnimation(fig, update, frames=len(generations), 
                                      interval=1000/fps, repeat=True, blit=False)
        
        # Save animation
        try:
            writer = PillowWriter(fps=fps)
            anim.save(filename, writer=writer)
            print(f"Animation saved to {filename}")
        except Exception as e:
            print(f"Error saving animation: {e}")
            print("Make sure 'pillow' is installed: pip install pillow")
        finally:
            plt.close(fig)
