
import time
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
    return randint(1, (w / food_size) - 1) * food_size, randint(1, (h / food_size) - 1) * food_size


pygame.init()
w, h = 800, 600
screen = pygame.display.set_mode((w+30, h+30))
player_size = 10
expanded_size = 14
food_size = 10

running = 1
direction = Direction.RIGHT
head = Node(w/2, h/2, Node(w/2-player_size, h/2))
food_x, food_y = random_food()
expand_points = []
step = 0

# Colors
green = (172, 184, 80)
gray = (101, 81, 38)

while running:
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

    # BACKGROUND
    screen.fill(green)

    # DRAW SNAKE
    node = head
    while node is not None:
        pygame.draw.rect(screen, gray, [node.x-player_size/2, node.y-player_size/2, player_size, player_size])
        if node.child is None:
            break
        else:
            node = node.child

    if step % 5 == 0:
        head.move(direction, dist=player_size)

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

    # EATING
    if abs(head.x - food_x) < player_size/2+1 and abs(head.y - food_y) < player_size/2+1:
        expand_points.append((head.x, head.y))
        food_x, food_y = random_food()

    # BORDERS
    for x in range(5, w+15, 10):
        pygame.draw.rect(screen, gray, [x, 5, 8, 8])
        pygame.draw.rect(screen, gray, [x, h+15, 8, 8])

    for x in range(5, h+15, 10):
        pygame.draw.rect(screen, gray, [5, x, 8, 8])
        pygame.draw.rect(screen, gray, [w+15, x, 8, 8])

    pygame.draw.rect(screen, gray, [w+15, h + 15, 8, 8])

    pygame.display.flip()
    step = step + 1

pygame.quit()

