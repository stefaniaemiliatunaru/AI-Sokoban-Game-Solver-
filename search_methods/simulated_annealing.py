import numpy as np
from typing import List
from sokoban.map import Map
from heuristics import ponderated_manhattan_heuristic
import random
random.seed(0)

class Solver:
    def __init__(self, map_obj):
        self.map = map_obj

class SimulatedAnnealing(Solver):
    def __init__(self, map_obj: Map, initial_temperature: float = 10000, final_temperature: float = 0.01, 
                 cooling_rate: float = 0.999, alpha: float = 0.97, max_iters: int = 100000, num_restarts: int = 20) -> None:
        super().__init__(map_obj)
        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.cooling_rate = cooling_rate
        self.alpha = alpha
        self.max_iters = max_iters
        self.num_restarts = num_restarts

    def softmax(self, x):
        x = np.array(x)
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def next_nodes(self, node: Map):
        moves = node.filter_possible_moves()
        neighbours = []
        for move in moves:
            new_map = node.copy()
            new_map.apply_move(move)
            neighbours.append((new_map, move))
        return neighbours

    def simulated_annealing(self, start_map=None) -> List[int]:
        current_state = (start_map or self.map).copy()
        current_cost = ponderated_manhattan_heuristic(current_state)
        best_state = current_state.copy()
        best_cost = current_cost
        best_path = []
        path = []
        temperature = self.initial_temperature
        iters = 0
        while temperature > self.final_temperature and iters < self.max_iters:
            if current_state.is_solved():
                return path
            neighbours = self.next_nodes(current_state)
            if not neighbours:
                break
            neighbour_states = [n[0] for n in neighbours]
            moves = [n[1] for n in neighbours]
            costs = [ponderated_manhattan_heuristic(state) for state in neighbour_states]
            probs = self.softmax(-np.array(costs) / (temperature * self.alpha))
            idx = np.random.choice(len(neighbours), p=probs)
            next_state = neighbour_states[idx]
            next_move = moves[idx]
            next_cost = costs[idx]
            delta = current_cost - next_cost
            if delta > 0:
                current_state = next_state
                current_cost = next_cost
                path.append(next_move)
                if current_cost < best_cost:
                    best_state = current_state.copy()
                    best_cost = current_cost
                    best_path = path.copy()
            else:
                acceptance_probability = np.exp(delta / (temperature * self.alpha))
                if np.random.rand() < acceptance_probability:
                    current_state = next_state
                    current_cost = next_cost
                    path.append(next_move)
            if iters % 1000 == 0 and current_cost > best_cost:
                current_state = best_state.copy()
                current_cost = best_cost
                path = best_path.copy()
            temperature *= self.cooling_rate
            iters += 1
        if best_state.is_solved():
            return best_path
        return path if current_state.is_solved() else []

    def solve(self) -> List[int]:
        best_path = []
        best_length = float('inf')
        for _ in range(self.num_restarts):
            path = self.simulated_annealing()
            if path and len(path) < best_length:
                best_path = path
                best_length = len(path)
        return best_path