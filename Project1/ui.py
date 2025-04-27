import pygame
import Project1.seater as seater

# Variáveis globais relacionadas a scrolling
SCROLL_SPEED = 15
scroll_offset = {'preferences': 0, 'seating': 0}


# Parâmetros usados nos algoritmos
parameters = {
    "min_per_table": 2,
    "max_per_table": 8,
    "initial_temperature": 100,
    "cooling_rate": 0.95,
    "iterations": 1000,
    "cooling_type": "exponential",
    "algorithm": "Simulated Annealing",
    "population_size": 100,
    "mutation_rate": 0.05
}

# Restrições de alguns dos parâmetros
MAX_INITIAL_TEMP = 100
MAX_ITERATIONS = 2000
MAX_COOLING_RATE = 1.0
COOLING_TYPES = ["exponential", "linear", "logarithmic"]

# ========================================================================================================================================================
# Função: draw_parameters_menu
# Descrição: Desenha o menu de parâmetros na janela o que permite ao utilizador visualizar e selecionar os parâmetros 
# que podem ser ajustados para a configuração da disposição das mesas.
# ========================================================================================================================================================
def draw_parameters_menu(screen, font, selected_index):
    screen.fill((240, 248, 255)) # Cor de fundo da janela

    title = font.render("Adjust Seating Parameters", True, (0, 0, 0)) # Título do menu
    screen.blit(title, (20, 20))

    labels = [
        "Min per Table", "Max per Table", "Initial Temperature",
        "Cooling Rate", "Iterations", "Cooling Type"
    ]
    
    y_offset = 80
    for i, (key, label) in enumerate(zip(parameters.keys(), labels)):
       # Destaca o parâmetro selecionado
        color = (0, 0, 255) if i == selected_index else (0, 0, 0)
        # Mostra o rótulo e o valor do parâmetro
        text = font.render(f"{label}: {parameters[key]}", True, color)
        screen.blit(text, (50, y_offset))
        y_offset += 40

    # Mensagem para confirmar com ENTER
    back_text = font.render("Press ENTER to Confirm", True, (255, 0, 0))
    screen.blit(back_text, (50, y_offset + 40))


