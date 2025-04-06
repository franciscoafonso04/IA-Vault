import pygame  
import file_handler
import seater
import ui
import os
import benchmark

pygame.init()

# Tamanho da janela
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Estados possíveis da interface
MENU, VIEW_PREFERENCES, VIEW_SEATING, PARAMETER_SELECTION, ADD_GUEST = "menu", "preferences", "seating", "parameters", "add_guest"

state = MENU    # Estado inicial é o menu principal

# Inicializar a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wedding Seater Planner")
font = pygame.font.Font(None, 28)

scroll_offset = {'preferences': 0, 'seating': 0}
new_guest_name = ""
selected_prefers = []
selected_avoids = []
input_active = False

# Parâmetros iniciais (default) do algoritmo
params = {
    "min_per_table": 3,
    "max_per_table": 8,
    "initial_temperature": 200,
    "cooling_rate": 0.98,
    "iterations": 2000,
    "mutation_rate": 0.01,
    "population_size": 50,
    "cooling_type": "exponential",  # Tipo de arrefecimento por default
    "algorithm": "Simulated Annealing"  # Algoritmo selecionado por default
}

# Ler os dados dos convidados
guests = file_handler.read_guest_preferences("guest_list.csv")

# Gerar uma disposição inicial aleatória e equilibrada
tables = seater.create_balanced_seating(guests, params["min_per_table"], params["max_per_table"])  

current_score = None  # Vai ser calculado após correr o algoritmo

running = True  # Controla o loop principal da aplicação

