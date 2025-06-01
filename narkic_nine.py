import pygame
import sys
import math
import random

pygame.init()

CHARACTER_WIDTH = 25
CHARACTER_HEIGHT = 25
WINDOW_WIDTH = 480
WINDOW_HEIGHT = 780  # povecaj visinu za 100
SIDE_PANEL_WIDTH = 200

# Dodaj desni panel
RIGHT_PANEL_WIDTH = 260  # povećano sa 200 na 260 (ili više po potrebi)

screen = pygame.display.set_mode((WINDOW_WIDTH + SIDE_PANEL_WIDTH + RIGHT_PANEL_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mapa Igre")
clock = pygame.time.Clock()

original_background = pygame.image.load("mapa3.jpg").convert()
background = pygame.transform.scale(original_background, (WINDOW_WIDTH, WINDOW_HEIGHT - 100))  # ili koristi originalnu visinu ako ti odgovara

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
        self.drawsize = (CHARACTER_WIDTH, CHARACTER_HEIGHT)

    def draw(self, surface):
        surface.blit(pygame.transform.scale(self.image, self.drawsize), self.drawpos)
        if self.selected:
            image_rect = pygame.Rect(self.drawpos, self.drawsize)
            pygame.draw.rect(surface, (0, 0, 255), image_rect, 3)
valid_fields = [
(87, 666), (191, 665), (291, 664), (390, 663), (88, 631), (190, 628), (290, 628), (391, 629),
(87, 599), (189, 598), (290, 598), (393, 599), (86, 562), (191, 562), (292, 560), (394, 563),
(87, 527), (123, 528), (154, 528), (196, 529), (227, 527), (258, 528), (290, 528), (326, 527),
(358, 525), (393, 524), (107, 493), (175, 494), (306, 494), (378, 491), (139, 460), (345, 457),
(137, 425), (345, 421), (158, 388), (329, 391), (191, 361), (295, 361), (220, 328), (269, 325),
(240, 294), (246, 261), (219, 228), (265, 226), (188, 192), (296, 190), (174, 160), (312, 159),
(176, 126), (315, 127), (198, 94), (299, 94), (249, 59), (246, 16)
]
kafici_fields = [(123, 528), (154, 528), (326, 527), (358, 525)]


characters = [
    Hero("Rajic", "Rajic.jpg", [40, 60], 0),
    Hero("Krsman", "Krsman.jpg", [40, 110], 1),
    Hero("Persic", "Persic.jpg", [80, 110], 1),
    Hero("Maja", "Maja.jpg", [120, 110], 1),
    Hero("Branka", "Branka.jpg", [160, 110], 1),
    Hero("Mitke", "Mitke.jpg", [40, 160], 2),
    Hero("Gomke", "Gomke.jpg", [80, 160], 2),
    Hero("Geci", "Geci.jpg", [120, 160], 2),
    Hero("Baler", "Baler.jpg", [160, 160], 2),
    Hero("Barac", "Barac.jpg", [40, 210], 3),
    Hero("Sladja", "Sladja.jpg", [80, 210], 3),
    Hero("Tanja", "Tanja.jpg", [120, 210], 3),
    Hero("Vlada", "Vlada.jpg", [160, 210], 3),
    Hero("Milica", "Milica.jpg", [40, 260], 4),
    Hero("Komsa", "Komsa.jpg", [80, 260], 4),
    Hero("Stifla", "Stifla.jpg", [120, 260], 4),
    Hero("Andjela", "Andjela.jpg", [160, 260], 4)
]

# Podešavanje statova
characters[1].attak = 1; characters[1].defense = 2; characters[1].speed = -1
characters[5].attak = 1; characters[5].defense = 2; characters[5].speed = -1
characters[2].attak = -1; characters[2].defense = 3; characters[2].speed = 1
characters[6].attak = -1; characters[6].defense = 3; characters[6].speed = 1
characters[3].attak = 0; characters[3].defense = 0; characters[3].speed = 3
characters[7].attak = 0; characters[7].defense = 0; characters[7].speed = 3
characters[4].attak = 1; characters[4].defense = 1; characters[4].speed = 0
characters[8].attak = 1; characters[8].defense = 1; characters[8].speed = 0

# Statovi za tim 3
characters[9].attak = characters[1].attak
characters[9].defense = characters[1].defense
characters[9].speed = characters[1].speed

characters[10].attak = characters[2].attak
characters[10].defense = characters[2].defense
characters[10].speed = characters[2].speed

characters[11].attak = characters[3].attak
characters[11].defense = characters[3].defense
characters[11].speed = characters[3].speed

characters[12].attak = characters[4].attak
characters[12].defense = characters[4].defense
characters[12].speed = characters[4].speed

# Statovi za tim 4
characters[13].attak = characters[1].attak
characters[13].defense = characters[1].defense
characters[13].speed = characters[1].speed

characters[14].attak = characters[2].attak
characters[14].defense = characters[2].defense
characters[14].speed = characters[2].speed

characters[15].attak = characters[3].attak
characters[15].defense = characters[3].defense
characters[15].speed = characters[3].speed

characters[16].attak = characters[4].attak
characters[16].defense = characters[4].defense
characters[16].speed = characters[4].speed

dice_result = None
rolling_result = None

# Dodaj na početak fajla
current_team = 1
team_order = [1, 2, 3, 4]
team_turn_index = 0
turn_dice_rolled = False
turn_character_played = False

def draw_characters_in_panel():
    for char in characters:
        if tuple(char.currentpos) not in valid_fields:
            char.drawpos = char.currentpos[:]
            char.drawsize = (CHARACTER_WIDTH, CHARACTER_HEIGHT)
            char.draw(screen)

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
    panel_x = WINDOW_WIDTH + SIDE_PANEL_WIDTH
    for _ in range(10):
        roll = random.randint(1, 6)
        screen.fill((200, 200, 200), (panel_x, 500 + y_offset, RIGHT_PANEL_WIDTH, 100))
        pygame.draw.rect(screen, (255, 255, 255), (panel_x + 10, 500 + y_offset, RIGHT_PANEL_WIDTH - 20, 90))
        label = "Napada!" if is_attacker else "Brani se!"
        screen.blit(font_small.render(f"{hero.name} {label}", True, (0, 0, 0)), (panel_x + 20, 510 + y_offset))
        screen.blit(font_large.render(str(roll), True, (0, 0, 0)), (panel_x + 20, 540 + y_offset))
        pygame.display.flip()
        pygame.time.delay(100)
    return roll

def show_final_score(hero, roll, bonus, y_offset):
    panel_x = WINDOW_WIDTH + SIDE_PANEL_WIDTH
    total = roll + bonus
    screen.fill((200, 200, 200), (panel_x, 500 + y_offset, RIGHT_PANEL_WIDTH, 100))
    pygame.draw.rect(screen, (255, 255, 255), (panel_x + 10, 500 + y_offset, RIGHT_PANEL_WIDTH - 20, 90))
    screen.blit(font_small.render(f"{hero.name} rezultat:", True, (0, 0, 0)), (panel_x + 20, 510 + y_offset))
    screen.blit(font_large.render(f"{roll} + {bonus} = {total}", True, (0, 0, 0)), (panel_x + 20, 540 + y_offset))
    pygame.display.flip()
    pygame.time.delay(1000)
    return total

def wait_for_kafic_click():
    # Prikazuj poruku ispod mape, u novom donjem prostoru
    msg_x = SIDE_PANEL_WIDTH + 20
    msg_y = WINDOW_HEIGHT - 80  # 80 piksela iznad dna prozora
    msg_w = WINDOW_WIDTH - 40
    msg_h = 60

    while True:
        # Očisti prostor ispod mape
        pygame.draw.rect(screen, (255, 255, 255), (msg_x, msg_y, msg_w, msg_h))
        pygame.draw.rect(screen, (0, 0, 0), (msg_x, msg_y, msg_w, msg_h), 2)
        screen.blit(font_large.render("Klikni na kafic!", True, (0, 0, 0)), (msg_x + 20, msg_y + 15))
        pygame.display.flip()
        pygame.time.delay(1000)
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

def get_characters_on_pos(pos):
    return [char for char in characters if char.currentpos == pos]

def draw_characters_grouped():
    for field in valid_fields:
        chars_on_field = get_characters_on_pos(field)
        n = len(chars_on_field)
        if n == 0:
            continue
        for idx, char in enumerate(chars_on_field):
            if n == 1:
                char_size = (CHARACTER_WIDTH, CHARACTER_HEIGHT)
                offset = (0, 0)
            else:
                char_size = (CHARACTER_WIDTH // 2, CHARACTER_HEIGHT // 2)
                angle = 2 * math.pi * idx / n
                radius = 12
                offset = (int(radius * math.cos(angle)), int(radius * math.sin(angle)))
            draw_x = field[0] + SIDE_PANEL_WIDTH - char_size[0] // 2 + offset[0]
            draw_y = field[1] - char_size[1] // 2 + offset[1]
            char.drawpos = [draw_x, draw_y]
            char.drawsize = char_size
            char.draw(screen)

# Dodaj ove konstante za panel
TEAM_PANEL_TOP = 90   # ispod dugmeta BACI
TEAM_PANEL_HEIGHT = 160
TEAM_PANEL_MARGIN = 20
TEAM_RECT_HEIGHT = 30
TEAM_RECT_WIDTH = SIDE_PANEL_WIDTH - 2 * TEAM_PANEL_MARGIN

# Funkcija za crtanje timova u panelu (dodaj i za TIM3)
def draw_teams_panel():
    teams = {1: [], 2: [], 3: [], 4: []}
    for char in characters:
        if char.team == 1:
            teams[1].append(char)
        elif char.team == 2:
            teams[2].append(char)
        elif char.team == 3:
            teams[3].append(char)
        elif char.team == 4:
            teams[4].append(char)
    # Prvi tim
    pygame.draw.rect(screen, (220, 220, 255), (TEAM_PANEL_MARGIN, TEAM_PANEL_TOP, TEAM_RECT_WIDTH, TEAM_RECT_HEIGHT))
    screen.blit(font_small.render("TIM1", True, (0, 0, 0)), (TEAM_PANEL_MARGIN + 5, TEAM_PANEL_TOP + 5))
    for idx, char in enumerate(teams[1]):
        x = TEAM_PANEL_MARGIN + 10 + idx * (CHARACTER_WIDTH + 10)
        y = TEAM_PANEL_TOP + 30
        char.drawpos = [x, y]
        char.drawsize = (CHARACTER_WIDTH, CHARACTER_HEIGHT)
        char.draw(screen)
    # Drugi tim
    pygame.draw.rect(screen, (255, 220, 220), (TEAM_PANEL_MARGIN, TEAM_PANEL_TOP + TEAM_PANEL_HEIGHT, TEAM_RECT_WIDTH, TEAM_RECT_HEIGHT))
    screen.blit(font_small.render("TIM2", True, (0, 0, 0)), (TEAM_PANEL_MARGIN + 5, TEAM_PANEL_TOP + TEAM_PANEL_HEIGHT + 5))
    for idx, char in enumerate(teams[2]):
        x = TEAM_PANEL_MARGIN + 10 + idx * (CHARACTER_WIDTH + 10)
        y = TEAM_PANEL_TOP + TEAM_PANEL_HEIGHT + 30
        char.drawpos = [x, y]
        char.drawsize = (CHARACTER_WIDTH, CHARACTER_HEIGHT)
        char.draw(screen)
    # Treći tim
    pygame.draw.rect(screen, (220, 255, 220), (TEAM_PANEL_MARGIN, TEAM_PANEL_TOP + 2 * TEAM_PANEL_HEIGHT, TEAM_RECT_WIDTH, TEAM_RECT_HEIGHT))
    screen.blit(font_small.render("TIM3", True, (0, 0, 0)), (TEAM_PANEL_MARGIN + 5, TEAM_PANEL_TOP + 2 * TEAM_PANEL_HEIGHT + 5))
    for idx, char in enumerate(teams[3]):
        x = TEAM_PANEL_MARGIN + 10 + idx * (CHARACTER_WIDTH + 10)
        y = TEAM_PANEL_TOP + 2 * TEAM_PANEL_HEIGHT + 30
        char.drawpos = [x, y]
        char.drawsize = (CHARACTER_WIDTH, CHARACTER_HEIGHT)
        char.draw(screen)
    # Četvrti tim
    pygame.draw.rect(screen, (255, 255, 200), (TEAM_PANEL_MARGIN, TEAM_PANEL_TOP + 3 * TEAM_PANEL_HEIGHT, TEAM_RECT_WIDTH, TEAM_RECT_HEIGHT))
    screen.blit(font_small.render("TIM4", True, (0, 0, 0)), (TEAM_PANEL_MARGIN + 5, TEAM_PANEL_TOP + 3 * TEAM_PANEL_HEIGHT + 5))
    for idx, char in enumerate(teams[4]):
        x = TEAM_PANEL_MARGIN + 10 + idx * (CHARACTER_WIDTH + 10)
        y = TEAM_PANEL_TOP + 3 * TEAM_PANEL_HEIGHT + 30
        char.drawpos = [x, y]
        char.drawsize = (CHARACTER_WIDTH, CHARACTER_HEIGHT)
        char.draw(screen)

def animate_button_roll():
    global rolling_result
    for _ in range(10):
        roll = random.randint(1, 6)
        # Očisti prostor pored dugmeta
        pygame.draw.rect(screen, (255, 255, 255), (140, 30, 50, 40))
        pygame.draw.rect(screen, (0, 0, 0), (140, 30, 50, 40), 2)
        screen.blit(font_large.render(str(roll), True, (0, 0, 0)), (155, 35))
        pygame.display.flip()
        pygame.time.delay(80)
    rolling_result = roll

def draw_button_result():
    if rolling_result is not None:
        pygame.draw.rect(screen, (255, 255, 255), (140, 30, 50, 40))
        pygame.draw.rect(screen, (0, 0, 0), (140, 30, 50, 40), 2)
        screen.blit(font_large.render(str(rolling_result), True, (0, 0, 0)), (155, 35))

def draw_current_team_panel():
    panel_x = WINDOW_WIDTH + SIDE_PANEL_WIDTH
    pygame.draw.rect(screen, (230, 230, 255), (panel_x, 30, RIGHT_PANEL_WIDTH - 20, 60))
    team_text = f"Na potezu: TIM{current_team}"
    screen.blit(font_large.render(team_text, True, (0, 0, 180)), (panel_x + 10, 50))

while True:
    screen.fill((200, 200, 200))
    screen.blit(background, (SIDE_PANEL_WIDTH, 0))

    draw_teams_panel()
    draw_characters_grouped()
    draw_button()
    draw_button_result()
    draw_current_team_panel()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Dodaj ovo pre ostalih klikova:
            if event.button == 1 and 30 <= mouse_x <= 130 and 30 <= mouse_y <= 70:
                if not turn_dice_rolled:
                    animate_button_roll()
                    turn_dice_rolled = True
                continue
            # --- NOVO: desni klik za statove ---
            if event.button == 3:  # desni klik
                for char in characters:
                    x, y = char.drawpos
                    w, h = char.drawsize
                    if (mouse_x >= x and mouse_x <= x + w and mouse_y >= y and mouse_y <= y + h):
                        # Prikazi prozor sa statovima
                        stat_rect_w, stat_rect_h = 160, 110
                        # Prilagodi poziciju da ne izlazi van ekrana
                        sx = min(mouse_x, WINDOW_WIDTH + SIDE_PANEL_WIDTH + RIGHT_PANEL_WIDTH - stat_rect_w - 10)
                        sy = min(mouse_y, WINDOW_HEIGHT - stat_rect_h - 10)
                        stat_rect = pygame.Rect(sx, sy, stat_rect_w, stat_rect_h)
                        close_rect = pygame.Rect(sx + 90, sy + 75, 60, 25)  # šire dugme

                        while True:
                            # Nacrtaj prozor
                            pygame.draw.rect(screen, (245, 245, 220), stat_rect)
                            pygame.draw.rect(screen, (0, 0, 0), stat_rect, 2)
                            screen.blit(font_small.render(f"{char.name}", True, (0, 0, 0)), (mouse_x + 10, mouse_y + 10))
                            screen.blit(font_small.render(f"Napad: {char.attak}", True, (0, 0, 0)), (mouse_x + 10, mouse_y + 35))
                            screen.blit(font_small.render(f"Odbrana: {char.defense}", True, (0, 0, 0)), (mouse_x + 10, mouse_y + 55))
                            screen.blit(font_small.render(f"Brzina: {char.speed}", True, (0, 0, 0)), (mouse_x + 10, mouse_y + 75))
                            # Dugme zatvori
                            pygame.draw.rect(screen, (200, 100, 100), close_rect)
                            pygame.draw.rect(screen, (0, 0, 0), close_rect, 1)
                            # Centriraj tekst "Zatvori" u dugmetu
                            text_surface = font_small.render("Zatvori", True, (255, 255, 255))
                            text_rect = text_surface.get_rect(center=close_rect.center)
                            screen.blit(text_surface, text_rect)
                            pygame.display.flip()
                            for ev in pygame.event.get():
                                if ev.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                elif ev.type == pygame.MOUSEBUTTONDOWN:
                                    mx, my = pygame.mouse.get_pos()
                                    if close_rect.collidepoint(mx, my):
                                        break
                            else:
                                continue
                            break
                        break
                continue

            najblize = closest_field((mouse_x - SIDE_PANEL_WIDTH, mouse_y), valid_fields)

            # Prvo proveri da li je kliknuto na grupu karaktera
            clicked_group = None
            for field in valid_fields:
                chars_on_field = get_characters_on_pos(field)
                if len(chars_on_field) > 1:
                    for char in chars_on_field:
                        x, y = char.drawpos
                        w, h = char.drawsize
                        if (mouse_x >= x and mouse_x <= x + w and mouse_y >= y and mouse_y <= y + h):
                            clicked_group = (field, chars_on_field)
                            break
                if clicked_group:
                    break

            if clicked_group:
                # Prikazi meni za izbor karaktera
                menu_rects = []
                menu_x = clicked_group[0][0] + SIDE_PANEL_WIDTH + 30
                menu_y = clicked_group[0][1] - 15

                # Prvo dodaj opciju "Niko"
                rect_niko = pygame.Rect(menu_x, menu_y, 80, 25)
                pygame.draw.rect(screen, (220, 220, 220), rect_niko)
                pygame.draw.rect(screen, (0, 0, 0), rect_niko, 1)
                screen.blit(font_small.render("Niko", True, (0, 0, 0)), (rect_niko.x + 3, rect_niko.y + 3))
                menu_rects.append((rect_niko, None))

                # Onda dodaj sve karaktere
                for idx, c in enumerate(clicked_group[1]):
                    rect = pygame.Rect(menu_x, menu_y + (idx + 1) * 30, 80, 25)
                    pygame.draw.rect(screen, (255, 255, 200), rect)
                    pygame.draw.rect(screen, (0, 0, 0), rect, 1)
                    screen.blit(font_small.render(c.name, True, (0, 0, 0)), (rect.x + 3, rect.y + 3))
                    menu_rects.append((rect, c))
                pygame.display.flip()
                selecting = True
                while selecting:
                    for ev in pygame.event.get():
                        if ev.type == pygame.MOUSEBUTTONDOWN:
                            mx, my = pygame.mouse.get_pos()
                            for rect, c in menu_rects:
                                if rect.collidepoint(mx, my):
                                    for cc in clicked_group[1]:
                                        cc.selected = False
                                    if c is not None:
                                        c.selected = True
                                        print(f"Selektovan {c.name}!")
                                    else:
                                        print("Niko nije selektovan!")
                                    selecting = False
                                    break
                        elif ev.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                continue

            # Standardna selekcija/pomeranje
            for char in characters:
                if char.selected:
                    if (mouse_x >= char.drawpos[0] and mouse_x <= char.drawpos[0] + char.drawsize[0] and
                        mouse_y >= char.drawpos[1] and mouse_y <= char.drawpos[1] + char.drawsize[1]):
                        char.selected = False
                        print(f"{char.name} vise nije selektovan!")
                    else:
                        # Dozvoli potez samo ako je njegov tim na potezu i kockica je bačena
                        if char.team == current_team and turn_dice_rolled and not turn_character_played:
                            char.drawpos = [najblize[0] + SIDE_PANEL_WIDTH - CHARACTER_WIDTH // 2,
                                            najblize[1] - CHARACTER_HEIGHT // 2]
                            char.currentpos = najblize[:]
                            char.offset_applied = False
                            print(f"{char.name} se pomera")
                            turn_character_played = True
                        else:
                            print("Nije tvoj tim na potezu ili nisi bacio kockicu!")
                    break
            else:
                for char in characters:
                    if (mouse_x >= char.drawpos[0] and mouse_x <= char.drawpos[0] + char.drawsize[0] and
                        mouse_y >= char.drawpos[1] and mouse_y <= char.drawpos[1] + char.drawsize[1]):
                        # Dozvoli selekciju samo svom timu u svom potezu
                        if char.team == current_team and turn_dice_rolled and not turn_character_played:
                            char.selected = True
                            print(f"Selektovan {char.name}!")
                        else:
                            print("Nije tvoj tim na potezu ili nisi bacio kockicu!")
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

    # Ako su oba koraka završena, prelazi na sledeći tim
    if turn_dice_rolled and turn_character_played:
        team_turn_index = (team_turn_index + 1) % len(team_order)
        current_team = team_order[team_turn_index]
        turn_dice_rolled = False
        turn_character_played = False
        rolling_result = None  # resetuj prikaz kockice

    pygame.display.flip()
    clock.tick(60)