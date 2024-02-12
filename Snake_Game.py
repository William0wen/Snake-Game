import pygame
import time
import random
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
yellow = (255, 255, 0)

# game fonts
score_font = pygame.font.SysFont("consolas", 20)
exit_font = pygame.font.SysFont("arialblack", 30)
msg_font = pygame.font.SysFont("consolas", 20)

clock = pygame.time.Clock()  # sets the frame rate


def message(msg, txt_colour, bkgd_colour):
    txt = msg_font.render(msg, True, txt_colour, bkgd_colour)

    # centre rect: 1000/2 =500 and 720/2 = 360
    text_box = txt.get_rect(center=(500, 360))
    screen.blit(txt, text_box)


def game_loop():
    quit_game = False
    game_over = False

    # snake will be 20 * 20px
    snake_x = 490  # centre point horizontally is (1000-20 snake width)/2 =490
    snake_y = 350

    snake_x_change = 0  # holds the value of changes in the x co-ord
    snake_y_change = 0

    # set a random position for the food to start
    food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
    food_y = round(random.randrange(20, 720 - 20) / 20) * 20

    while not quit_game:
        # give user the option to quit or play again when they die
        while game_over:
            screen.fill(white)
            message("You died! Press 'Q' to Quit or 'A' to play again",
                    white, black)
            pygame.display.update()

            # check if user wants to quit(q) or play again (a)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit_game = True
                        game_over = False
                    if event.key == pygame.K_a:
                        game_loop()  # restart game loop

        # handling response if user presses 'X' - giving them the option
        # to quit, start new game, or keep playing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instructions = "Exit: Q to Quit, SPACE to resume, R to reset"
                message(instructions, white, black)
                pygame.display.update()

                end = False
                while not end:
                    for event in pygame.event.get():
                        # if user presses X button, game quits
                        if event.type == pygame.QUIT:
                            quit_game = True
                            end = True

                        # if user presses R button again, game is reset
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                end = True, game_loop()

                        # if user presses space, game continues
                            if event.key == pygame.K_SPACE:
                                end = True

                        # if user presses Q, game quits
                            if event.key == pygame.K_q:
                                quit_game = True
                                end = True

            # snake arrow key controls
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
            game_over = True

        snake_x += snake_x_change
        snake_y += snake_y_change

        screen.fill(green)

        # create rect for snake
        pygame.draw.rect(screen, red, [snake_x, snake_y, 20, 20])
        pygame.display.update()

        # create circle for food
        pygame.draw.circle(screen, yellow, [food_x, food_y], 10)
        pygame.display.update()

        # food collision detection
        if snake_x == food_x - 10 and snake_y == food_y - 10:
            #  set new position for food if snake touches it
            food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
            food_y = round(random.randrange(20, 720 - 20) / 20) * 20

        clock.tick(10)  # game runs at 15 fps

    pygame.quit()
    quit()


# Main
game_loop()
