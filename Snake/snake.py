
import pygame
from random import randint
from pygame.locals import *
from enum import Enum

"""
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
RPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
RPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
RPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
RPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)
up = GPIO.input(18)
right = GPIO.input(23)
down = GPIO.input(24)
left = GPIO.input(25)
"""


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Node:
    def __init__(self, x_coord, y_coord, child=None):
        self.x = x_coord
        self.y = y_coord
        self.child = child

    def move(self, d, dist):
        if self.child is not None:
            self.child.move_to(self.x, self.y)
        if d == Direction.UP:
            self.y -= dist
        elif d == Direction.RIGHT:
            self.x += dist
        elif d == Direction.DOWN:
            self.y += dist
        elif d == Direction.LEFT:
            self.x -= dist

    def move_to(self, new_x, new_y):
        if self.child is not None:
            self.child.move_to(self.x, self.y)
        self.x = new_x
        self.y = new_y


def random_food():
    return randint(2, (w / food_size) - 1) * food_size, randint(2, (h / food_size) - 1) * food_size


def snake():
    t3 = Node(w / 2 - 3 * player_size, h / 2)
    t2 = Node(w / 2 - 2 * player_size, h / 2, t3)
    t1 = Node(w / 2 - 1 * player_size, h / 2, t2)
    return Node(w / 2, h / 2, t1)


def draw_square(color, x, y, size):
    pygame.draw.rect(screen, color, [x-size/2, y-size/2, size, size])


pygame.init()
w, h = 800, 600
screen = pygame.display.set_mode((w+60, h+60))
player_size = 16
expanded_size = 20
food_size = 16
border = 10

running = 1
direction = Direction.RIGHT
head = snake()
food_x, food_y = random_food()
expand_points = []
step = 0
pause = False
dead = False

# Colors
green = (172, 184, 80)
gray = (101, 81, 38)

while running:
    # BACKGROUND
    screen.fill(green)

    # BORDERS
    for x in range(10, w+60-border-10, 12):
        pygame.draw.rect(screen, gray, [x, 10, border, border])
        pygame.draw.rect(screen, gray, [x, h+60-border-10, border, border])

    for x in range(10, h+60-border-10, 12):
        pygame.draw.rect(screen, gray, [10, x, border, border])
        pygame.draw.rect(screen, gray, [w+60-border-10, x, border, border])

    pygame.draw.rect(screen, gray, [w+60-border-10, h + 60 - border - 10, border, border])

    if dead:
        running = 1
        direction = Direction.RIGHT
        head = snake()
        food_x, food_y = random_food()
        expand_points = []
        step = 0
        pause = False
        dead = False

    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        elif event.type == KEYDOWN:
            if event.key == 273 and (direction == Direction.LEFT or direction == Direction.RIGHT):
                direction = Direction.UP
            elif event.key == 275 and (direction == Direction.UP or direction == Direction.DOWN):
                direction = Direction.RIGHT
            elif event.key == 274 and (direction == Direction.LEFT or direction == Direction.RIGHT):
                direction = Direction.DOWN
            elif event.key == 276 and (direction == Direction.UP or direction == Direction.DOWN):
                direction = Direction.LEFT
            elif event.key == 32:
                pause = not pause
            elif event.key == 8:
                dead = True

    if step % 5 == 0 and not pause:
        head.move(direction, dist=player_size)
        if head.x <= 30 or head.x >= w or head.y <= 30 or head.y >= h:
            dead = True

    # DRAW SNAKE
    node = head
    while node is not None:
        draw_square(gray, node.x, node.y, player_size)
        if node.child is None:
            break
        else:
            node = node.child

    # Draw expanded points on the snake (and add new child if expanded point hits tail)
    remove_point = None
    for (exp_x, exp_y) in expand_points:
        if node.x == exp_x and node.y == exp_y:
            node.child = Node(node.x, node.y)
            remove_point = (exp_x, exp_y)
        pygame.draw.rect(screen, gray, [exp_x-expanded_size/2, exp_y-expanded_size/2, expanded_size, expanded_size])
    if remove_point is not None:
        expand_points = [x for x in expand_points if not x == remove_point]

    # DRAW FOOD
    pygame.draw.rect(screen, gray, [food_x-(food_size/2), food_y-(food_size/2), food_size, food_size])
    pygame.draw.rect(screen, (0, 0, 0), [food_x, food_y, 1, 1])

    # EATING
    if abs(head.x - food_x) < player_size/2+1 and abs(head.y - food_y) < player_size/2+1:
        expand_points.append((head.x, head.y))
        food_x, food_y = random_food()

    pygame.display.flip()
    step = step + 1



pygame.quit()

