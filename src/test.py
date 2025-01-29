import pygame as pg
import sys

sys.path.append(".")

from boid import Boid
from boidguard import BoidGuard
from utils.utils import get_config, find_target_positions, plot_boids_data
from utils.create_result import create_file

def run(WIDTH, HEIGHT, BOIDS, BOIDGUARDS, alignment, cohesion, separation, TARGET, MAP, GREEN, BLACK):
    pg.init()

    # create the map for the simulation
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    image = pg.image.load(MAP).convert()
    pg.display.set_caption("Boids")
    screen.blit(image, (0, 0))
    pg.display.flip()

    # create boids
    boids = [Boid(WIDTH, HEIGHT) for _ in range(BOIDS)]

    # create boidguards
    boidguards = [BoidGuard(WIDTH, HEIGHT, MAP, GREEN, BLACK) for _ in range(BOIDGUARDS)]

    # list of logs to store and plot the data
    time_log = []           
    boids_log = []          
    boidguards_log = []

    # dict to store the data that we are going to write in the result file
    interval_data = {
        30: None, 60: None, 90: None, 120: None, 150: None,
        180: None, 210: None, 240: None, 270: None, 300: None,
        330: None, 360: None, 390: None, 420: None, 450: None,
        480: None, 510: None, 540: None, 570: None, 600: None,
        630: None, 660: None, 690: None, 720: None, 750: None,
        780: None, 810: None, 840: None, 870: None, 900: None,
        930: None, 960: None, 990: None, 1020: None, 1050: None,
        1080: None, 1110: None, 1140: None, 1170: None, 1200: None,
        1230: None, 1260: None, 1290: None, 1320: None, 1350: None,
        1380: None, 1410: None, 1440: None, 1470: None, 1500: None,
        1530: None, 1560: None, 1590: None, 1620: None, 1650: None,
        1680: None, 1710: None, 1740: None, 1770: None, 1800: None,
    }

    # frame counter
    count = 0

    # list of reached targets
    greens_reached = list()

    running = True
    while running:
        count+=1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # reset the initial map
        screen.blit(image, (0, 0))

        # boidguards draw and update
        for boidg in boidguards:
            boidg.draw(screen)
            position_reached = boidg.update(TARGET)

            # insert the target in the list of reached targets
            if position_reached != None:
                greens_reached.append(position_reached)
            
            # if the boidguard reached the target, remove it from the list
            if boidg.reached:
                boidguards.remove(boidg)
        
        # boids draw and update
        for boid in boids:
            boid.draw(screen)
            position_reached = boid.update(boids, boidguards, alignment, cohesion, separation, TARGET)

            # insert the target in the list of reached targets
            if position_reached != None:
                greens_reached.append(position_reached)
            
            # if the boid reached the target, remove it from the list
            if boid.reached:
                boids.remove(boid)

        # collect data
        if count % 2 == 0:
            time_log.append(count/2)
            boids_log.append(len(boids))
            boidguards_log.append(len(boidguards))

        # insert the result in the dict
        for t in interval_data.keys():
            if interval_data[t] is None and count == (2*t):
                interval_data[t] = (len(boids), len(boidguards))

        # update the screen
        pg.display.flip()

        # force break after 5 simulated minutes or when there are no more boids or boidguards left
        threshold = BOIDS * 0.05
        if count == 600 or (len(boids) < threshold):
            running = False

    pg.quit()
    
    # Plot data
    if time_log and boids_log and boidguards_log:
        plot_boids_data(time_log, boids_log, boidguards_log)
    else: 
        print("No data to plot")

    # Create result file
    create_file(BOIDS, BOIDGUARDS, interval_data)


if __name__ == "__main__":
    WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION = get_config()
    
    # create the map using pygame in order to search the targets
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    image = pg.image.load(MAP).convert()
    
    # find all the target points (the green ones)
    TARGET = find_target_positions(image, OBJ_COLOR, WIDTH, HEIGHT)
    
    run(WIDTH, HEIGHT, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION, TARGET, MAP, OBJ_COLOR, BORDER_COLOR)
