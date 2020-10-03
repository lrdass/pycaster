import pygame
import sys
import math
from numpy import arange
from pygame.locals import *
# import math

clock = pygame.time.Clock()

WINDOW = (720, 360)
screen = pygame.display.set_mode(WINDOW)

walls = [
    # pygame.Rect(300, 100, 300, 300),
    # pygame.Rect(150, 90, 100, 40),
    [[300, 100], [300, 300]]
]

# ray_position = pygame.Vector2(100, 200)

player = pygame.Vector2(180, 160)
fov = math.pi / 3 
ray_direction = pygame.Vector2(1, 0)

speed = pygame.Vector2(2, 2)


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


top_view_surface = pygame.surface.Surface((360,360))
first_person = pygame.surface.Surface((360,360))
pygame.draw.line(first_person, (0,0,255), (120, 120), (0,0))

pressed_keys = {"left": False, "right": False, "up": False, "down": False}


while True:

    screen.fill((0, 0, 0))

    top_view_surface.fill((0,0,0))
    first_person.fill((0,0,0))

    mouse = pygame.mouse.get_pos()
    # pygame.draw.line(screen, (255, 255, 255),
    #  (WINDOW[0]/2, WINDOW[1]/2), mouse, 1)
    
    for i in range(0, 360):
        player_direction = pygame.Vector2(mouse[0] - player.x, mouse[1] - player.y)
        if(player_direction.x == 0):
            player_direction.x = player.x
        angle_player = math.atan(player_direction.y / player_direction.x)

        angle = (angle_player - (fov / 2)) + ((i*fov)/360)
        ray_direction.update(player.x * math.cos(angle), player.y * math.sin(angle))
        
        ray_direction = ray_direction.normalize() * 3

        ray_distance = pygame.Vector2(
            player.x + ray_direction.x*20, player.y+ray_direction.y*20
        )

        pygame.draw.line(top_view_surface, (255, 255, 0), player, ray_distance)
        points = cast_ray(walls)
        if points:
            for point in points:
                pygame.draw.circle(top_view_surface, (255, 255, 0),
                                   (int(point.x), int(point.y)), 3, 3)
        
    for wall in walls:
        pygame.draw.line(top_view_surface, (255, 255, 0), (300, 100), (300, 300))
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pressed_keys["left"] = True
            if event.key == pygame.K_d:
                pressed_keys["right"] = True
            if event.key == pygame.K_w:
                pressed_keys["up"] = True
            if event.key == pygame.K_s:
                pressed_keys["down"] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                pressed_keys["left"] = False
            if event.key == pygame.K_d:
                pressed_keys["right"] = False
            if event.key == pygame.K_w:
                pressed_keys["up"] = False
            if event.key == pygame.K_s:
                pressed_keys["down"] = False

    if pressed_keys["left"]:  # == True is implied here
        player.x -= speed.x
    if pressed_keys["right"]:
        player.x += speed.x
    if pressed_keys["up"]:
        player.y -= speed.y
    if pressed_keys["down"]:
        player.y += speed.y

    screen.blit(top_view_surface, (0,0))
    screen.blit(first_person, (360,0))
    pygame.display.update()
    clock.tick(60)
