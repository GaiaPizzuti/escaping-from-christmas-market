import sys
import yaml
import random
import pygame as pg

from boid import Boid

sys.path.append(".")

with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

WIDTH = config["image"]["width"]
HEIGHT = config["image"]["height"]
BORDER_COLOR = config["color"]["border"]
OBJ_COLOR = config["color"]["target"]

MAP = config["image"]["path"]
BOIDS = config["people"]["num"]

def run(WIDTH, HEIGHT, BOIDS, alignment, cohesion, separation):
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    image = pg.image.load(MAP).convert()
    pg.display.set_caption("Boids")
    screen.blit(image, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()

    # create boids
    boids = [Boid(WIDTH, HEIGHT) for _ in range(BOIDS)]

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        for boid in boids:
            boid.update(boids, alignment, cohesion, separation)
            boid.draw(screen)

        pg.display.flip()
        clock.tick(60)
    pg.quit()

if __name__ == "__main__":
    run(WIDTH, HEIGHT, BOIDS, 0.5, 0.5, 0.5)