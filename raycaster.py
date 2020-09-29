import pygame
import sys
from pygame.locals import *
# import math

clock = pygame.time.Clock()

WINDOW = (480, 360)
screen = pygame.display.set_mode(WINDOW)

walls = [
    # pygame.Rect(300, 100, 300, 300),
    # pygame.Rect(150, 90, 100, 40),
    [[300, 100], [300, 300]]
]

# ray_position = pygame.Vector2(100, 200)

player = pygame.Vector2(0, 0)
ray_direction = pygame.Vector2(1, 0)


def cast_ray(walls):

    points_hit = []
    for wall in walls:
        x1 = wall[0][0]
        y1 = wall[0][1]

        x2 = wall[1][0]
        y2 = wall[1][1]

        x3 = player.x
        y3 = player.y
        x4 = (player + ray_direction).x
        y4 = (player + ray_direction).y

        den = (x1-x2) * (y3-y4) - (y1-y2) * (x3-x4)

        if den == 0:
            continue

        t = ((x1-x3) * (y3-y4) - (y1-y3) * (x3-x4)) / den
        u = - ((x1 - x2) * (y1-y3) - (y1 - y2) * (x1-x3)) / den

        if t > 0 and t < 1 and u > 0:
            x = x1 + t * (x2-x1)
            y = y1 + t * (y2-y1)
            points_hit.append(pygame.Vector2(x, y))

    return points_hit


while True:

    screen.fill((0, 0, 0))
    mouse = pygame.mouse.get_pos()
    # pygame.draw.line(screen, (255, 255, 255),
    #  (WINDOW[0]/2, WINDOW[1]/2), mouse, 1)

    ray_direction.update((mouse[0] - player.x) - ray_direction.x,
                         (mouse[1] - player.y) - ray_direction.y)
    ray_direction = ray_direction.normalize()

    ray_distance = pygame.Vector2(
        player.x + ray_direction.x*20, player.y+ray_direction.y*20
    )

    pygame.draw.line(screen, (255, 255, 0), player, ray_distance)

    for wall in walls:
        pygame.draw.line(screen, (255, 255, 0), (300, 100), (300, 300))

    points = cast_ray(walls)
    if points:
        for point in points:
            print(point)
            pygame.draw.circle(screen, (255, 255, 0),
                               (int(point.x), int(point.y)), 3, 3)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.y -= 5
            if event.key == pygame.K_s:
                player.y += 5
            if event.key == pygame.K_d:
                player.x += 5
            if event.key == pygame.K_a:
                player.x -= 5
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
