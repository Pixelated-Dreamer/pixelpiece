import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CARD_WIDTH = 300
CARD_HEIGHT = 400
CARD_SPACING = 50
SCROLL_SPEED = 10

# Colors
TWILIGHT_BLUE = (6, 0, 60)
DOCK_BROWN = (101, 67, 33)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CARD_BG = (210, 180, 140)
SHIP_COLOR = (139, 69, 19)

# Arcs data
ARCS = [
    {
        "name": "Marineford",
        "characters": ["Whitebeard", "Luffy", "Akainu"],
        "icon": "marine_flag.png"  # Placeholder
    },
    {
        "name": "Thriller Bark",
        "characters": ["Moria", "Luffy", "Brook"],
        "icon": "steering_wheel.png"  # Placeholder
    },
    {
        "name": "Enies Lobby",
        "characters": ["Luffy", "Lucci", "Zoro"],
        "icon": "world_government_flag.png" # Placeholder
    }
]

def run_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pixel Piece - Arc Select")
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    # Ship properties
    ship_x = SCREEN_WIDTH / 2
    ship_y = SCREEN_HEIGHT - 150
    ship_speed_x = random.uniform(-0.5, 0.5)
    ship_speed_y = random.uniform(-0.1, 0.1)

    # Card properties
    scroll_offset = 0
    target_scroll = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    target_scroll += SCROLL_SPEED * 5
                elif event.button == 5:  # Scroll down
                    target_scroll -= SCROLL_SPEED * 5

        # Smooth scrolling
        scroll_offset += (target_scroll - scroll_offset) * 0.1

        # Clamp scrolling
        max_scroll = (CARD_WIDTH + CARD_SPACING) * (len(ARCS) - 1)
        target_scroll = max(min(target_scroll, 0), -max_scroll)
        scroll_offset = max(min(scroll_offset, 0), -max_scroll)


        # Drawing background
        screen.fill(TWILIGHT_BLUE)
        pygame.draw.rect(screen, DOCK_BROWN, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))

        # Ship animation
        ship_x += ship_speed_x
        ship_y += ship_speed_y
        if ship_x < 0 or ship_x > SCREEN_WIDTH:
            ship_speed_x *= -1
        if ship_y < SCREEN_HEIGHT - 180 or ship_y > SCREEN_HEIGHT - 120:
            ship_speed_y *= -1

        # Draw ship (as a simple polygon)
        ship_points = [(ship_x, ship_y), (ship_x + 20, ship_y + 40), (ship_x - 20, ship_y + 40)]
        pygame.draw.polygon(screen, SHIP_COLOR, ship_points)
        pygame.draw.rect(screen, SHIP_COLOR, (ship_x - 5, ship_y - 30, 10, 30)) # Mast

        # Draw cards
        start_x = (SCREEN_WIDTH - CARD_WIDTH) / 2 + scroll_offset
        for i, arc in enumerate(ARCS):
            card_x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            card_rect = pygame.Rect(card_x, (SCREEN_HEIGHT - CARD_HEIGHT) / 2, CARD_WIDTH, CARD_HEIGHT)

            # Check if card is on screen before drawing
            if card_rect.right > 0 and card_rect.left < SCREEN_WIDTH:
                pygame.draw.rect(screen, CARD_BG, card_rect, border_radius=15)
                pygame.draw.rect(screen, BLACK, card_rect, 2, border_radius=15)

                # Arc Title
                title_text = font.render(arc["name"], True, BLACK)
                screen.blit(title_text, (card_x + 20, card_rect.y + 20))

                # Characters
                for j, char in enumerate(arc["characters"]):
                    char_text = small_font.render(char, True, BLACK)
                    screen.blit(char_text, (card_x + 20, card_rect.y + 70 + j * 30))

                # Icon (placeholder)
                icon_text = small_font.render(f"Icon: {arc['icon']}", True, BLACK)
                screen.blit(icon_text, (card_x + 20, card_rect.y + CARD_HEIGHT - 50))


        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    run_menu()