# ========================================================================================================================================================
# Função: draw_parameter_selection
# Descrição: Gera uma interface interativa para a seleção e a personalização de parâmetros específicos de acordo com o algoritmo
# escolhido (Simulated Annealing, Genetic Algorithm ou Hill Climbing). Permite a navegação entre valores e a seleção
# através de botões incrementais, decrementais e menus suspensos.
# ========================================================================================================================================================
def draw_parameter_selection(screen, font, params):
    screen.fill((240, 248, 255)) # Cor de fundo da janela

     # Título do menu de parâmetros
    title = font.render("Adjust Seating Parameters", True, (0, 0, 0))
    screen.blit(title, (20, 20))
    y = 80
    buttons = [] # Lista de botões interativos

    # Define o tamanho, a altura e o espaço do botão 
    button_width = 120
    button_height = 40
    spacing = 10

    # Define os parâmetros por algoritmo
    algorithm_parameters = {
        "Simulated Annealing": [
            ("Min per Table", "min_per_table", 1, 10),
            ("Max per Table", "max_per_table", 1, 10),
            ("Initial Temp", "initial_temperature", 1, 1000),
            ("Cooling Rate", "cooling_rate", 0.01, 1.0),
            ("Iterations", "iterations", 100, 10000),
            ("Cooling Type", "cooling_type", None, None),
        ],
        "Genetic Algorithm": [
            ("Min per Table", "min_per_table", 1, 10),
            ("Max per Table", "max_per_table", 1, 10),
            ("Population Size", "population_size", 10, 500),
            ("Mutation Rate", "mutation_rate", 0.01, 1.0),
            ("Generations", "iterations", 100, 10000),
        ],
        "Hill Climbing": [
            ("Min per Table", "min_per_table", 1, 10),
            ("Max per Table", "max_per_table", 1, 10),
            ("Iterations", "iterations", 100, 10000)
        ]
    }

     # Seleciona o algoritmo
    algorithm_label = font.render("Algorithm:", True, (0, 0, 0))
    screen.blit(algorithm_label, (50, y))
    algorithm_rect = pygame.Rect(0, y, 210, 30)
    algorithm_rect.centerx = screen.get_width() // 2 + 50
    pygame.draw.rect(screen, (255, 255, 255), algorithm_rect)
    pygame.draw.rect(screen, (0, 0, 0), algorithm_rect, 2)
    algorithm_text = font.render(params["algorithm"], True, (0, 0, 0))
    screen.blit(algorithm_text, algorithm_text.get_rect(center=algorithm_rect.center))
    buttons.append((algorithm_rect, "algorithm", None))
    y += 50

    #  Parâmetros para o algoritmo selecionado
    selected_algorithm = params["algorithm"]
    param_defs = algorithm_parameters.get(selected_algorithm, [])

    center_x = screen.get_width() // 2 + 50

    for label, key, min_val, max_val in param_defs:
        screen.blit(font.render(f"{label}:", True, (0, 0, 0)), (50, y))

        value_rect = pygame.Rect(0, y, 150, 30)
        value_rect.centerx = center_x

        if key == "cooling_type":
            # Campo de seleção para o tipo de arrefecimento do  Simmulated Annealing
            pygame.draw.rect(screen, (255, 255, 255), value_rect)
            pygame.draw.rect(screen, (0, 0, 0), value_rect, 2)
            type_text = font.render(str(params.get(key, "")), True, (0, 0, 0))
            screen.blit(type_text, type_text.get_rect(center=value_rect.center))
            buttons.append((value_rect, key, "cycle"))
        else:
            # Campo de valor com botões + e -
            pygame.draw.rect(screen, (255, 255, 255), value_rect)
            pygame.draw.rect(screen, (0, 0, 0), value_rect, 2)
            value_text = font.render(str(params.get(key, "")), True, (0, 0, 0))
            screen.blit(value_text, value_text.get_rect(center=value_rect.center))

            # Botão de decremento (-)
            dec_button = pygame.Rect(value_rect.left - 50, y, 40, 30)
            pygame.draw.rect(screen,(100, 149, 237), dec_button, border_radius=5)
            minus_text = font.render("-", True, (0, 0, 0))
            screen.blit(minus_text, minus_text.get_rect(center=dec_button.center))
            buttons.append((dec_button, key, -1))

            # Botão de incremento (+)
            inc_button = pygame.Rect(value_rect.right + 10, value_rect.top, 40, 30)
            pygame.draw.rect(screen, (40, 167, 69), inc_button, border_radius=5)
            plus_text = font.render("+", True, (0, 0, 0))
            screen.blit(plus_text, plus_text.get_rect(center=inc_button.center))
            buttons.append((inc_button, key, 1))

        y += 50

    # Botões de navegação (Back, Start, Benchmark, Compare)
    y_button = y + 30
    total_buttons = 4
    total_width = total_buttons * button_width + (total_buttons - 1) * spacing
    start_x = (screen.get_width() - total_width) // 2

    colors = [(255, 59, 48)] + [(40, 167, 69)] * 3  
    texts = ["Back", "Start", "Benchmark", "Compare"]
    buttons_rects = []

    for i in range(total_buttons):
        x = start_x + i * (button_width + spacing)
        button = pygame.Rect(x, y_button, button_width, button_height)
        pygame.draw.rect(screen, colors[i], button, border_radius=10)
        text_color = (0, 0, 0) if i != 0 else (255, 255, 255)

        text_surface = font.render(texts[i], True, text_color)
        screen.blit(text_surface, text_surface.get_rect(center=button.center))
        buttons_rects.append(button)

    return buttons, *buttons_rects



