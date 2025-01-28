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
    time_log = []           
    boids_log = []          
    boidguards_log = []     
    elapsed_time = 0        

    interval_data = {
        30: None, 60: None, 90: None, 120: None, 150: None,
        180: None, 210: None, 240: None, 270: None, 300: None
    }

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

        dt = clock.tick(60) / 1000  
        elapsed_time += dt

        # Collect data
        time_log.append(elapsed_time)
        boids_log.append(len(boids))
        boidguards_log.append(len(boidguards))


        for t in interval_data.keys():
            if interval_data[t] is None and elapsed_time >= t:
                interval_data[t] = (len(boids), len(boidguards))

        # Force break after 5 minutes or when there are no more boids or boidguards left
        if elapsed_time > 300 or (not boids and not boidguards):
            running = False

        # Update the screen
        pg.display.flip()
        clock.tick(60)
    pg.quit()

    print(interval_data)

    with open("./src/results.csv", "a") as f:
        # Prima colonna: numero iniziale di boids
        # Seconda colonna: numero iniziale di boidguards * 100
        # Colonne successive: boids e boidguards a intervalli di tempo
        f.write(f"{BOIDS},{BOIDGUARDS}," + 
                ",".join(f"{b},{g}" for val in interval_data.values() if val is not None and len(val) == 2 and (b := val[0]) is not None and (g := val[1]) is not None) + "\n")

    # Plot data
    if time_log and boids_log and boidguards_log:
        plt.figure(figsize=(10, 6))
        plt.plot(time_log, boids_log, label="Boids", color="red", linewidth=2)
        plt.plot(time_log, boidguards_log, label="BoidGuards", color="blue", linewidth=2)
        plt.xlabel("Time (s)")
        plt.ylabel("Numero")
        plt.title("Evolution of number of Boids and BoidGuards")
        plt.legend()
        plt.grid()
        plt.show()
    else: 
        print("No data to plot")

if __name__ == "__main__":
    WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION = get_config()
    
    
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    image = pg.image.load(MAP).convert()
    
    TARGET = find_target_positions(image, OBJ_COLOR, WIDTH, HEIGHT)
    
    run(WIDTH, HEIGHT, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION, TARGET)
