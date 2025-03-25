import pygame

# Add these global variables for scrolling
SCROLL_SPEED = 15
scroll_offset = {'preferences': 0, 'seating': 0}

# Define constraints
MAX_INITIAL_TEMP = 100
MAX_ITERATIONS = 2000
MAX_COOLING_RATE = 1.0
COOLING_TYPES = ["exponential", "linear", "logarithmic"]

# Default parameters
parameters = {
    "min_per_table": 2,
    "max_per_table": 8,
    "initial_temperature": 100,
    "cooling_rate": 0.95,
    "iterations": 1000,
    "cooling_type": "exponential"
}

def draw_parameters_menu(screen, font, selected_index):
    screen.fill((240, 248, 255))

    title = font.render("Adjust Seating Parameters", True, (0, 0, 0))
    screen.blit(title, (20, 20))

    labels = [
        "Min per Table", "Max per Table", "Initial Temperature",
        "Cooling Rate", "Iterations", "Cooling Type"
    ]
    
    y_offset = 80
    for i, (key, label) in enumerate(zip(parameters.keys(), labels)):
        # Highlight the selected parameter
        color = (0, 0, 255) if i == selected_index else (0, 0, 0)
        # Display the parameter label and value
        text = font.render(f"{label}: {parameters[key]}", True, color)
        screen.blit(text, (50, y_offset))
        y_offset += 40

    back_text = font.render("Press ENTER to Confirm", True, (255, 0, 0))
    screen.blit(back_text, (50, y_offset + 40))


def handle_parameters_input(event, selected_index):
    key = list(parameters.keys())[selected_index]  # Get the selected parameter key

    if event.type == pygame.KEYDOWN:
        if key in ["min_per_table", "max_per_table", "iterations"]:
            if event.key == pygame.K_UP:
                # Ensure "iterations" does not exceed its max, and "min_per_table" and "max_per_table" have reasonable limits
                if key == "iterations":
                    parameters[key] = min(parameters[key] + 100, MAX_ITERATIONS)
                else:
                    parameters[key] = min(parameters[key] + 1, 20 if key == "max_per_table" else 8)
            elif event.key == pygame.K_DOWN:
                if key == "iterations":
                    parameters[key] = max(parameters[key] - 100, 100)
                else:
                    parameters[key] = max(parameters[key] - 1, 1)
        elif key == "initial_temperature":
            if event.key == pygame.K_UP:
                parameters[key] = min(parameters[key] + 1, MAX_INITIAL_TEMP)
            elif event.key == pygame.K_DOWN:
                parameters[key] = max(parameters[key] - 1, 1)
        elif key == "cooling_rate":
            if event.key == pygame.K_UP:
                parameters[key] = min(parameters[key] + 0.01, MAX_COOLING_RATE)
            elif event.key == pygame.K_DOWN:
                parameters[key] = max(parameters[key] - 0.01, 0.01)
        elif key == "cooling_type":
            index = COOLING_TYPES.index(parameters[key])
            if event.key == pygame.K_UP:
                parameters[key] = COOLING_TYPES[(index - 1) % len(COOLING_TYPES)]
            elif event.key == pygame.K_DOWN:
                parameters[key] = COOLING_TYPES[(index + 1) % len(COOLING_TYPES)]


