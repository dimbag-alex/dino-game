import random

import pygame

pygame.init()

size = display_width, display_height = 800, 600  # creates tuple called size with width 400  and height 230
display = pygame.display.set_mode(size)  # creates screen
pygame.display.set_caption("DinoRun")

cactus_img = [pygame.image.load("Cactus0.png"), pygame.image.load("Cactus1.png"), pygame.image.load("Cactus2.png")]
cactus_options = [69, 449, 37, 410, 40,
                  420]  # cactus_width, window_heigth - ground - cactus_heigh, the same for second cactus

stone_img = [pygame.image.load("Stone0.png"), pygame.image.load("Stone1.png")]
cloud_img = [pygame.image.load("Cloud0.png"), pygame.image.load("Cloud1.png")]

dino_img = [pygame.image.load("Dino0.png"), pygame.image.load("Dino1.png"), pygame.image.load("Dino2.png"),
            pygame.image.load("Dino3.png"), pygame.image.load("Dino4.png")]

img_counter = 0


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            # self.x = display_width + 100 + random.randrange(-80, 60)
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


usr_width = 60
usr_height = 100
usr_x = display_width // 3
cactus_heigh = 70
usr_y = display_height - 200
clock = pygame.time.Clock()
make_jump = False
jump_counter = 30
white = 255, 255, 255
cactus_width = 20
cactus_x = display_width - 50
cactus_y = display_height - cactus_heigh - 100

scores = 0
max_scores = 0
above_cactus = False


def run_game():
    global make_jump
    global scores
    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)

    stone, cloud = open_random_objects()

    land = pygame.image.load("Land.jpg")
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True

        if keys[pygame.K_ESCAPE]:
            pause()

        if make_jump:
            jump()

        count_scores(cactus_arr)

        display.blit(land, (0, 0))
        draw_array(cactus_arr)

        print_text("Scores :" + str(scores), 600, 10)

        move_objects(stone, cloud)

        draw_dino()
        if scores <= 10:
            pygame.display.update()
            clock.tick(60)
        elif scores > 10:
            pygame.display.update()
            clock.tick(70)
        elif scores > 25:
            pygame.display.update()
            clock.tick(80)
        elif scores > 25:
            pygame.display.update()
            clock.tick(90)

        if check_collision(cactus_arr):
            game = False

    return game_over()


def jump():
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 2.5))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 2.5))

    choice = random.randrange(0, 2)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 700, height, width, img, 2.5))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if (radius - maximum) < 50:
            radius += 150
    else:
        radius = maximum

    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(200, 350)

    return radius


def draw_array(array):
    for cactus in array:
        cactus.move()
        check = cactus.move()
        if not check:
            radius = find_radius(array)

            choice = random.randrange(0, 2)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 2)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 2.5)
    cloud = Object(display_width, display_height + 80, 70, img_of_cloud, 1.5)

    return stone, cloud


def move_objects(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(50, 200), cloud.width, img_of_cloud)


def draw_dino():
    global img_counter
    if img_counter == 25:
        img_counter = 0

    display.blit(dino_img[img_counter // 5], (usr_x, usr_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type='PINGPONG.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("Paused. Press Enter to continue.", 160, 300)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(15)


def check_collision(barriers):
    for barrier in barriers:
        if barrier.y == 449:
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 20 <= barrier.x + barrier.width:
                    return True
            elif jump_counter >= 0:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 20 <= barrier.x + barrier.width:
                        return True
            else:
                if usr_y + usr_height - 10 >= barrier.y:
                    if barrier.x <= usr_x <= barrier.x + barrier.width:
                        return True
        else:
            if not make_jump:
                if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                    return True
            elif jump_counter == 10:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 5 <= barrier.x + barrier.width:
                        return True
            elif jump_counter >= -1:
                if usr_y + usr_height - 5 >= barrier.y:
                    if barrier.x <= usr_x + usr_width - 35 <= barrier.x + barrier.width:
                        return True
                else:
                    if usr_y + usr_height - 10 >= barrier.y:
                        if barrier.x <= usr_x + 5 <= barrier.x + barrier.width:
                            return True
    return False


def count_scores(barriers):
    global scores, above_cactus

    if not above_cactus:
        for barrier in barriers:
            if barrier.x <= usr_x + usr_width / 2 <= barrier.x + barrier.width:
                if usr_y + usr_height - 5 <= barrier.y:
                    above_cactus = True
                    break
    else:
        if jump_counter == -30:
            scores += 1
            above_cactus = False


def game_over():
    global max_scores, scores
    if scores > max_scores:
        max_scores = scores
        
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text("Game over. Press enter to play, esc to exit", 48, 300)
        print_text('max scores: ' + str(max_scores), 60, 250)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True

        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


while run_game():
    scores = 0
    make_jump = False
    jump_counter = 30
    usr_y = display_height - usr_height - 100
pygame.quit()
quit()