# ========================================================================================================================================================
# Função: draw_table
# Descrição: Desenha uma tabela com os convidados e as respetivas pessoas que preferem estar na mesa ou evitar.
# Também possui botões de navegação para voltar ao menu inicial e para adicionar um convidado.
# ========================================================================================================================================================
def draw_table(screen, data, font, row_height, col_widths):
    global scroll_offset

    # Cabeçalhos da tabela
    headers = ['Guest', 'Prefers', 'Avoids']
    for col, header in enumerate(headers):
        pygame.draw.rect(screen, (100, 149, 237), (col * col_widths[col], 20, col_widths[col], row_height))
        text = font.render(header, True, (255, 255, 255))
        screen.blit(text, (col * col_widths[col] + 10, 30))

    # Início do conteúdo da tabela (com ajuste do scroll)
    y_offset = 60 - scroll_offset['preferences']
    for guest, preferences in data.items():
        # Nome do convidado
        pygame.draw.rect(screen, (255, 255, 255), (0, y_offset, col_widths[0], row_height))
        text = font.render(guest, True, (0, 0, 0))
        screen.blit(text, (10, y_offset + 10))

         # Preferências
        prefer_text = ', '.join(preferences['prefers']) if preferences['prefers'] else "None"
        pygame.draw.rect(screen, (255, 255, 255), (col_widths[0], y_offset, col_widths[1], row_height))
        screen.blit(font.render(prefer_text, True, (0, 0, 0)), (col_widths[0] + 10, y_offset + 10))

        # Pessoas a evitar
        avoid_text = ', '.join(preferences['avoids']) if preferences['avoids'] else "None"
        pygame.draw.rect(screen, (255, 255, 255), (col_widths[0] + col_widths[1], y_offset, col_widths[2], row_height))
        screen.blit(font.render(avoid_text, True, (0, 0, 0)), (col_widths[0] + col_widths[1] + 10, y_offset + 10))

        y_offset += row_height

   # Botão "Back"
    back_button = pygame.Rect(10, screen.get_height() - 60, 100, 40)
    pygame.draw.rect(screen, (200, 0, 0), back_button, border_radius=10)
    back_text = font.render('Back', True, (255, 255, 255))
    screen.blit(back_text, back_text.get_rect(center=back_button.center))

    # Botão "Add Guest"
    add_button = pygame.Rect(screen.get_width() - 130, screen.get_height() - 60, 120, 40)
    pygame.draw.rect(screen, (33, 150, 243), add_button, border_radius=10)
    add_text = font.render('Add Guest', True, (255, 255, 255))
    screen.blit(add_text, add_text.get_rect(center=add_button.center))

    return back_button, add_button


