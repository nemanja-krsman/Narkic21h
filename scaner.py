import pygame
import sys

pygame.init()

# Dimenzije prozora
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 680
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Klik na polja")

# Pozadina (tvoja mapa)
background = pygame.image.load("mapa3.jpg").convert()
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

font = pygame.font.SysFont(None, 24)

# Skladišti koordinate klikova
clicked_coords = []

# Glavna petlja
running = True
while running:
    screen.blit(background, (0, 0))

    # Crtamo brojeve na kliknuta mesta
    for idx, (x, y) in enumerate(clicked_coords):
        pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
        number = font.render(str(idx + 1), True, (255, 255, 0))
        screen.blit(number, (x + 5, y - 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            clicked_coords.append((x, y))
            print(f"{len(clicked_coords)}. ({x}, {y})")

    pygame.display.flip()

pygame.quit()

# Na kraju možeš ispisati sve klikove kao listu
print("Koordinate polja:")
for coord in clicked_coords:
    print(coord, end=", ")
