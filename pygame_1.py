import pygame
import random
from pygame.math import Vector2
from sys import exit
from pygame import mixer

mixer.init()
mixer.music.load('music/5 Action Chiptunes By Juhani Junkala/Juhani Junkala [Retro Game Music Pack] Level 1.wav')
mixer.music.set_volume(0.05)
mixer.music.play(-1)


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('images/snake_game_graphic/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('images/snake_game_graphic/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('images/snake_game_graphic/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('images/snake_game_graphic/head_left.png').convert_alpha()

        self.body_tr = pygame.image.load('images/snake_game_graphic/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('images/snake_game_graphic/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('images/snake_game_graphic/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('images/snake_game_graphic/body_bl.png').convert_alpha()

        self.body_ver = pygame.image.load('images/snake_game_graphic/body_vertical.png').convert_alpha()
        self.body_hor = pygame.image.load('images/snake_game_graphic/body_horizontal.png').convert_alpha()

    def make_snake(self):
        self.update_head_direct()

        for index, block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index != 0 and index != len(self.body) - 1:
                prev_block = self.body[index+1] - block
                next_block = self.body[index-1] - block
                if prev_block.x == next_block.x:
                    screen.blit(self.body_ver, block_rect)
                elif prev_block.y == next_block.y:
                    screen.blit(self.body_hor, block_rect)
                else:
                    if prev_block.x == -1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif prev_block.x == -1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif prev_block.x == 1 and next_block.y == -1 or prev_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif prev_block.x == 1 and next_block.y == 1 or prev_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_direct(self):
        neck_pos = self.body[1] - self.body[0]
        if neck_pos == Vector2(1, 0):
            self.head = self.head_left
        elif neck_pos == Vector2(-1, 0):
            self.head = self.head_right
        elif neck_pos == Vector2(0, 1):
            self.head = self.head_up
        elif neck_pos == Vector2(0, -1):
            self.head = self.head_down

    def move_snake(self):
        # when moving the snake,copy the all previous position except the last block
        if self.new_block is True:
            copy_body = self.body[:]
            copy_body.insert(0, copy_body[0] + self.direction)
            self.body = copy_body[:]
            self.new_block = False
        else:
            copy_body = self.body[:-1]
            copy_body.insert(0, copy_body[0] + self.direction)
            self.body = copy_body[:]

    def add_length(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class TARGET:
    def __init__(self):
        self.re_generate_target()

    def make_target(self):
        tar_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(target, tar_rect)

    def re_generate_target(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.target = TARGET()

    def update(self):
        self.snake.move_snake()
        self.check_eating()
        self.check_game_over()

    def track_max(self):
        with open("highest_score.txt", "r") as f:
            return f.read()

    def draw_element(self):
        self.grass()
        self.target.make_target()
        self.snake.make_snake()
        self.score_board()

    def check_eating(self):
        # if snake hit the target
        if self.target.pos == self.snake.body[0]:
            # reposition the target
            self.target.re_generate_target()
            # and add length of the snake
            self.snake.add_length()

        for block in self.snake.body[1:]:
            if block == self.target.pos:
                self.target.re_generate_target()

    def check_game_over(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for body in self.snake.body[1:]:
            if body == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def score_board(self):
        score_text = ": " + str(len(self.snake.body) - 3)
        score_surf = game_font.render(score_text, True, (56, 74, 22))
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40

        score_rect = score_surf.get_rect(center=(score_x, score_y))
        target_rect = target.get_rect(midright=(score_rect.left, score_rect.centery))

        screen.blit(score_surf, score_rect)
        screen.blit(target, target_rect)

        current_score = len(self.snake.body) - 3
        try:
            max_score = int(self.track_max())
        except:
            max_score = 0
        if max_score < current_score:
            max_score = current_score
        with open("highest_score.txt", "w") as f:
            f.write(str(max_score))
        max_text = "Highest: " + str(max_score)
        max_surf = game_font.render(max_text, True, (56, 74, 22))
        max_rect = max_surf.get_rect(center=(score_x - 30, score_y - 40))

        screen.blit(max_surf, max_rect)

    def grass(self):
        grass_color = (153, 209, 169)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def paused(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c or event.key == pygame.K_p:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        exit()

            screen.fill((255, 255, 235))
            text = "GAME PAUSED\
            Press P or C to play\
            Press Q to quit game"
            text_surf = game_font.render(text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=(400, 300))
            screen.blit(text_surf, text_rect)
            pygame.display.update()
            clock.tick(10)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size, cell_number*cell_size))  # width,height
pygame.display.set_caption('Snake Game')
# clock object to set frame rate
clock = pygame.time.Clock()

target = pygame.image.load('images/snake_game_graphic/apple.png').convert_alpha()

game_font = pygame.font.SysFont('Times', 25)
main_game = MAIN()
screen_update = pygame.USEREVENT
pygame.time.set_timer(screen_update, 100)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == screen_update:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_p:
                main_game.paused()

    screen.fill((122, 163, 134))
    main_game.draw_element()
    pygame.display.update()
    clock.tick(60)  # set the max frame rate = 60fps
