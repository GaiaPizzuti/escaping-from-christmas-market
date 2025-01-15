import pygame as pg
import random
from rules import Rules
import sys
import yaml

sys.path.append(".")
with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

MAP = config["image"]["path"]

class Boid(Rules):

    def __init__(self, WIDTH, HEIGHT):

        # Rules init
        super().__init__(WIDTH, HEIGHT)

        # boid image
        self.image = pg.image.load(MAP).convert()

        # initial random position of the boid
        self.position = self.set_position()

        # initial random velocity of the boid
        self.velocity = pg.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

        # radius of the ant
        self.radius = 50
    
    def set_position(self):
        position = pg.Vector2(random.randint(0, self.width), random.randint(0, self.height))
        
        # check if the pixel is white
        while self.image.get_at((int(position.x), int(position.y))) != pg.Color('white'):
            position = pg.Vector2(random.randint(0, self.width), random.randint(0, self.height))
        return position
    
    def draw(self, screen):
        pg.draw.circle(screen, 'red', self.position, 5)
    
    def update(self, boid, alignment, cohesion, separation):
        
        # ant in the range
        neighbors = Rules.find_neighbors(self, boid)

        # alignment
        alignment = Rules.match_velocity(self, neighbors)