# Loop principal do jogo (Pygame)
while running:
    screen.fill((255, 255, 255))

    # Desenha o ecrã consoante o estado atual
    if state == MENU:
        button1_rect, button2_rect = ui.draw_main_menu(screen, font)
    elif state == VIEW_PREFERENCES:
        back_button, add_button = ui.draw_table(screen, guests, font, row_height=40, col_widths=[200, 200, 200])
    elif state == ADD_GUEST:
        input_box, guest_buttons, save_button, cancel_button = ui.draw_add_guest_menu(
            screen, font, new_guest_name, selected_prefers, selected_avoids, list(guests.keys()), input_active)
    elif state == VIEW_SEATING:
        back_button, retry_button = ui.draw_seating_arrangement(screen, tables, font, score=current_score, guests=guests)
    elif state == PARAMETER_SELECTION:
        param_buttons, back_button, start_button, benchmark_button, compare_button = ui.draw_parameter_selection(screen, font, params)

    # Processa os eventos do utilizador
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if state == ADD_GUEST and input_active:
                if event.key == pygame.K_BACKSPACE:
                    new_guest_name = new_guest_name[:-1]
                elif event.key == pygame.K_RETURN:
                    input_active = False
                else:
                    if len(new_guest_name) < 30:
                        new_guest_name += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5):  # Scroll wheel
                if state == VIEW_PREFERENCES:
                    ui.handle_scroll_event(event, 'preferences')
                elif state == VIEW_SEATING:
                    ui.handle_scroll_event(event, 'seating')
            if event.button == 1:  # Clique esquerdo
                mouse_pos = event.pos

                if state == MENU:
                    if button1_rect.collidepoint(mouse_pos):
                        state = PARAMETER_SELECTION
                    elif button2_rect.collidepoint(mouse_pos):
                        state = VIEW_PREFERENCES

                elif state == VIEW_PREFERENCES:
                    if back_button.collidepoint(mouse_pos):
                        state = MENU
                    elif add_button.collidepoint(mouse_pos):
                        new_guest_name = ""
                        selected_prefers = []
                        selected_avoids = []
                        input_active = True
                        state = ADD_GUEST

                elif state == ADD_GUEST:
                    if input_box.collidepoint(mouse_pos):
                        input_active = True
                    else:
                        input_active = False

                    for rect, name in guest_buttons:
                        if rect.collidepoint(mouse_pos):
                            if name in selected_prefers:
                                selected_prefers.remove(name)
                            elif name in selected_avoids:
                                selected_avoids.remove(name)
                            elif len(selected_prefers) < 3:
                                selected_prefers.append(name)
                            elif len(selected_avoids) < 3:
                                selected_avoids.append(name)

                    if save_button.collidepoint(mouse_pos):
                        if new_guest_name and new_guest_name not in guests and len(selected_prefers) <= 3 and len(selected_avoids) <= 3:
                            guests[new_guest_name] = {
                                "prefers": selected_prefers[:],
                                "avoids": selected_avoids[:]
                            }
                            state = VIEW_PREFERENCES

                    if cancel_button.collidepoint(mouse_pos):
                        state = VIEW_PREFERENCES

                elif state == VIEW_SEATING:
                    if back_button.collidepoint(mouse_pos):
                        state = MENU
                    elif retry_button.collidepoint(mouse_pos):
                        # Retry o algoritmo com os mesmos parâmetros
                        try:
                            seater.validate_parameters(params, len(guests))
                            output_folder = file_handler.generate_output_folder()
                            print("Retrying with parameters:", params)
                            if params["algorithm"] == "Simulated Annealing":
                                tables = seater.simulated_annealing(
                                    guests=guests,
                                    initial_temperature=params["initial_temperature"],
                                    cooling_rate=params["cooling_rate"],
                                    iterations=params["iterations"],
                                    cooling_type=params["cooling_type"],
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"],
                                    output_folder=output_folder
                                )
                            elif params["algorithm"] == "Genetic Algorithm":
                                
                                tables = seater.genetic_algorithm(
                                    guests=guests,
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"],
                                    population_size=params["population_size"],
                                    generations=params["iterations"],
                                    mutation_rate=params["mutation_rate"],
                                    output_folder=output_folder
                                )
                            elif params["algorithm"] == "Hill Climbing":
                                tables = seater.hill_climbing(
                                    guests=guests,
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"],
                                    iterations=params["iterations"],
                                    output_folder=output_folder
                                )

                            current_score = -seater.calculate_cost(tables, guests)
                            perfect_score = seater.calculate_theoretical_perfect_score(guests)
                            optimality = (current_score / perfect_score * 100) if perfect_score > 0 else 0

                            file_handler.write_seating_arrangement(
                                tables,
                                filename=os.path.join(output_folder, "seating.txt"),
                                current_score=current_score,
                                perfect_score=perfect_score,
                                optimality=optimality,
                                algorithm=params["algorithm"]
                            )
                        except Exception as e:
                            print(f"Error: {e}")

                elif state == PARAMETER_SELECTION:
                    if back_button.collidepoint(mouse_pos):
                        state = MENU
                    elif benchmark_button.collidepoint(mouse_pos):
                        try:
                            seater.validate_parameters(params, len(guests))
                            benchmark.run_benchmark(guests, params, params["algorithm"], n_runs=10)
                        except Exception as e:
                            print(f"Benchmark error: {e}")
                    elif compare_button.collidepoint(mouse_pos):
                        try:
                            seater.validate_parameters(params, len(guests))
                            algorithms_to_test = ["Simulated Annealing", "Genetic Algorithm", "Hill Climbing"]
                            benchmark.compare_algorithms(guests, algorithms_to_test, params, n_runs=10)
                        except Exception as e:
                            print(f"Erro ao comparar algoritmos: {e}")
                    elif start_button.collidepoint(mouse_pos):
                        try:
                            seater.validate_parameters(params, len(guests))
                            print("Starting with parameters:", params)
                            output_folder = file_handler.generate_output_folder()

                            if params["algorithm"] == "Simulated Annealing":
                                tables = seater.simulated_annealing(
                                    guests=guests,
                                    initial_temperature=params["initial_temperature"],
                                    cooling_rate=params["cooling_rate"],
                                    iterations=params["iterations"],
                                    cooling_type=params["cooling_type"],
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"],
                                    output_folder=output_folder
                                )
                            elif params["algorithm"] == "Genetic Algorithm":
                                tables = seater.genetic_algorithm(
                                    guests=guests,
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"],
                                    population_size=params["population_size"],
                                    generations=params["iterations"],
                                    mutation_rate=params["mutation_rate"],
                                    output_folder=output_folder
                                )
                            elif params["algorithm"] == "Hill Climbing":
                                tables = seater.hill_climbing(
                                    guests=guests,
                                    min_per_table=params["min_per_table"],
                                    max_per_table=params["max_per_table"],
                                    iterations=params["iterations"],
                                    output_folder=output_folder
                                )

                            current_score = -seater.calculate_cost(tables, guests)
                            perfect_score = seater.calculate_theoretical_perfect_score(guests)
                            optimality = (current_score / perfect_score * 100) if perfect_score > 0 else 0

                            file_handler.write_seating_arrangement(
                                tables,
                                filename=os.path.join(output_folder, "seating.txt"),
                                current_score=current_score,
                                perfect_score=perfect_score,
                                optimality=optimality,
                                algorithm=params["algorithm"]
                            )
                            state = VIEW_SEATING
                        except Exception as e:
                            print(f"Error: {e}")
                    else:
                        # Cliques nos botões dos parâmetros
                        for rect, key, operation in param_buttons:
                            if rect.collidepoint(mouse_pos):
                                if key == "cooling_type":
                                    types = ["exponential", "linear", "logarithmic"]
                                    idx = types.index(params[key])
                                    params[key] = types[(idx + 1) % len(types)]
                                elif key == "algorithm":
                                    algorithms = ["Simulated Annealing", "Genetic Algorithm", "Hill Climbing"]
                                    idx = algorithms.index(params[key])
                                    params[key] = algorithms[(idx + 1) % len(algorithms)]
                                else:
                                    step, min_val, max_val = {
                                        "min_per_table": (1, 1, 20),
                                        "max_per_table": (1, 1, 20),
                                        "initial_temperature": (10, 10, 1000),
                                        "cooling_rate": (0.005, 0.01, 1.0),
                                        "iterations": (100, 100, 10000),
                                        "mutation_rate": (0.01, 0.01, 1.0),
                                        "population_size": (10, 10, 500),
                                    }[key]
                                    new_value = round(params[key] + (operation * step), 3)
                                    params[key] = max(min(new_value, max_val), min_val)

    # Atualiza o ecrã
    pygame.display.flip()

# Termina a aplicação
pygame.quit()