import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Starship !')
pygame_icon = pygame.image.load(os.path.join('Assets','spaceship-64x64.ico'))
pygame.display.set_icon(pygame_icon)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','hit-sound.wav'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','laser_1.mp3'))

WINNER_SOUND = pygame.mixer.Sound(os.path.join('Assets','winner.wav'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 120)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

RED_HIT = pygame.USEREVENT + 1
GREEN_HIT = pygame.USEREVENT + 2

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship-red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

GREEN_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship-green.png'))
GREEN_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(GREEN_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.jpg')), (WIDTH, HEIGHT))

def draw_window(red, green, red_bullets, green_bullets, red_health, green_health):
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(SPACE, (0, 0))

    red_health_text = HEALTH_FONT.render('Health : ' + str(red_health), 1, WHITE)
    green_health_text = HEALTH_FONT.render('Health : ' + str(green_health), 1, WHITE)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(green_health_text, ((WIDTH - green_health_text.get_width() - 10), 10))

    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(GREEN_SPACESHIP, (green.x, green.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    for bullet in green_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width - 15 < BORDER.x: #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 40: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT - 15: #DOWN
        red.y += VEL

def green_handle_movement(keys_pressed, green):
    if keys_pressed[pygame.K_LEFT] and green.x - VEL > BORDER.x + BORDER.width: #LEFT
        green.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and green.x - VEL + green.width < WIDTH + 5: #RIGHT
        green.x += VEL
    if keys_pressed[pygame.K_UP] and green.y - VEL > 40: #UP
        green.y -= VEL
    if keys_pressed[pygame.K_DOWN] and green.y + VEL + green.height < HEIGHT - 15: #DOWN
        green.y += VEL

def handle_bullets(red_bullets, green_bullets, red, green):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            green_bullets.remove(bullet)
        elif bullet.x < 0:
            green_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, ((WIDTH/2 - draw_text.get_width()/2), (HEIGHT/2 - draw_text.get_height()/2)))
    pygame.display.update()
    WINNER_SOUND.play()
    pygame.time.delay(8000)

def main():
    red = pygame.Rect(200, 350, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    green = pygame.Rect(1040, 350, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    green_bullets = []

    red_health = 10
    green_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(green_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(green.x, green.y + green.height//2 - 2, 10, 5)
                    green_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == GREEN_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ''
        if red_health <= 0:
            winner_text = 'Green Won !'
        if green_health <= 0:
            winner_text = 'Red Won !'
        
        if winner_text != '':
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        green_handle_movement(keys_pressed, green)

        handle_bullets(red_bullets, green_bullets, red, green)

        draw_window(red, green, red_bullets, green_bullets, red_health, green_health)
    
    main()


if __name__ == '__main__':
    main()