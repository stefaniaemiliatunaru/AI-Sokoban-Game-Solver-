import os
import sys
import math
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

def euclidean_distance(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])

def manhattan_distance(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])

def ponderated_euclidian_heuristic(state, weight=2) -> float:
    boxes = list(state.positions_of_boxes.keys())
    targets = list(state.targets)
    total = 0
    used_targets = set()
    
    for box in boxes:
        min_dist = float('inf')
        min_target = None
        for target in targets:
            if target in used_targets:
                continue
            dist = euclidean_distance(box, target)
            if dist < min_dist:
                min_dist = dist
                min_target = target
        if min_target is not None:
            used_targets.add(min_target)
        total += min_dist
    
    player = (state.player.x, state.player.y)
    min_player_box = min(euclidean_distance(player, box) for box in boxes)
    
    return weight * total + min_player_box

def ponderated_manhattan_heuristic(state, weight=2) -> int:
    boxes = list(state.positions_of_boxes.keys())
    targets = list(state.targets)
    total = 0
    used_targets = set()
    
    for box in boxes:
        min_dist = float('inf')
        min_target = None
        for target in targets:
            if target in used_targets:
                continue
            dist = manhattan_distance(box, target)
            if dist < min_dist:
                min_dist = dist
                min_target = target
        if min_target is not None:
            used_targets.add(min_target)
        total += min_dist
    
    player = (state.player.x, state.player.y)
    min_player_box = min(manhattan_distance(player, box) for box in boxes)
    
    return weight * total + min_player_box
