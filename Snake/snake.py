
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

    def move(self, d):
        if d == Direction.UP:
            self.y -= 5
        elif d == Direction.RIGHT:
            self.x += 5
        elif d == Direction.DOWN:
            self.y += 5
        elif d == Direction.LEFT:
            self.x -= 5


pygame.init()
w, h = 800, 600
screen = pygame.display.set_mode((w+30, h+30))
object_size = 15

running = 1
direction = Direction.RIGHT
head = Node(w/2, h/2)
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
                print("Going up")
                direction = Direction.UP
            elif event.key == 275 and (direction == Direction.UP or direction == Direction.DOWN):
                print("Going right")
                direction = Direction.RIGHT
            elif event.key == 274 and (direction == Direction.LEFT or direction == Direction.RIGHT):
                print("Going down")
                direction = Direction.DOWN
            elif event.key == 276 and (direction == Direction.UP or direction == Direction.DOWN):
                print("Going left")
                direction = Direction.LEFT

    # BACKGROUND
    screen.fill(green)

    node = head
    while node is not None:
        pygame.draw.rect(screen, gray, [node.x, node.y, object_size, object_size])
        node = node.child

    if step % 5 == 0:
        head.move(d=direction)

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

