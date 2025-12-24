"""Solver for Reinforcement Learning (Q-Learning)"""

__version__ = "0.4.1"
__author__ = "ariadie@gmail.com"
__date__ = "2025-12-24"

import random
from typing import Dict, Tuple, List, Any
from rl_env import RLEnvironment

class RLSolver:
    """Tabular Q-Learning Solver."""
    
    def __init__(self, env: RLEnvironment, actions: List[int], 
                 alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 0.1):
        self.env = env
        self.actions = actions
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table: Dict[Tuple[int, ...], Dict[int, float]] = {}

    def get_q(self, state: Tuple[int, ...], action: int) -> float:
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        return self.q_table[state][action]

    def update_q(self, state: Tuple[int, ...], action: int, reward: float, next_state: Tuple[int, ...]):
        old_q = self.get_q(state, action)
        
        # Max Q for next state
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0.0 for a in self.actions}
        max_next_q = max(self.q_table[next_state].values())
        
        # Q-learning update rule
        new_q = old_q + self.alpha * (reward + self.gamma * max_next_q - old_q)
        self.q_table[state][action] = new_q

    def choose_action(self, state: Tuple[int, ...]) -> int:
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            # Exploitation: best action
            if state not in self.q_table:
                self.q_table[state] = {a: 0.0 for a in self.actions}
            return max(self.q_table[state], key=self.q_table[state].get)

    def train(self, episodes: int = 1000, max_steps: int = 50):
        print(f"Training for {episodes} episodes...")
        for ep in range(episodes):
            state = self.env.reset()
            total_reward = 0
            
            for _ in range(max_steps):
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                
                self.update_q(state, action, reward, next_state)
                
                state = next_state
                total_reward += reward
                
                if done:
                    break
            
            # Decay epsilon (optional)
            if ep % 100 == 0:
                self.epsilon = max(0.01, self.epsilon * 0.99)
                
        print("Training complete.")

    def solve(self, max_steps: int = 50) -> Any:
        # Run a greedy episode without exploration
        state = self.env.reset()
        original_epsilon = self.epsilon
        self.epsilon = 0  # Force exploitation
        
        path = [state]
        for _ in range(max_steps):
            action = self.choose_action(state)
            next_state, _, done = self.env.step(action)
            state = next_state
            path.append(state)
            if done:
                break
        
        self.epsilon = original_epsilon
        return state, path
