import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from sokoban import Map, save_images, create_gif
from ida_star import IDAStar
from simulated_annealing import SimulatedAnnealing

def count_pull_moves(solution, current_map):
    pull_moves = 0
    temp_map = current_map.copy()
    for move in solution:
        before_undo = temp_map.undo_moves
        temp_map.apply_move(move)
        after_undo = temp_map.undo_moves
        if after_undo > before_undo:
            pull_moves += 1
            
    return pull_moves

def run_and_save_gif(solver_class, map_file, images_folder, gif_suffix):
    tests_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests')
    map_path = os.path.join(tests_dir, map_file)
    print(f"Running {solver_class.__name__} algorithm on {map_file}...")
    os.makedirs(images_folder, exist_ok=True)
    current_map = Map.from_yaml(map_path)
    solver = solver_class(current_map)
    start_time = time.time()
    solution = solver.solve()
    end_time = time.time()
    if hasattr(solver, "states_built"):
        states_built = solver.states_built
    elif hasattr(current_map, "explored_states"):
        temp_map = current_map.copy()
        for move in solution or []:
            temp_map.apply_move(move)
        states_built = temp_map.explored_states
    else:
        states_built = len(solution) + 1 if solution else 1
    pull_moves = count_pull_moves(solution or [], current_map)
    print(f"Execution time: {end_time - start_time:.3f} seconds")
    print(f"States built: {states_built}")
    print(f"Number of pull moves: {pull_moves}")
    if solution:
        solution_map = current_map.copy()
        solution_steps = [solution_map.copy()]
        for move in solution:
            solution_map.apply_move(move)
            solution_steps.append(solution_map.copy())
        save_images(solution_steps, images_folder)
        gif_name = f"{current_map.test_name}_{gif_suffix}"
        create_gif(images_folder, gif_name, images_folder)
        gif_path = os.path.join(images_folder, f"{gif_name}.gif")
        print(f"GIF successfully created at: {gif_path}")
    else:
        print(f"No solution found for {map_file}")

if __name__ == "__main__":
    maps = [
        "easy_map1.yaml", "easy_map2.yaml",
        "medium_map1.yaml", "medium_map2.yaml",
        "large_map1.yaml", "large_map2.yaml",
        "hard_map1.yaml", "hard_map2.yaml",
        "super_hard_map1.yaml"
    ]
    
    for map_file in maps:
        run_and_save_gif(IDAStar, map_file, "images_ida_star", "ida_solution")
    for map_file in maps:
        run_and_save_gif(SimulatedAnnealing, map_file, "images_simulated_annealing", "sa_solution")