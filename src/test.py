import sys
import yaml
import random
import pygame as pg
import numpy as np

from boid import Boid
from boidguard import BoidGuard
from utils.utils import get_config, find_target_positions

step_size = 10


def run(WIDTH, HEIGHT, BOIDS, BOIDGUARDS, alignment, cohesion, separation, TARGET):
    pg.init()

    screen = pg.display.set_mode((WIDTH, HEIGHT))
    image = pg.image.load(MAP).convert()
    pg.display.set_caption("Boids")
    screen.blit(image, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()

    # create boids
    boids = [Boid(WIDTH, HEIGHT) for _ in range(BOIDS)]
    boidguards = [BoidGuard(WIDTH, HEIGHT) for _ in range(BOIDGUARDS)]

    # initialize tend to position
    #desired_position = np.zeros(2, dtype=np.int32)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # reset the initial map
        screen.blit(image, (0, 0))
        greens_reached = list()

        for boid in boids:
            boid.draw(screen)
            position_reached = boid.update(boids, boidguards, alignment, cohesion, separation, greens_reached)
            if position_reached != None:
                greens_reached.append(position_reached)
            

            if boid.reached:
                print("Boid reached the target")
                boids.remove(boid)
            

        for boidg in boidguards:
            boidg.draw(screen)
            position_reached = boidg.update(boidguards, TARGET)
            if position_reached != None:
                greens_reached.append(position_reached)
            if boidg.reached:
                print("BoidGuard reached the target")
                boidguards.remove(boidg)

        # update the screen
        pg.display.flip()
        clock.tick(60)
    pg.quit()

if __name__ == "__main__":
    WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION = get_config()
    
    #Questo l'ho tolto dalla run function
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    image = pg.image.load(MAP).convert()
    
    TARGET = find_target_positions(image, OBJ_COLOR, WIDTH, HEIGHT)
    
    run(WIDTH, HEIGHT, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION, TARGET)
