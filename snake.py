import pygame
import random

# Configuración del juego
pygame.init()
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colores
GREEN_LIGHT = (168, 230, 161)  # Verde claro
GREEN_DARK = (76, 175, 80)  # Verde oscuro
GRID_LINES = (50, 120, 50)  # Verde oscuro pero más suave que negro

# Cargar imágenes
apple_img = pygame.image.load("src/img/apple.png")
snake_head_img = pygame.image.load("src/img/cabeza.png")  # Imagen de la cabeza
snake_body_img = pygame.image.load("src/img/cuerpo.png")  # Imagen del cuerpo

# Redimensionar imágenes
snake_head_img = pygame.transform.scale(snake_head_img, (GRID_SIZE, GRID_SIZE))
snake_body_img = pygame.transform.scale(snake_body_img, (GRID_SIZE, GRID_SIZE))
apple_size = int(GRID_SIZE * 1.5)  # Tamaño aumentado de la manzana
apple_img = pygame.transform.scale(apple_img, (apple_size, apple_size))

# Generar posiciones aleatorias para cuadros claros
def generate_light_squares():
    return {(random.randint(0, COLS - 1), random.randint(0, ROWS - 1)) for _ in range(50)}

light_squares = generate_light_squares()

# Clase de la serpiente
class Snake:
    def __init__(self):
        self.body = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = (0, -GRID_SIZE)
        self.growing = False

    def move(self):
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        if not self.growing:
            self.body.pop()
        else:
            self.growing = False
        self.body.insert(0, new_head)

    def grow(self):
        self.growing = True

    def check_collision(self):
        head_x, head_y = self.body[0]
        return (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or self.body[0] in self.body[1:])

    def draw(self):
        # Dibujar cabeza
        screen.blit(snake_head_img, self.body[0])
        # Dibujar cuerpo
        for segment in self.body[1:]:
            screen.blit(snake_body_img, segment)

# Clase de la comida
class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.position = (
            random.randrange(0, WIDTH, GRID_SIZE),
            random.randrange(0, HEIGHT, GRID_SIZE)
        )

    def draw(self):
        x, y = self.position
        x_centered = x - (apple_size - GRID_SIZE) // 2  # Centrar la manzana en la celda
        y_centered = y - (apple_size - GRID_SIZE) // 2
        screen.blit(apple_img, (x_centered, y_centered))

# Función para dibujar la cuadrícula con base en verde oscuro y cuadros claros aleatorios
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = GREEN_LIGHT if (col, row) in light_squares else GREEN_DARK
            pygame.draw.rect(screen, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    # Dibujar líneas de la cuadrícula con menor visibilidad
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRID_LINES, (x, 0), (x, HEIGHT), 1)  # Grosor reducido a 1 px
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRID_LINES, (0, y), (WIDTH, y), 1)

    # Dibujar bordes del juego
    pygame.draw.rect(screen, GREEN_DARK, (0, 0, WIDTH, HEIGHT), 3)

# Función para regenerar cuadros claros después de comer una manzana
def update_light_squares():
    global light_squares
    light_squares = generate_light_squares()

# Función para mostrar el botón de reintentar
def draw_retry_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Reintentar", True, (0, 0, 0))
    button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 20, 150, 50)

    pygame.draw.rect(screen, (255, 255, 255), button_rect, border_radius=10)
    screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2 + 30))

    return button_rect

# Función principal
def game_loop():
    snake = Snake()
    food = Food()
    running = True
    game_over = False
    score = 0

    while running:
        screen.fill((255, 255, 255))
        draw_grid()  # Dibuja la cuadrícula con colores aleatorios

        if game_over:
            font = pygame.font.Font(None, 36)
            text = font.render(f"Manzanas recogidas: {score}", True, (0, 0, 0))
            screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))

            retry_button = draw_retry_button()
            pygame.display.flip()

            while True:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN and retry_button.collidepoint(event.pos):
                    game_loop()
                    return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != (0, GRID_SIZE):
                    snake.direction = (0, -GRID_SIZE)
                elif event.key == pygame.K_DOWN and snake.direction != (0, -GRID_SIZE):
                    snake.direction = (0, GRID_SIZE)
                elif event.key == pygame.K_LEFT and snake.direction != (GRID_SIZE, 0):
                    snake.direction = (-GRID_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake.direction != (-GRID_SIZE, 0):
                    snake.direction = (GRID_SIZE, 0)

        snake.move()
        if snake.body[0] == food.position:
            snake.grow()
            food.respawn()
            score += 1
            update_light_squares()  # Cambiar posiciones de cuadros claros

        if snake.check_collision():
            game_over = True

        food.draw()
        snake.draw()

        # Mostrar el puntaje
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Manzanas: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()


game_loop()