import pygame
import sys
import math
import random
import os

def resource_path(relative_path):
    """Ottiene il percorso corretto per una risorsa."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Inizializza Pygame
pygame.init()

# Impostazioni della finestra
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Intro by Kr0n0s for WWW.LAFORESTAINCANTATA.ORG")

# Colori e font
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)
RAINBOW_COLORS = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (128, 0, 128)]
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 18)

# Testo sinusoidale
sinusoidal_text = "**** KR0N0S PRESENTS ANOTHER FINE RELEASE FOR WWW.LAFORESTAINCANTATA.ORG ... INTRO CODED BY KR0N0S IN MEMORY OF OLD CRACKTRO FROM THE '90s ... I would like to thank all the great scene groups who have inspired me with their amazing creations over the past 30 years. Thanks for everything, guys! *****"
text_width = len(sinusoidal_text) * 40
start_x = WIDTH
x_positions = [start_x + i * 40 for i in range(len(sinusoidal_text))]

# Genera stelle casuali per lo sfondo
stars = [{'x': random.uniform(-WIDTH // 2, WIDTH // 2),
          'y': random.uniform(-HEIGHT // 2, HEIGHT // 2),
          'z': random.uniform(1, WIDTH // 2)} for _ in range(1000)]

# Carica il suono della cracktro
pygame.mixer.init()
pygame.mixer.music.load(resource_path("assets/cracktro.xm"))
pygame.mixer.music.play(loops=-1)

# Carica i loghi
logo = pygame.image.load(resource_path("assets/kr0n0s.png"))
corner_logo = pygame.image.load(resource_path("assets/logo.png"))

# Clock per il frame rate
clock = pygame.time.Clock()
time = 0
angle_x, angle_y, angle_z = 0, 0, 0

# Vertici e facce del cubo
cube_vertices = [
    [-50, -50, -50], [50, -50, -50], [50, 50, -50], [-50, 50, -50],
    [-50, -50, 50], [50, -50, 50], [50, 50, 50], [-50, 50, 50]
]
cube_faces = [
    ([0, 1, 2, 3], (255, 0, 0)), ([4, 5, 6, 7], (0, 255, 0)),
    ([0, 1, 5, 4], (0, 0, 255)), ([2, 3, 7, 6], (255, 255, 0)),
    ([0, 3, 7, 4], (255, 0, 255)), ([1, 2, 6, 5], (0, 255, 255))
]

# Posizione del movimento delle stelle
target_x, target_y = WIDTH // 2, HEIGHT // 2

# Funzione per proiettare punti 3D su 2D
def project_3d_to_2d(x, y, z, angle_x, angle_y, angle_z):
    cos_x, sin_x = math.cos(angle_x), math.sin(angle_x)
    y, z = y * cos_x - z * sin_x, y * sin_x + z * cos_x
    cos_y, sin_y = math.cos(angle_y), math.sin(angle_y)
    x, z = x * cos_y + z * sin_y, -x * sin_y + z * cos_y
    cos_z, sin_z = math.cos(angle_z), math.sin(angle_z)
    x, y = x * cos_z - y * sin_z, x * sin_z + y * cos_z
    scale = 100 / (z + 200)
    x_projected = x * scale + 100  # Posiziona il cubo in basso a sinistra
    y_projected = y * scale + HEIGHT - 100
    return x_projected, y_projected

# Ciclo principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    # Aggiorna la posizione target con il movimento del mouse
    target_x, target_y = pygame.mouse.get_pos()

    screen.fill(BLACK)

    # Stelle
    center_x, center_y = target_x, target_y
    for star in stars:
        star['z'] -= 2
        if star['z'] <= 0:
            star['x'] = random.uniform(-WIDTH // 2, WIDTH // 2)
            star['y'] = random.uniform(-HEIGHT // 2, HEIGHT // 2)
            star['z'] = WIDTH // 2
        scale = 400 / star['z']
        screen_x = int(star['x'] * scale + center_x)
        screen_y = int(star['y'] * scale + center_y)
        size = max(1, int(3 * (WIDTH // 2 - star['z']) / (WIDTH // 2)))
        color = RAINBOW_COLORS[random.randint(0, len(RAINBOW_COLORS) - 1)]
        pygame.draw.circle(screen, color, (screen_x, screen_y), size)

    # Testo sinusoidale
    for i, char in enumerate(sinusoidal_text):
        x = x_positions[i] - 4
        y = int(math.sin((x + time) * 0.02) * 70 + HEIGHT // 2 + 150)  # Abbassata la scritta scorrevole
        if x < -text_width:
            x_positions = [start_x + j * 40 for j in range(len(sinusoidal_text))]
            break
        color = RAINBOW_COLORS[i % len(RAINBOW_COLORS)]
        rendered_char = font.render(char, True, color)
        screen.blit(rendered_char, (x, y))
        x_positions[i] = x

    # Logo
    screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, 10))  # Alzato al massimo il logo
    screen.blit(corner_logo, (WIDTH - corner_logo.get_width() - 10, HEIGHT - corner_logo.get_height() - 10))

    # Testo "Use your mouse for space journey"
    journey_text = small_font.render("Use your mouse for space journey", True, DARK_BLUE)
    screen.blit(journey_text, (10, 10))

    # Disegna il cubo in basso a sinistra
    rotated_vertices = [project_3d_to_2d(x, y, z, angle_x, angle_y, angle_z) for x, y, z in cube_vertices]
    for face, color in cube_faces:
        points = [rotated_vertices[i] for i in face]
        pygame.draw.polygon(screen, color, points, 2)

    time += 1
    angle_x += 0.03
    angle_y += 0.04
    angle_z += 0.05

    pygame.display.flip()
    clock.tick(60)

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