def draw_parameter_selection(screen, font, params, selected_index):
    screen.fill((240, 248, 255))
    title = font.render("Adjust Seating Parameters", True, (0, 0, 0))
    screen.blit(title, (20, 20))

    y = 80
    buttons = []
    
    # Configurações para cada parâmetro
    parameters = [
        ("Min per Table", "min_per_table", 1, 20),
        ("Max per Table", "max_per_table", 1, 20),
        ("Initial Temperature", "initial_temperature", 1, 1000),
        ("Cooling Rate", "cooling_rate", 0.01, 1.0),
        ("Iterations", "iterations", 100, 10000),
        ("Cooling Type", "cooling_type", None, None)
    ]

    for idx, (label, key, min_val, max_val) in enumerate(parameters):
        # Desenha o rótulo
        text = font.render(f"{label}:", True, (0, 0, 0))
        screen.blit(text, (50, y))

        # Desenha o valor atual
        value_rect = pygame.Rect(250, y, 150, 30)
        pygame.draw.rect(screen, (255, 255, 255), value_rect)
        pygame.draw.rect(screen, (0, 0, 0), value_rect, 2)
        
        value_text = font.render(str(params[key]), True, (0, 0, 0))
        screen.blit(value_text, (260, y + 5))

        # Botões de incremento/decremento para valores numéricos
        if key != "cooling_type":
            dec_button = pygame.draw.rect(screen, (200, 200, 200), (200, y, 40, 30))
            dec_text = font.render("-", True, (0, 0, 0))
            screen.blit(dec_text, (212, y))

            inc_button = pygame.draw.rect(screen, (200, 200, 200), (410, y, 40, 30))
            inc_text = font.render("+", True, (0, 0, 0))
            screen.blit(inc_text, (422, y))

            buttons.append((dec_button, key, -1))
            buttons.append((inc_button, key, 1))
        else:
            # Botão de alternância para cooling type
            cycle_button = pygame.draw.rect(screen, (200, 200, 200), (200, y, 250, 30))
            current_type = params[key]
            type_text = font.render(f"{current_type}", True, (0, 0, 0))
            screen.blit(type_text, (210, y))
            buttons.append((cycle_button, key, None))

        y += 50

    # Botões de navegação
    back_button = pygame.draw.rect(screen, (255, 99, 71), (50, y + 20, 100, 40))
    start_button = pygame.draw.rect(screen, (50, 205, 50), (screen.get_width()-150, y + 20, 100, 40))
    
    screen.blit(font.render("Back", True, (255, 255, 255)), (70, y + 30))
    screen.blit(font.render("Start", True, (255, 255, 255)), (screen.get_width()-130, y + 30))

    return buttons, back_button, start_button

def handle_parameter_input(event, params, selected_index):
    key = list(params.keys())[selected_index]

    if event.key == pygame.K_UP:
        if key == "iterations":
            params[key] = min(params[key] + 10, 2000)
        elif key == "cooling_rate":
            params[key] = min(params[key] + 0.01, 1.0)
        elif key == "initial_temperature":
            params[key] = min(params[key] + 1, 100)
        elif key in ["min_per_table", "max_per_table"]:
            params[key] = min(params[key] + 1, 20)
    elif event.key == pygame.K_DOWN:
        if key == "iterations":
            params[key] = max(params[key] - 10, 100)
        elif key == "cooling_rate":
            params[key] = max(params[key] - 0.01, 0.01)
        elif key == "initial_temperature":
            params[key] = max(params[key] - 1, 1)
        elif key in ["min_per_table", "max_per_table"]:
            params[key] = max(params[key] - 1, 1)
    elif event.key == pygame.K_LEFT:
        if key == "cooling_rate":
            params[key] = max(params[key] - 0.01, 0.01)
    elif event.key == pygame.K_RIGHT:
        if key == "cooling_rate":
            params[key] = min(params[key] + 0.01, 1.0)
    elif event.key == pygame.K_1:
        if key == "cooling_type":
            params[key] = "exponential"
    elif event.key == pygame.K_2:
        if key == "cooling_type":
            params[key] = "linear"
    elif event.key == pygame.K_3:
        if key == "cooling_type":
            params[key] = "logarithmic"



