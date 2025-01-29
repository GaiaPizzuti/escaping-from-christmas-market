import sys
import yaml
import random
import pygame as pg
import numpy as np
import matplotlib.pyplot as plt

from boid import Boid
from boidguard import BoidGuard
from utils.utils import get_config, find_target_positions, plot_boids_data
from utils.create_result import create_file

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

    # Logger per plottare i dati
    time_log = []           
    boids_log = []          
    boidguards_log = []     
    elapsed_time = 0        

    interval_data = {
        30: None, 60: None, 90: None, 120: None, 150: None,
        180: None, 210: None, 240: None, 270: None, 300: None
    }

    count=0
    running = True
    greens_reached = list()
    while running:
        count+=1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # reset the initial map
        screen.blit(image, (0, 0))

        for boid in boids:
            boid.draw(screen)
            position_reached = boid.update(boids, boidguards, alignment, cohesion, separation, greens_reached, TARGET)
            if position_reached != None:
                greens_reached.append(position_reached)
            
            if boid.reached:
                boids.remove(boid)
            

        for boidg in boidguards:
            boidg.draw(screen)
            position_reached = boidg.update(boidguards, TARGET)
            if position_reached != None:
                greens_reached.append(position_reached)
            if boidg.reached:
                boidguards.remove(boidg)

        dt = clock.tick(60) / 1000  
        elapsed_time += dt

        # Collect data
        if count % step_size == 0:
            time_log.append(count/2)
            boids_log.append(len(boids))
            boidguards_log.append(len(boidguards))


        for t in interval_data.keys():
            if interval_data[t] is None and count == (2*t):
                interval_data[t] = (len(boids), len(boidguards))

        # Update the screen
        pg.display.flip()
        clock.tick(60)

        # Force break after 5 minutes or when there are no more boids or boidguards left
        if count == 600 or (not boids and not boidguards):
            running = False

    pg.quit()

    print(interval_data)

    
    # Plot data
    if time_log and boids_log and boidguards_log:
        plot_boids_data(time_log, boids_log, boidguards_log)
    else: 
        print("No data to plot")

    # Create result file
    create_file(BOIDS, BOIDGUARDS, interval_data)


if __name__ == "__main__":
    WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION = get_config()
    
    
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    image = pg.image.load(MAP).convert()
    
    TARGET = find_target_positions(image, OBJ_COLOR, WIDTH, HEIGHT)
    
    run(WIDTH, HEIGHT, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION, TARGET)
