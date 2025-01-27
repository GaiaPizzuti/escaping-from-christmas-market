import sys
import yaml
import random
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt

from boid import Boid
from boidguard import BoidGuard
from utils.utils import get_config, find_target_positions


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

    # Logger per plottare i dati
    time_log = []           # Tempo simulato
    boids_log = []          # Numero di boids
    boidguards_log = []     # Numero di boidguards
    elapsed_time = 0        # Tempo cumulativo

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # reset the initial map
        screen.blit(image, (0, 0))

        for boid in boids:
            boid.draw(screen)
            boid.update(boids, boidguards, alignment, cohesion, separation)
            if boid.reached:
                print("Boid reached the target")
                boids.remove(boid)


        for boidg in boidguards:
            boidg.draw(screen)
            boidg.update(boidguards, TARGET)
            if boidg.reached:
                print("BoidGuard reached the target")
                boidguards.remove(boidg)

        # update the screen
        pg.display.flip()
        clock.tick(60)
    pg.quit()

    # Plot dei dati raccolti
    plt.figure(figsize=(10, 6))
    plt.plot(time_log, boids_log, label="Boids", color="blue", linewidth=2)
    plt.plot(time_log, boidguards_log, label="BoidGuards", color="red", linewidth=2)
    plt.xlabel("Tempo (s)")
    plt.ylabel("Numero")
    plt.title("Evoluzione del numero di Boids e BoidGuards")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION = get_config()
    
    #Questo l'ho tolto dalla run function
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    image = pg.image.load(MAP).convert()
    
    TARGET = find_target_positions(image, OBJ_COLOR, WIDTH, HEIGHT)
    
    run(WIDTH, HEIGHT, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION, TARGET)
