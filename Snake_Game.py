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

current_keydown = ""
previous_keydown = ""

clock = pygame.time.Clock()  # sets the frame rate


# function to keep track of the highest recorded score to a txt file
def load_high_score():
    try:
        hi_score_file = open("HI_score.txt", "r")
    except IOError:
        hi_score_file = open("HI_score.txt", "w")
        hi_score_file.write("0")
    hi_score_file = open("HI_score.txt", "r")
    value = hi_score_file.read()
    hi_score_file.close()
    return value


# update record of the highest score
def update_high_score(score, hi_score):
    if int(score) > int(hi_score):
        return score
    else:
        return hi_score


# save updated high score to txt file
def save_high_score(hi_score):
    high_score_file = open("HI_score.txt", "w")
    high_score_file.write(str(hi_score))
    high_score_file.close()


# display player score in the game
def player_score(score, score_colour):
    display_score = score_font.render(f"Score: {score}", True, score_colour)
    screen.blit(display_score, (800, 20))  # coordinates for top right


# create snake - replaces previous snake drawing section in main loop
def draw_snake(snake_list):
    print(f"Snake list: {snake_list}")  # for testing
    for i in snake_list:
        pygame.draw.rect(screen, red, [i[0], i[1], 20, 20])


def message(msg, txt_colour, bkgd_colour):
    txt = msg_font.render(msg, True, txt_colour, bkgd_colour)

    # centre rect: 1000/2 =500 and 720/2 = 360
    text_box = txt.get_rect(center=(500, 360))
    screen.blit(txt, text_box)


def game_loop():

    global current_keydown
    global previous_keydown

    start_time = time.time()
    quit_game = False
    game_over = False

    # snake will be 20 * 20px
    snake_x = 480  # centre point horizontally is (1000-20 snake width)/2 =490
    snake_y = 340

    snake_x_change = 0  # holds the value of changes in the x co-ord
    snake_y_change = 0
    snake_list = []
    snake_length = 1

    # set a random position for the food to start
    food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
    food_y = round(random.randrange(20, 720 - 20) / 20) * 20

    # load the high score
    high_score = load_high_score()
    print(f"high_score test: {high_score}")  # for testing purposes

    while not quit_game:
        # give user the option to quit or play again when they die
        while game_over:
            save_high_score(high_score)
            screen.fill(white)
            message(f"You died! (Score: {score}) Press 'Q' to Quit or 'A' to play again",
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
                    current_keydown = "left"
                    if previous_keydown != "right":
                        snake_x_change = -20
                        snake_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    current_keydown = "right"
                    if previous_keydown != "left":
                        snake_x_change = 20
                        snake_y_change = 0
                elif event.key == pygame.K_UP:
                    current_keydown = "up"
                    if previous_keydown != "down":
                        snake_x_change = 0
                        snake_y_change = -20
                elif event.key == pygame.K_DOWN:
                    current_keydown = "down"
                    if previous_keydown != "up":
                        snake_x_change = 0
                        snake_y_change = 20

            current_keydown = previous_keydown

        if snake_x >= 1000 or snake_x < 0 or snake_y >= 720 or snake_y < 0:
            game_over = True

        snake_x += snake_x_change
        snake_y += snake_y_change

        screen.fill(green)

        # create rect for snake
        snake_head = [snake_x, snake_y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

            for x in snake_list[:-1]:
                if x == snake_head:
                    game_over = True

            draw_snake(snake_list)

        # keeping track of player score
        score = round(snake_length)
        player_score(score, black)

        # get high score
        high_score = update_high_score(score, high_score)

        # increase difficulty speed up snake
        if score > 10:
            speed = (score + 1)
        else:
            speed = 10

        # using sprite for food
        food = pygame.Rect(food_x, food_y, 20, 20)
        number = random.randint(1, 20)
        if number == 1:
            apple = pygame.image.load("rainbow_apple.png").convert_alpha()
        else:
            apple = pygame.image.load("apple.png").convert_alpha()
        resized_apple = pygame.transform.smoothscale(apple, [20, 20])
        screen.blit(resized_apple, food)
        pygame.display.update()

        # food collision detection
        # print lines are for testing
        print(f"Snake x: {snake_x}")
        print(f"Food x: {food_x}")
        print(f"Snake y: {snake_y}")
        print(f"Food y: {food_y}")
        print("\n\n")

        # detecting contact with food sprite (instead of circle)
        if snake_x == food_x and snake_y == food_y:
            #  set new position for food if snake touches it
            food_x = round(random.randrange(20, 1000 - 20) / 20) * 20
            food_y = round(random.randrange(20, 720 - 20) / 20) * 20
            # testing
            print("Got it")

            # increase length of snake (by original size)
            snake_length += 1

            score += 1

        clock.tick(speed)  # game runs at 15 fps

    pygame.quit()
    quit()


# Main
game_loop()
