from typing import List, Tuple
from math import inf
from sokoban.map import Map
from heuristics import ponderated_manhattan_heuristic

class Solver:
    def __init__(self, map_obj):
        self.map = map_obj

class IDAStar(Solver):
    def __init__(self, map_obj: Map) -> None:
        super().__init__(map_obj)
        self.visited_states = {}

    def next_nodes(self, node: Map) -> List[Tuple[Map, int]]:
        moves = node.filter_possible_moves()
        neighbours = node.get_neighbours()
        next_states = []
        for i, neighbour in enumerate(neighbours):
            next_states.append((neighbour, moves[i]))
        
        return next_states

    def create_state_tuple(self, node: Map) -> tuple:
        player_pos = (node.player.x, node.player.y)
        box_positions = tuple(sorted(node.positions_of_boxes.keys()))
        return (player_pos, box_positions)

    def Search(self, node: Map, g: int, threshold: int, path: List[int]) -> Tuple[bool, int, List[int]]:
        f = g + ponderated_manhattan_heuristic(node)
        if f > threshold:
            return False, f, []
        if node.is_solved():
            return True, 0, path
        current_state = self.create_state_tuple(node)
        if current_state in self.visited_states and g >= self.visited_states[current_state]:
            return False, float('inf'), []
        self.visited_states[current_state] = g
        min_f = float('inf')
        min_path = []
        for next_state, move in self.next_nodes(node):
            found, new_f, temp_path = self.Search(next_state, g + 1, threshold, path + [move])
            if found:
                return True, new_f, temp_path
            if new_f < min_f:
                min_f = new_f
                min_path = temp_path
                
        return False, min_f, min_path

    def IDA_star(self) -> List[int]:
        threshold = ponderated_manhattan_heuristic(self.map)
        while True:
            self.visited_states = {}
            found, new_threshold, path = self.Search(self.map, 0, threshold, [])
            if found:
                return path
            if new_threshold == float('inf'):
                return []
            threshold = new_threshold

    def solve(self) -> List[int]:
        return self.IDA_star()
