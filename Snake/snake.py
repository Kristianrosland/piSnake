import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((830, 630))

running = 1


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        else:
            print event

    # BACKGROUND
    screen.fill((172, 184, 80))

    for x in range(5, 810, 10):
        pygame.draw.rect(screen, (0, 0, 0), [x, 5, 10, 10])
        pygame.draw.rect(screen, (0, 0, 0), [x, 615, 10, 10])

    for x in range(5, 615, 10):
        pygame.draw.rect(screen, (0, 0, 0), [5, x, 10, 10])
        pygame.draw.rect(screen, (0, 0, 0), [815, x, 10, 10])

    pygame.display.flip()

pygame.quit()

