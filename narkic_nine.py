import pygame
import sys
import math
import random

pygame.init()

CHARACTER_WIDTH = 25
CHARACTER_HEIGHT = 25
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 680
SIDE_PANEL_WIDTH = 200

screen = pygame.display.set_mode((WINDOW_WIDTH + SIDE_PANEL_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mapa Igre")
clock = pygame.time.Clock()

original_background = pygame.image.load("mapa3.jpg").convert()
background = pygame.transform.scale(original_background, (WINDOW_WIDTH, WINDOW_HEIGHT))

font_small = pygame.font.SysFont(None, 24)
font_large = pygame.font.SysFont(None, 36)

class Hero:
    def __init__(self, name, image, startpos, team):
        self.name = name
        self.image = pygame.transform.scale(pygame.image.load(image).convert(), (CHARACTER_WIDTH, CHARACTER_HEIGHT))
        self.startpos = startpos
        self.currentpos = startpos[:]
        self.drawpos = startpos[:]
        self.selected = False
        self.team = team
        self.attak = 0
        self.defense = 0
        self.speed = 0
        self.dice = 0
        self.offset_applied = False

    def draw(self, surface):
        surface.blit(self.image, self.drawpos)
        if self.selected:
            image_rect = self.image.get_rect(topleft=self.drawpos)
            pygame.draw.rect(surface, (0, 0, 255), image_rect, 3)

characters = [
    Hero("Rajic", "Rajic.jpg", [30, 100], 0),
    Hero("Krsman", "Krsman.jpg", [30, 180], 1),
    Hero("Persic", "Persic.jpg", [30, 220], 1),
    Hero("Maja", "Maja.jpg", [30, 260], 1),
    Hero("Branka", "Branka.jpg", [30, 300], 1),
    Hero("Mitke", "Mitke.jpg", [30, 380], 2),
    Hero("Gomke", "Gomke.jpg", [30, 420], 2),
    Hero("Geci", "Geci.jpg", [30, 460], 2),
    Hero("Baler", "Baler.jpg", [30, 500], 2),
]

# Podešavanje statova
characters[1].attak = 1; characters[1].defense = 2
characters[5].attak = 1; characters[5].defense = 2
characters[2].attak = -1; characters[2].defense = 3
characters[6].attak = -1; characters[6].defense = 3
characters[3].attak = 0; characters[3].defense = 0
characters[7].attak = 0; characters[7].defense = 0
characters[4].attak = 1; characters[4].defense = 1
characters[8].attak = 1; characters[8].defense = 1

valid_fields = [
(87, 666), (191, 665), (291, 664), (390, 663), (88, 631), (190, 628), (290, 628), (391, 629),
(87, 599), (189, 598), (290, 598), (393, 599), (86, 562), (191, 562), (292, 560), (394, 563),
(87, 527), (123, 528), (154, 528), (196, 529), (227, 527), (258, 528), (290, 528), (326, 527),
(358, 525), (393, 524), (107, 493), (175, 494), (306, 494), (378, 491), (139, 460), (345, 457),
(137, 425), (345, 421), (158, 388), (329, 391), (191, 361), (295, 361), (220, 328), (269, 325),
(240, 294), (246, 261), (219, 228), (265, 226), (188, 192), (296, 190), (174, 160), (312, 159),
(176, 126), (315, 127), (198, 94), (299, 94), (249, 59), (246, 16)
]
kafici_fields = [(123, 528), (157, 528), (327, 531), (357, 527)]

dice_result = None

def closest_field(pos, fields):
    x, y = pos
    return min(fields, key=lambda f: math.hypot(f[0] - x, f[1] - y))

def draw_button():
    pygame.draw.rect(screen, (255, 255, 255), (30, 30, 100, 40))
    pygame.draw.rect(screen, (0, 0, 0), (30, 30, 100, 40), 2)
    text = font_small.render("BACI", True, (0, 0, 0))
    screen.blit(text, (60, 40))

def draw_dice_result(result):
    text = font_large.render(f"Rezultat: {result}", True, (0, 0, 0))
    screen.blit(text, (30, 80))

def animate_dice_roll(hero, is_attacker, y_offset):
    for _ in range(10):
        roll = random.randint(1, 6)
        screen.fill((200, 200, 200), (0, 500 + y_offset, SIDE_PANEL_WIDTH, 100))
        pygame.draw.rect(screen, (255, 255, 255), (10, 500 + y_offset, SIDE_PANEL_WIDTH - 20, 90))
        label = "Napada!" if is_attacker else "Brani se!"
        screen.blit(font_small.render(f"{hero.name} {label}", True, (0, 0, 0)), (20, 510 + y_offset))
        screen.blit(font_large.render(str(roll), True, (0, 0, 0)), (20, 540 + y_offset))
        pygame.display.flip()
        pygame.time.delay(100)
    return roll

def show_final_score(hero, roll, bonus, y_offset):
    total = roll + bonus
    screen.fill((200, 200, 200), (0, 500 + y_offset, SIDE_PANEL_WIDTH, 100))
    pygame.draw.rect(screen, (255, 255, 255), (10, 500 + y_offset, SIDE_PANEL_WIDTH - 20, 90))
    screen.blit(font_small.render(f"{hero.name} rezultat:", True, (0, 0, 0)), (20, 510 + y_offset))
    screen.blit(font_large.render(f"{roll} + {bonus} = {total}", True, (0, 0, 0)), (20, 540 + y_offset))
    pygame.display.flip()
    pygame.time.delay(1000)
    return total

def wait_for_kafic_click():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for kafic in kafici_fields:
                    kafic_rect = pygame.Rect(
                        kafic[0] + SIDE_PANEL_WIDTH - CHARACTER_WIDTH // 2,
                        kafic[1] - CHARACTER_HEIGHT // 2,
                        CHARACTER_WIDTH,
                        CHARACTER_HEIGHT
                    )
                    if kafic_rect.collidepoint(mouse_x, mouse_y):
                        return kafic
        pygame.display.flip()
        clock.tick(60)

def process_battle(hero1, hero2):
    if tuple(hero1.currentpos) in kafici_fields:
        print("Borba se ne odvija u kaficima!")
        return

    print("Borba!")

    while True:
        attacker = hero1 if hero1.selected else hero2
        defender = hero2 if hero1.selected else hero1

        atk_roll = animate_dice_roll(attacker, True, 0)
        atk_total = show_final_score(attacker, atk_roll, attacker.attak, 0)

        def_roll = animate_dice_roll(defender, False, 110)
        def_total = show_final_score(defender, def_roll, defender.defense, 110)

        if atk_total != def_total:
            break

    loser = attacker if atk_total < def_total else defender
    print(f"{loser.name} je izgubio! Klikni na kafic da ga pošalješ tamo.")

    kafic_pos = wait_for_kafic_click()
    loser.drawpos = [kafic_pos[0] + SIDE_PANEL_WIDTH - CHARACTER_WIDTH // 2,
                     kafic_pos[1] - CHARACTER_HEIGHT // 2]
    loser.currentpos = kafic_pos[:]
    loser.offset_applied = False

while True:
    screen.fill((200, 200, 200))
    screen.blit(background, (SIDE_PANEL_WIDTH, 0))

    for char in characters:
        char.draw(screen)

    draw_button()
    if dice_result is not None:
        draw_dice_result(dice_result)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            najblize = closest_field((mouse_x - SIDE_PANEL_WIDTH, mouse_y), valid_fields)

            for char in characters:
                if char.selected:
                    if (mouse_x >= char.drawpos[0] and mouse_x <= char.drawpos[0] + CHARACTER_WIDTH and
                        mouse_y >= char.drawpos[1] and mouse_y <= char.drawpos[1] + CHARACTER_HEIGHT):
                        char.selected = False
                        print(f"{char.name} vise nije selektovan!")
                    else:
                        char.drawpos = [najblize[0] + SIDE_PANEL_WIDTH - CHARACTER_WIDTH // 2,
                                        najblize[1] - CHARACTER_HEIGHT // 2]
                        char.currentpos = najblize[:]
                        char.offset_applied = False
                        print(f"{char.name} se pomera")
                    break
            else:
                for char in characters:
                    if (mouse_x >= char.drawpos[0] and mouse_x <= char.drawpos[0] + CHARACTER_WIDTH and
                        mouse_y >= char.drawpos[1] and mouse_y <= char.drawpos[1] + CHARACTER_HEIGHT):
                        char.selected = True
                        print(f"Selektovan {char.name}!")
                        break

            for i, hero1 in enumerate(characters):
                for j, hero2 in enumerate(characters):
                    if i >= j:
                        continue
                    if (hero1.currentpos == hero2.currentpos and
                        hero1.team != hero2.team and
                        tuple(hero1.currentpos) not in kafici_fields):
                        process_battle(hero1, hero2)
                    elif (hero1.currentpos == hero2.currentpos and
                          hero1.team == hero2.team and
                          not hero1.offset_applied and
                          not hero2.offset_applied):
                        hero1.drawpos[0] -= CHARACTER_WIDTH // 2
                        hero2.drawpos[0] += CHARACTER_WIDTH // 2
                        hero1.offset_applied = True
                        hero2.offset_applied = True

    pygame.display.flip()
    clock.tick(60)