# ========================================================================================================================================================
# Função: draw_add_guest_menu
# Descrição: Desenha o formulário para adicionar o novo convidado, incluindo o nome, as preferências e as pessoas que prefere evitar.
# Para além disso também possui botões para salvar e para cancelar.
# ========================================================================================================================================================
def draw_add_guest_menu(screen, font, new_name, selected_prefers, selected_avoids, guests, name_active):
    width, height = screen.get_size()
    screen.fill((255, 255, 255)) # Cor de fundo da janela

    # Título do formulário
    title = font.render("Add New Guest", True, (0, 0, 0))
    screen.blit(title, (width // 2 - title.get_width() // 2, 20))

     # Caixa de input para o nome
    input_box = pygame.Rect(100, 80, 600, 40)
    pygame.draw.rect(screen, (0, 0, 0), input_box, 2)
    name_color = (0, 0, 0) if name_active else (150, 150, 150)
    screen.blit(font.render(new_name or "Enter guest name...", True, name_color), (input_box.x + 10, input_box.y + 10))

     # Instruções de uso
    instructions = font.render("Click to select 3 prefers (green) and 3 avoids (red)", True, (50, 50, 50))
    screen.blit(instructions, (100, 140))

    # Botões com os nomes dos convidados disponíveis
    guest_buttons = []
    y_offset = 180
    for name in guests:
        rect = pygame.Rect(100, y_offset, 600, 30)
        color = (200, 200, 200)
        if name in selected_prefers:
            color = (76, 175, 80)  # verde
        elif name in selected_avoids:
            color = (244, 67, 54)  # vermelho
        pygame.draw.rect(screen, color, rect)
        screen.blit(font.render(name, True, (0, 0, 0)), (rect.x + 10, rect.y + 5))
        guest_buttons.append((rect, name))
        y_offset += 40

   # Botão "Save"
    save_button = pygame.Rect(100, height - 60, 120, 40)
    pygame.draw.rect(screen, (33, 150, 243), save_button, border_radius=10)
    save_text = font.render("Save", True, (255, 255, 255))
    screen.blit(save_text, save_text.get_rect(center=save_button.center))

    # Botão "Cancel"
    cancel_button = pygame.Rect(width - 220, height - 60, 120, 40)
    pygame.draw.rect(screen, (200, 0, 0), cancel_button, border_radius=10)
    cancel_text = font.render("Cancel", True, (255, 255, 255))
    screen.blit(cancel_text, cancel_text.get_rect(center=cancel_button.center))


    return input_box, guest_buttons, save_button, cancel_button

# ========================================================================================================================================================
# Função: draw_main_menu
# Descrição: Desenha o menu principal com um título e botões para iniciar e visualizar preferências.
# ========================================================================================================================================================
def draw_main_menu(screen, font):
    # Fundo em degradê azul
    for y in range(screen.get_height()):
        color = (240 - y // 20, 248 - y // 30, 255 - y // 40)
        pygame.draw.line(screen, color, (0, y), (screen.get_width(), y))
    
    # Container central branco semi-transparente do Menu
    container_width = 400
    container_height = 350
    container_x = (screen.get_width() - container_width) // 2
    container_y = (screen.get_height() - container_height) // 2 - 30
    container_surface = pygame.Surface((container_width, container_height), pygame.SRCALPHA)
    pygame.draw.rect(container_surface, (255, 255, 255, 200), 
                    (0, 0, container_width, container_height), 
                    border_radius=20)
    screen.blit(container_surface, (container_x, container_y))
    
    # Título centralizado dentro do Container
    title_font = pygame.font.Font(None, 40)  # Fonte maior e mais elegante
    title_text = 'Wedding Seater Planner'
    title = title_font.render(title_text, True, (70, 100, 180))
    title_rect = title.get_rect(center=(container_x + container_width // 2, container_y + 45))
    screen.blit(title, title_rect)
    
    # Linha decorativa abaixo do título
    pygame.draw.line(screen, (200, 200, 220), (container_x + 50, container_y + 90), (container_x + container_width - 50, container_y + 90), 3)
    
    # Botões
    button_width = 320
    button_height = 60
    start_x = (screen.get_width() - button_width) // 2
    
    # Botão 1 - "Get Seating Arrangement"
    button_y = container_y + 130
    button1_rect = pygame.Rect(start_x, button_y, button_width, button_height)
    shadow_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, (0, 0, 0, 50), (0, 0, button_width, button_height), border_radius=15)
    
    # Sombra do botão
    screen.blit(shadow_surface, (start_x + 3, button_y + 3))
    button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    for y in range(button_height):
        color = (80 + y // 2, 180 + y // 3, 80 + y // 2, 255)
        pygame.draw.line(button_surface, color, (0, y), (button_width, y))
    
    pygame.draw.rect(button_surface, (0, 0, 0, 0),  (0, 0, button_width, button_height),  border_radius=15, width=2)
    screen.blit(button_surface, (start_x, button_y))
    
    # Texto do botão
    btn_text = font.render('Get Seating Arrangement', True, (255, 255, 255))
    btn_rect = btn_text.get_rect(center=(start_x + button_width // 2, button_y + button_height // 2))
    screen.blit(btn_text, btn_rect)
    
    # Botão 2 - "View Preferences Table"
    button_y = container_y + 210
    button2_rect = pygame.Rect(start_x, button_y, button_width, button_height)
    
    # Sombra do botão
    screen.blit(shadow_surface, (start_x + 3, button_y + 3))
    
    button_surface2 = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    for y in range(button_height):
        color = (80 + y // 2, 120 + y // 3, 210 + y // 2, 255)
        pygame.draw.line(button_surface2, color, (0, y), (button_width, y))
    
    pygame.draw.rect(button_surface2, (0, 0, 0, 0), 
                    (0, 0, button_width, button_height), 
                    border_radius=15, width=2)
    screen.blit(button_surface2, (start_x, button_y))
    
    # Texto do botão
    btn_text = font.render('View Preferences Table', True, (255, 255, 255))
    btn_rect = btn_text.get_rect(center=(start_x + button_width // 2, button_y + button_height // 2))
    screen.blit(btn_text, btn_rect)
    
    # Ícones decorativos (alianças)
    ring_x1 = container_x + 60
    ring_x2 = container_x + container_width - 60
    ring_y = container_y + 300
    
    # Anel esquerdo
    pygame.draw.circle(screen, (255, 215, 0), (ring_x1, ring_y), 15, width=3)
    # Anel direito
    pygame.draw.circle(screen, (255, 215, 0), (ring_x2, ring_y), 15, width=3)

    return button1_rect, button2_rect

# ========================================================================================================================================================
# Função: draw_seating_arrangement
# Descrição: Desenha a disposição das mesas e convidados, exibindo o título, a pontuação da disposição atual, pontuação teórica perfeita e 
# a percentagem de otimização. Também exibe os botões "Back" e "Retry".
# ========================================================================================================================================================
def draw_seating_arrangement(screen, tables, font, score=None, guests=None):
    screen.fill((240, 248, 255)) # Cor da Janela
    
    # Titulo
    title_text = 'Optimized Seating Arrangement' if score is not None else 'Random Seating Arrangement'
    title = font.render(title_text, True, (0, 0, 0))
    screen.blit(title, (20, 20))
    
    # Exibir pontuação se disponível
    if score is not None:
        #  Pontuação atual
        score_text = font.render(f'Score: {round(score,2)}', True, (0, 100, 0))
        screen.blit(score_text, (screen.get_width() - 300, 20))
        
        # Pontuação perfeita (ideal)
        perfect_score = calculate_perfect_score(tables, guests)
        perfect_text = font.render(f'Perfect Score: {perfect_score}', True, (100, 100, 100))
        screen.blit(perfect_text, (screen.get_width() - 300, 45))
        
        # Percentagem de quão próxima está do ideal
        if perfect_score > 0:  
            percentage = min(100, max(0, (score / perfect_score) * 100))
            percentage_text = font.render(f'Optimality: {percentage:.1f}%', True, (0, 0, 100))
            screen.blit(percentage_text, (screen.get_width() - 300, 70))
    
    # Desenha cada mesa e seus convidados
    y_offset = 80 - scroll_offset['seating']

    for i, table in enumerate(tables):
        # Título da mesa
        table_text = f"Table {i + 1}"
        text = font.render(table_text, True, (0, 0, 0))
        screen.blit(text, (20, y_offset))
        
        # Convidados nesta mesa
        for j, guest in enumerate(table):
            guest_text = font.render(f"  • {guest}", True, (0, 0, 0))
            screen.blit(guest_text, (40, y_offset + 30 + j * 25))
        
        # Atualizar o y_offset para a próxima mesa
        y_offset += 30 + len(table) * 25 + 20
    
    # Botão "Back"
    back_button = pygame.draw.rect(screen, (200, 0, 0), (10, screen.get_height() - 60, 100, 40), border_radius=10)
    text = font.render('Back', True, (255, 255, 255))
    text_rect = text.get_rect(center=(10 + 100 // 2, screen.get_height() - 40))
    screen.blit(text, text_rect)
    
    # Botão "Retry"
    retry_button = pygame.draw.rect(screen, (50, 205, 50), (120, screen.get_height() - 60, 100, 40), border_radius=10)
    text = font.render('Retry', True, (255, 255, 255))
    text_rect = text.get_rect(center=(120 + 100 // 2, screen.get_height() - 40))
    screen.blit(text, text_rect)
    
    return back_button, retry_button

# ========================================================================================================================================================
# Função: handle_scroll_event
# Descrição: Lida com eventos de scrolling do mouse para as janelas que possuem conteúdo com scroll (como "preferences" e "seating").
# ========================================================================================================================================================
def handle_scroll_event(event, current_state):
    if current_state in ['preferences', 'seating']:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll para cima
                scroll_offset[current_state] = max(0, scroll_offset[current_state] - SCROLL_SPEED)
            elif event.button == 5:  # Scroll para baixo
                scroll_offset[current_state] += SCROLL_SPEED

# ========================================================================================================================================================
# Função: calculate_perfect_score
# Descrição: Calcula a pontuação teórica perfeita — ou seja, a pontuação máxima que seria atingida se todos os convidados se sentassem exatamente com quem 
# preferem e evitassem quem não gostam. Pode usar uma estimativa aproximada ou uma versão precisa se os dados dos convidados forem fornecidos.
# ========================================================================================================================================================
def calculate_perfect_score(tables, guests=None):
    if guests is None:
        # Estimativa aproximada caso os dados não estejam disponíveis
        total_guests = sum(len(table) for table in tables)
        # Assume 3 preferências por convidado, 10 pontos cada
        return total_guests * 3 * 10
    else:        
        return seater.calculate_theoretical_perfect_score(guests)
