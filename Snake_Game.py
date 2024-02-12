import pygame
import time
pygame.init()


screen = pygame.display.set_mode((1000, 720))
game_icon = pygame.image.load("snake_icon.png")
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Snake Game")

# colour variables
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (188, 227, 119)

# game fonts
score_font = pygame.font.SysFont("consolas", 20)
exit_font = pygame.font.SysFont("arialblack", 30)

clock = pygame.time.Clock()  # sets the frame rate

# snake will be 20 * 20px
snake_x = 490  # centre point horizontally is (1000-20 snake width)/2 =490
snake_y = 350

snake_x_change = 0  # holds the value of changes in the x co-ord
snake_y_change = 0


quit_game = False
while not quit_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_x_change = -20
                snake_y_change = 0
            elif event.key == pygame.K_RIGHT:
                snake_x_change = 20
                snake_y_change = 0
            elif event.key == pygame.K_UP:
                snake_x_change = 0
                snake_y_change = -20
            elif event.key == pygame.K_DOWN:
                snake_x_change = 0
                snake_y_change = 20

    if snake_x >= 1000 or snake_x < 0 or snake_y >= 720 or snake_y < 0:
        quit_game = True

    snake_x += snake_x_change
    snake_y += snake_y_change

    screen.fill(green)

    # create rect for snake
    pygame.draw.rect(screen, red, [snake_x, snake_y, 20, 20])
    pygame.display.update()

    clock.tick(15)


pygame.quit()
quit()
