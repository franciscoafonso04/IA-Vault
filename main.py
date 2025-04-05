import pygame  
import file_handler
import seater
import ui

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MENU, VIEW_PREFERENCES, VIEW_SEATING, PARAMETER_SELECTION = "menu", "preferences", "seating", "parameters"
state = MENU

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wedding Seater Planner")
font = pygame.font.Font(None, 28)

# Default parameters
params = {
    "min_per_table": 2,
    "max_per_table": 8,
    "initial_temperature": 100,
    "cooling_rate": 0.95,
    "iterations": 1000,
    "mutation_rate": 0.01,
    "population_size": 50,
    "tabu_size": 10,
    "max_flips": 1000,
    "cooling_type": "exponential",
    "algorithm": "Simulated Annealing"
}

guests = file_handler.read_guest_preferences("guest_list.csv")
tables = seater.create_balanced_seating(guests, params["min_per_table"], params["max_per_table"])  
current_score = None

running = True



while running:
    screen.fill((255, 255, 255))

    # Draw the screen according to the current state
    if state == MENU:
        button1_rect, button2_rect = ui.draw_main_menu(screen, font)
    elif state == VIEW_PREFERENCES:
        back_button = ui.draw_table(screen, guests, font, row_height=40, col_widths=[200, 200, 200])
    elif state == VIEW_SEATING:
        back_button, retry_button = ui.draw_seating_arrangement(screen, tables, font, score=current_score, guests=guests)
    elif state == PARAMETER_SELECTION:
        selected_index = 0
        param_buttons, back_button, start_button, benchmark_button = ui.draw_parameter_selection(screen, font, params, selected_index)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5):  # Scroll wheel
                if state == VIEW_PREFERENCES:
                    ui.handle_scroll_event(event, 'preferences')
                elif state == VIEW_SEATING:
                    ui.handle_scroll_event(event, 'seating')
                    
            elif event.button == 1:  # Left click
                mouse_pos = event.pos
                
                if state == MENU:
                    if button1_rect.collidepoint(mouse_pos):
                        state = PARAMETER_SELECTION
                    elif button2_rect.collidepoint(mouse_pos):
                        state = VIEW_PREFERENCES
                        
                elif state == VIEW_PREFERENCES:
                    if back_button.collidepoint(mouse_pos):
                        state = MENU
                        
                elif state == VIEW_SEATING:
                    if back_button.collidepoint(mouse_pos):
                        state = MENU
                    elif retry_button.collidepoint(mouse_pos):
                        try:
                            seater.validate_parameters(params, len(guests))
                            print("Retrying with parameters:", params)
                            if params["algorithm"] == "Simulated Annealing":
                                tables = seater.simulated_annealing(
                                    guests=guests, 
                                    initial_temperature=params["initial_temperature"],
                                    cooling_rate=params["cooling_rate"],
                                    iterations=params["iterations"],
                                    cooling_type=params["cooling_type"],
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"]
                                )
                            elif params["algorithm"] == "CNF + WalkSAT":
                                tables = seater.cnf_walksat(
                                    guests=guests, 
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"],
                                    max_flips=params["max_flips"]
                                )
                            elif params["algorithm"] == "Tabu Search":
                                tables = seater.tabu_search(
                                    guests=guests, 
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"],
                                    tabu_size=params["tabu_size"],
                                    iterations=params["iterations"],
                                )
                            elif params["algorithm"] == "Genetic Algorithm":
                                tables = seater.genetic_algorithm(
                                    guests=guests, 
                                    min_per_table=params["min_per_table"],
                                    generations=params["iterations"],
                                    max_per_table=params["max_per_table"]
                                )
                            current_score = -seater.calculate_cost(tables, guests)
                            perfect_score = seater.calculate_theoretical_perfect_score(guests)
                            optimality = (current_score / perfect_score * 100) if perfect_score > 0 else 0
                            
                            # Save the seating arrangement with metrics
                            file_handler.write_seating_arrangement(
                                tables, 
                                current_score=current_score,
                                perfect_score=perfect_score,
                                optimality=optimality,
                                algorithm=params["algorithm"]  # Add this line
                            )
                        except Exception as e:
                            print(f"Error: {e}")
                        
                elif state == PARAMETER_SELECTION:
                    if back_button.collidepoint(mouse_pos):
                        state = MENU
                    elif benchmark_button.collidepoint(mouse_pos):
                        print("Benchmarking in progress...")
                        try:
                            seater.validate_parameters(params, len(guests))
                            from benchmark import run_benchmark  # se colocares isto num ficheiro benchmark.py
                            run_benchmark(guests, params, n_runs=10)
                        except Exception as e:
                            print(f"Benchmark error: {e}")
                    elif start_button.collidepoint(mouse_pos):
                        try:
                            seater.validate_parameters(params, len(guests))
                            print("Starting with parameters:", params)
                            if params["algorithm"] == "Simulated Annealing":
                                tables = seater.simulated_annealing(
                                    guests=guests, 
                                    initial_temperature=params["initial_temperature"],
                                    cooling_rate=params["cooling_rate"],
                                    iterations=params["iterations"],
                                    cooling_type=params["cooling_type"],
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"]
                                )
                            elif params["algorithm"] == "CNF + WalkSAT":
                                tables = seater.cnf_walksat(
                                    guests=guests, 
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"]
                                )
                            elif params["algorithm"] == "Tabu Search":
                                tables = seater.tabu_search(
                                    guests=guests, 
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"]
                                )
                            elif params["algorithm"] == "Genetic Algorithm":
                                tables = seater.genetic_algorithm(
                                    guests=guests, 
                                    min_per_table=params["min_per_table"],
                                    generations=params["iterations"],
                                    max_per_table=params["max_per_table"]
                                )
                            current_score = -seater.calculate_cost(tables, guests)
                            perfect_score = seater.calculate_theoretical_perfect_score(guests)
                            optimality = (current_score / perfect_score * 100) if perfect_score > 0 else 0
                            
                            # Save the seating arrangement with metrics
                            file_handler.write_seating_arrangement(
                                tables, 
                                current_score=current_score,
                                perfect_score=perfect_score,
                                optimality=optimality,
                                algorithm=params["algorithm"]  # Add this line
                            )
                            state = VIEW_SEATING
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        for btn in param_buttons:
                            rect, key, operation = btn
                            if rect.collidepoint(mouse_pos):
                                if key == "cooling_type":
                                    types = ["exponential", "linear", "logarithmic"]
                                    current_idx = types.index(params[key])
                                    params[key] = types[(current_idx + 1) % len(types)]
                                elif key == "algorithm":
                                    algorithms = ["Simulated Annealing", "CNF + WalkSAT", "Tabu Search", "Genetic Algorithm"]
                                    current_idx = algorithms.index(params[key])
                                    params[key] = algorithms[(current_idx + 1) % len(algorithms)]
                                else:
                                    steps = {
                                        "min_per_table": (1, 1, 20),
                                        "max_per_table": (1, 1, 20),
                                        "initial_temperature": (10, 10, 1000),
                                        "cooling_rate": (0.005, 0.01, 1.0),
                                        "iterations": (100, 100, 10000),
                                        "mutation_rate": (0.01, 0.01, 1.0), 
                                        "population_size": (10, 10, 500),  
                                        "tabu_size": (1, 1, 50),        
                                        "max_flips": (100, 100, 10000),   
                                    }
                                    step, min_val, max_val = steps[key]
                                    new_value = round(params[key] + (operation * step), 3)
                                    params[key] = max(min(new_value, max_val), min_val)
    pygame.display.flip()

pygame.quit()