# Função para desenhar a tabela no Pygame
def draw_table(screen, data, font, row_height, col_widths):
    # Título das colunas
    headers = ['Guest', 'Prefers', 'Avoids']
    for col, header in enumerate(headers):
        pygame.draw.rect(screen, (100, 149, 237), (col * col_widths[col], 20, col_widths[col], row_height))  # Azul suave
        text = font.render(header, True, (255, 255, 255))
        screen.blit(text, (col * col_widths[col] + 10, 20 + 10))  # Texto branco
    
    # Preencher com os dados
    y_offset = 60 - scroll_offset['preferences'] # Começar um pouco abaixo do título
    for guest, preferences in data.items():
        # Desenhar o nome do convidado
        pygame.draw.rect(screen, (255, 255, 255), (0, y_offset, col_widths[0], row_height))
        text = font.render(guest, True, (0, 0, 0))
        screen.blit(text, (10, y_offset + 10))
        
        # Desenhar as preferências
        prefer_text = ', '.join(preferences['prefers']) if preferences['prefers'] else "None"
        pygame.draw.rect(screen, (255, 255, 255), (col_widths[0], y_offset, col_widths[1], row_height))
        text = font.render(prefer_text, True, (0, 0, 0))
        screen.blit(text, (col_widths[0] + 10, y_offset + 10))
        
        # Desenhar as evitações
        avoid_text = ', '.join(preferences['avoids']) if preferences['avoids'] else "None"
        pygame.draw.rect(screen, (255, 255, 255), (col_widths[0] + col_widths[1], y_offset, col_widths[2], row_height))
        text = font.render(avoid_text, True, (0, 0, 0))
        screen.blit(text, (col_widths[0] + col_widths[1] + 10, y_offset + 10))
        
        y_offset += row_height

    # Draw and return back button
    back_button = pygame.draw.rect(screen, (255, 99, 71), 
                                 (10, screen.get_height() - 60, 100, 40), 
                                 border_radius=10)
    text = font.render('Back', True, (255, 255, 255))
    text_rect = text.get_rect(center=(10 + 100 // 2, screen.get_height() - 40))
    screen.blit(text, text_rect)
    
    return back_button

# Função para desenhar o menu principal
def draw_main_menu(screen, font):
    # Create a gradient background
    for y in range(screen.get_height()):
        # Gradient from light blue to slightly darker blue
        color = (240 - y // 20, 248 - y // 30, 255 - y // 40)
        pygame.draw.line(screen, color, (0, y), (screen.get_width(), y))
    
    # Menu container
    container_width = 400
    container_height = 350
    container_x = (screen.get_width() - container_width) // 2
    container_y = (screen.get_height() - container_height) // 2 - 30
    
    # Draw a semi-transparent rounded container
    container_surface = pygame.Surface((container_width, container_height), pygame.SRCALPHA)
    pygame.draw.rect(container_surface, (255, 255, 255, 200), 
                    (0, 0, container_width, container_height), 
                    border_radius=20)
    screen.blit(container_surface, (container_x, container_y))
    
    # Title styling - CORRIGIDO: posicionado dentro do container
    title_font = pygame.font.Font(None, 40)  # Fonte maior e mais elegante
    title_text = 'Wedding Seater Planner'
    title = title_font.render(title_text, True, (70, 100, 180))
    # Ajustado para ficar dentro do container
    title_rect = title.get_rect(center=(container_x + container_width // 2, container_y + 45))
    screen.blit(title, title_rect)
    
    # Decorative divider
    pygame.draw.line(screen, (200, 200, 220), 
                    (container_x + 50, container_y + 90), 
                    (container_x + container_width - 50, container_y + 90), 
                    3)
    
    # Button styling
    button_width = 320
    button_height = 60
    start_x = (screen.get_width() - button_width) // 2
    
    # First button - Get Best Seating
    button_y = container_y + 130
    button1_rect = pygame.Rect(start_x, button_y, button_width, button_height)
    
    # Button shadow effect
    shadow_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surface, (0, 0, 0, 50), 
                    (0, 0, button_width, button_height), 
                    border_radius=15)
    screen.blit(shadow_surface, (start_x + 3, button_y + 3))
    
    # Actual button with gradient
    button_surface = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    for y in range(button_height):
        # Gradient from darker to lighter green
        color = (80 + y // 2, 180 + y // 3, 80 + y // 2, 255)
        pygame.draw.line(button_surface, color, (0, y), (button_width, y))
    
    pygame.draw.rect(button_surface, (0, 0, 0, 0), 
                    (0, 0, button_width, button_height), 
                    border_radius=15, width=2)
    screen.blit(button_surface, (start_x, button_y))
    
    # Button text
    btn_text = font.render('Get Seating Arrangement', True, (255, 255, 255))
    btn_rect = btn_text.get_rect(center=(start_x + button_width // 2, button_y + button_height // 2))
    screen.blit(btn_text, btn_rect)
    
    # Second button - View Preferences
    button_y = container_y + 210
    button2_rect = pygame.Rect(start_x, button_y, button_width, button_height)
    
    # Button shadow
    screen.blit(shadow_surface, (start_x + 3, button_y + 3))
    
    # Actual button with gradient
    button_surface2 = pygame.Surface((button_width, button_height), pygame.SRCALPHA)
    for y in range(button_height):
        # Gradient from darker to lighter blue
        color = (80 + y // 2, 120 + y // 3, 210 + y // 2, 255)
        pygame.draw.line(button_surface2, color, (0, y), (button_width, y))
    
    pygame.draw.rect(button_surface2, (0, 0, 0, 0), 
                    (0, 0, button_width, button_height), 
                    border_radius=15, width=2)
    screen.blit(button_surface2, (start_x, button_y))
    
    # Button text
    btn_text = font.render('View Preferences Table', True, (255, 255, 255))
    btn_rect = btn_text.get_rect(center=(start_x + button_width // 2, button_y + button_height // 2))
    screen.blit(btn_text, btn_rect)
    
    # Add decorative wedding icons
    # Simple ring icons (circles)
    ring_x1 = container_x + 60
    ring_x2 = container_x + container_width - 60
    ring_y = container_y + 300
    
    # Left ring
    pygame.draw.circle(screen, (255, 215, 0), (ring_x1, ring_y), 15, width=3)
    # Right ring
    pygame.draw.circle(screen, (255, 215, 0), (ring_x2, ring_y), 15, width=3)
    
    # Return button information for click detection
    return button1_rect, button2_rect

def draw_seating_arrangement(screen, tables, font, score=None, guests=None):
    screen.fill((240, 248, 255))
    
    # Draw title
    title_text = 'Optimized Seating Arrangement' if score is not None else 'Random Seating Arrangement'
    title = font.render(title_text, True, (0, 0, 0))
    screen.blit(title, (20, 20))
    
    # Display the score if available
    if score is not None:
        # Display current score
        score_text = font.render(f'Current Score: {score}', True, (0, 100, 0))
        screen.blit(score_text, (screen.get_width() - 300, 20))
        
        # Calculate and display theoretical perfect score
        perfect_score = calculate_perfect_score(tables, guests)
        perfect_text = font.render(f'Perfect Score: {perfect_score}', True, (100, 100, 100))
        screen.blit(perfect_text, (screen.get_width() - 300, 45))
        
        # Display percentage of optimal
        if perfect_score > 0:  # Avoid division by zero
            percentage = min(100, max(0, (score / perfect_score) * 100))
            percentage_text = font.render(f'Optimality: {percentage:.1f}%', True, (0, 0, 100))
            screen.blit(percentage_text, (screen.get_width() - 300, 70))
    
    # Draw tables
    y_offset = 80 - scroll_offset['seating']

    for i, table in enumerate(tables):
        # Draw table header
        table_text = f"Table {i + 1}"
        text = font.render(table_text, True, (0, 0, 0))
        screen.blit(text, (20, y_offset))
        
        # Draw guests at this table
        for j, guest in enumerate(table):
            guest_text = font.render(f"  • {guest}", True, (0, 0, 0))
            screen.blit(guest_text, (40, y_offset + 30 + j * 25))
        
        y_offset += 30 + len(table) * 25 + 20
    
    # Draw and return back button - FIXED: removed the trailing comma
    back_button = pygame.draw.rect(screen, (255, 99, 71), (10, screen.get_height() - 60, 100, 40), border_radius=10)
    text = font.render('Back', True, (255, 255, 255))
    text_rect = text.get_rect(center=(10 + 100 // 2, screen.get_height() - 40))
    screen.blit(text, text_rect)
    
    return back_button

# Add this function to handle scrolling events
def handle_scroll_event(event, current_state):
    if current_state in ['preferences', 'seating']:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                scroll_offset[current_state] = max(0, scroll_offset[current_state] - SCROLL_SPEED)
            elif event.button == 5:  # Scroll down
                scroll_offset[current_state] += SCROLL_SPEED

# Fix the helper function that calculates the theoretical perfect score
def calculate_perfect_score(tables, guests=None):
    """
    Calculate what the score would be if everyone sat with all their preferred
    people and away from all their avoided people.
    
    This is a theoretical maximum that may not be achievable in practice.
    """
    if guests is None:
        # If guests data isn't provided, make a rough estimate
        total_guests = sum(len(table) for table in tables)
        # Assuming each guest has on average 3 preferred people
        return total_guests * 3 * 10
    else:
        # Use the more accurate calculation from seater
        from seater import calculate_theoretical_perfect_score
        return calculate_theoretical_perfect_score(guests)
