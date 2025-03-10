import pygame
import file_handler
import seater
import ui

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
MENU, VIEW_PREFERENCES, VIEW_SEATING = "menu", "preferences", "seating"
state = MENU

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wedding Seater Planner")
font = pygame.font.Font(None, 28)  

guests = file_handler.read_guest_preferences("IA-Vault/guest_list.csv")
tables = seater.create_random_seating(guests)

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
        back_button = ui.draw_seating_arrangement(screen, tables, font)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if state == MENU:
                if button1_rect.collidepoint(mouse_pos):
                    tables = seater.create_random_seating(guests)
                    state = VIEW_SEATING
                elif button2_rect.collidepoint(mouse_pos):
                    state = VIEW_PREFERENCES
            elif state in (VIEW_PREFERENCES, VIEW_SEATING):
                if back_button.collidepoint(mouse_pos):
                    state = MENU

    pygame.display.flip()

pygame.quit()

