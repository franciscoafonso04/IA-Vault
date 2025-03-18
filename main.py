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
    "cooling_type": "exponential"
}

guests = file_handler.read_guest_preferences("guest_list.csv")
tables = seater.create_balanced_seating(guests, params["min_per_table"], params["max_per_table"])  
current_score = None
selected_index = 0 
input_text = ""


running = True
while running:
    screen.fill((255, 255, 255))  # Fill the screen with white

    # Draw the screen according to the current state
    if state == MENU:
        button1_rect, button2_rect = ui.draw_main_menu(screen, font)
    elif state == VIEW_PREFERENCES:
        back_button = ui.draw_table(screen, guests, font, row_height=40, col_widths=[200, 200, 200])
    elif state == VIEW_SEATING:
        back_button = ui.draw_seating_arrangement(screen, tables, font, score=current_score, guests=guests)
    elif state == PARAMETER_SELECTION:
        back_button, start_button = ui.draw_parameter_selection(screen, font, params, selected_index,input_text)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button in (4, 5):  # Mouse scroll wheel (scroll)
                if state == VIEW_PREFERENCES:
                    ui.handle_scroll_event(event, 'preferences')
                elif state == VIEW_SEATING:
                    ui.handle_scroll_event(event, 'seating')
            elif event.button == 1:  # Mouse click (button click)
                mouse_pos = event.pos
                if state == MENU:
                    if button1_rect.collidepoint(mouse_pos):
                        state = PARAMETER_SELECTION  # Transition to PARAMETER_SELECTION
                    elif button2_rect.collidepoint(mouse_pos):
                        state = VIEW_PREFERENCES  # Transition to VIEW_PREFERENCES
                elif state == PARAMETER_SELECTION:
                    if back_button.collidepoint(mouse_pos):
                        state = MENU  # Go back to MENU
                    elif start_button.collidepoint(mouse_pos):
                        try:
                            seater.validate_parameters(params,len(guests))
                            print("Starting simulated annealing with parameters:", params)
                            tables = seater.simulated_annealing(
                                guests=guests, 
                                initial_temperature=params["initial_temperature"], 
                                cooling_rate=params["cooling_rate"], 
                                iterations=params["iterations"],  
                                cooling_type=params["cooling_type"],
                                min_per_table=params["min_per_table"], 
                                max_per_table=params["max_per_table"]
                            )
                            current_score = -seater.calculate_cost(tables, guests)
                            state = VIEW_SEATING  # Go to the seating view after starting
                        except ValueError as e:
                            print(f"Invalid parameters: {e}")
                        except Exception as e:
                            print(f"Error during simulated annealing: {e}")
                elif state in (VIEW_PREFERENCES, VIEW_SEATING):
                    if back_button.collidepoint(mouse_pos):
                        state = MENU  # Back button to MENU

        elif event.type == pygame.KEYDOWN:
            if state == PARAMETER_SELECTION:  # When in the PARAMETER_SELECTION state
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(params)  # Cycle through parameters upwards
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(params)  # Cycle through parameters downwards
                elif event.key == pygame.K_RETURN:  # Enter key modifies selected parameter value
                    ui.handle_parameter_input(event, params, selected_index)  # Modify selected parameter value
                elif event.key == pygame.K_ESCAPE:  # Escape key to go back to the menu
                    state = MENU  # Exit parameter selection to the menu

    # Update the screen
    pygame.display.flip()

pygame.quit()
