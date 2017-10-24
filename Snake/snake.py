
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

    def all_positions(self, position_list=None):
        if position_list is None:
            position_list = []
        position_list.append((self.x, self.y))
        if self.child is not None:
            self.child.all_positions(position_list)
        return position_list


def random_food():
    return (player_size/2) + randint(0, int(w/player_size)-1)*player_size, (player_size/2) + randint(0, int(h/player_size)-1)*player_size,


def snake():
    start_w, start_h = (player_size/2)+int(w/player_size)/2*player_size, (player_size/2)+int(h/player_size)/2*player_size
    t3 = Node(start_w - 3 * player_size, start_h)
    t2 = Node(start_w - 2 * player_size, start_h, t3)
    t1 = Node(start_w - 1 * player_size, start_h, t2)
    return Node(start_w, start_h, t1)


def draw_square(color, x, y, height, width=None):
    if width is None:
        width = height
    pygame.draw.rect(screen, color, [x-width/2, y-height/2, width, height])


pygame.init()
w, h = 810, 630
screen = pygame.display.set_mode((w, h))
player_size = 18
expanded_size = 22

running = 1
direction = Direction.RIGHT
head = snake()
food_x, food_y = random_food()
expand_points = []
step = 0
score = 0
pause = False
dead = False

# Colors
green = (172, 184, 80)
gray = (101, 81, 38)
font = pygame.font.SysFont("monospace", 40, True)

while running:
    # BACKGROUND
    screen.fill(green)

    if dead:
        running = 1
        direction = Direction.RIGHT
        head = snake()
        food_x, food_y = random_food()
        expand_points = []
        step = 0
        score = 0
        pause = False
        dead = False
        new_food = True

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
        if head.x <= 0:
            head.x = w - player_size/2
        elif head.x >= w:
            head.x = player_size/2
        if head.y <= 0:
            head.y = h - player_size/2
        elif head.y >= h:
            head.y = player_size/2

        # Check if crash with tail
        all_positions = head.child.all_positions()
        if (head.x, head.y) in all_positions:
            dead = True
            continue

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
    draw_square(gray, food_x, food_y, player_size)
    draw_square(green, food_x, food_y, player_size / 3)
    for i in {-1, 1}:
        for j in {-1, 1}:
            draw_square(green, food_x + (i*player_size/3), food_y + (j*player_size/3), player_size/3)

    # EATING
    if abs(head.x - food_x) < player_size/2+1 and abs(head.y - food_y) < player_size/2+1:
        expand_points.append((head.x, head.y))
        food_x, food_y = random_food()
        score += 1

    score_label = font.render(str(score), 1, gray)
    screen.blit(score_label, (w-20-(len(str(score))*20), 10))
    pygame.display.flip()
    step = step + 1

pygame.quit()

