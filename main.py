import pygame
import file_handler
import seater  # Make sure this import works correctly
import ui

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MENU, VIEW_PREFERENCES, VIEW_SEATING = "menu", "preferences", "seating"
state = MENU

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wedding Seater Planner")
font = pygame.font.Font(None, 28)  

guests = file_handler.read_guest_preferences("guest_list.csv")
# Use the new balanced seating creation
tables = seater.create_balanced_seating(guests)
current_score = None

# Loop principal
running = True
while running:
    screen.fill((255, 255, 255))  # Fundo branco
    
    # Draw current state and get button areas
    if state == MENU:
        button1_rect, button2_rect = ui.draw_main_menu(screen, font)
    elif state == VIEW_PREFERENCES:
        back_button = ui.draw_table(screen, guests, font, row_height=40, col_widths=[200, 200, 200])
    elif state == VIEW_SEATING:
        back_button = ui.draw_seating_arrangement(screen, tables, font, score=current_score, guests=guests)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # For scrolling
            if event.button in (4, 5):  # Wheel up (4) or down (5)
                if state == VIEW_PREFERENCES:
                    ui.handle_scroll_event(event, 'preferences')
                elif state == VIEW_SEATING:
                    ui.handle_scroll_event(event, 'seating')
            # For button clicks
            elif event.button == 1:  # Left click only
                mouse_pos = event.pos
                if state == MENU:
                    if button1_rect.collidepoint(mouse_pos):
                        try:
                            print("Starting simulated annealing...")
                            tables = seater.simulated_annealing(
                                guests=guests, 
                                initial_temperature=100, 
                                cooling_rate=0.95, 
                                iterations=1000  # Already 1000, no change needed
                            )
                            # Calculate score for display
                            current_score = -seater.calculate_cost(tables, guests)
                            state = VIEW_SEATING
                        except Exception as e:
                            print(f"Error during simulated annealing: {e}")
                    elif button2_rect.collidepoint(mouse_pos):
                        state = VIEW_PREFERENCES
                elif state in (VIEW_PREFERENCES, VIEW_SEATING):
                    # Fix potential issue with back_button check
                    try:
                        if back_button.collidepoint(mouse_pos):
                            state = MENU
                    except:
                        print("Back button error - returning to menu")
                        state = MENU

    pygame.display.flip()

pygame.quit()

