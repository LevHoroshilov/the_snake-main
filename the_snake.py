from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
direct_list = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 6

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def new_position(self):
        self.position = (randint(0, GRID_WIDTH - GRID_SIZE) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - GRID_SIZE) * GRID_SIZE)


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None

    def move(self):
        self.head = self.get_head_position()
        if self.direction == RIGHT:
            self.positions.insert(0, ((self.head[0] + GRID_SIZE) %
                                      SCREEN_WIDTH, self.head[1]))
        elif self.direction == LEFT:
            self.positions.insert(0, ((self.head[0] - GRID_SIZE) %
                                      SCREEN_WIDTH, self.head[1]))
        elif self.direction == UP:
            self.positions.insert(0, (self.head[0], (self.head[1] - GRID_SIZE)
                                      % SCREEN_HEIGHT))
        elif self.direction == DOWN:
            self.positions.insert(0, (self.head[0], (self.head[1] + GRID_SIZE)
                                      % SCREEN_HEIGHT))

    def draw(self):
        for position in self.positions[::-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, head_rect)
            pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        if len(self.positions) > self.length:
            last_rect = pygame.Rect(self.positions[-1], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            list.remove(self.positions, self.positions[-1])

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def reset(self):
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice(direct_list)


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        pygame.display.update()
        if snake.get_head_position() == apple.position:
            while True:
                apple.new_position()
                if apple.position not in snake.positions:
                    break
            snake.length += 1
            apple.draw()
            pygame.display.update()
        if snake.positions.count(snake.get_head_position()) > 1:
            snake.reset()
            pygame.display.update()


if __name__ == '__main__':
    main()
