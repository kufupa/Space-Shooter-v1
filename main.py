import pygame
import os

# pygame.init() # initiliase all pygame modules
pygame.font.init()  # for displaying text
pygame.mixer.init()  # for playing sounds

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "Gun+Silencer.mp3"))

WIDTH, HEIGHT = 960, 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame in 90 Minutes - For Beginners - Xin Code")
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BULLET_VEL = 8
MAX_BULLETS = 5

BORDER = pygame.Rect(WIDTH // 2 - 10, 0, 20, HEIGHT)

VEL = 5
SHIP_WIDTH, SHIP_HEIGHT = 60, 50

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 90
)

RED_SHIP_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SHIP_IMAGE, (SHIP_WIDTH, SHIP_HEIGHT)), 270
)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT)
)


def yellow_handle_movement(keys_pressed, yellow):
    # wasd is for the yellow spaceship (one on the left)
    if (
        keys_pressed[pygame.K_a] and yellow.x - VEL > 0
    ):  # "a" key, left, decreasing x axis
        yellow.x -= VEL
    if (
        keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x
    ):  # "d" key, right, increasing x axis
        yellow.x += VEL
    if (
        keys_pressed[pygame.K_w] and yellow.y - VEL > 0
    ):  # "w" key, up, decreasing y axis
        yellow.y -= VEL
    if (
        keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT
    ):  # "s" key, down, increasing y axis
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    # arrow keys for red ship (one on the right)
    if (
        keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width
    ):  # left, decreasing x axis
        red.x -= VEL
    if (
        keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH
    ):  # right, increasing x axis
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up, decreasing y axis
        red.y -= VEL
    if (
        keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT
    ):  # down, increasing y axis
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    # Checks for collisions
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SHIP, (red.x, red.y))
    pygame.draw.rect(WIN, BLACK, BORDER)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_winner(winner_text):
    draw_text = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(
        draw_text,
        (
            (WIDTH / 2 - draw_text.get_width() // 2),
            (HEIGHT / 2 - draw_text.get_height() // 2),
        ),
    )
    pygame.display.update()
    pygame.time.delay(3000)


def game():

    red = pygame.Rect(775, 300, SHIP_WIDTH, SHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SHIP_WIDTH, SHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 5
    yellow_health = 5

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width,
                        yellow.y + yellow.height // 2 - 2,
                        10,
                        5,
                    )
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            winner_text = ""

            if event.type == RED_HIT:
                red_health -= 1
                if red_health <= 0:
                    winner_text = "YELLOW WINS!"
                BULLET_HIT_SOUND.play()

            elif event.type == YELLOW_HIT:
                yellow_health -= 1
                if yellow_health <= 0:
                    winner_text = "RED WINS!"
                BULLET_HIT_SOUND.play()

            if winner_text != "":  # Somebody Won!
                draw_window(
                    red, yellow, red_bullets, yellow_bullets, red_health, yellow_health
                )
                draw_winner(winner_text)
                run = False

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.quit()


if __name__ == "__main__":
    game()
