import pygame as pg
import random
from rules import Rules
import sys
import yaml

sys.path.append(".")
with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

MAP = config["image"]["path"]
GREEN = config["color"]["target"]

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

        # radius of the boid
        self.radius = 50
    
    def set_position(self):
        print("Setting position")
        position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))

        print(position)
        
        # check if the pixel is white
        while self.image.get_at((int(position.x), int(position.y))) != pg.Color('white'):
            position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            print(position)
        return position
    
    def is_border(self):
        return self.position.x == 0 or self.position.y == 0 or self.position.x == self.width - 1 or self.position.y == self.height - 1

    def draw(self, screen):
        pg.draw.circle(screen, 'red', self.position, 5)
    
    def is_black(self):
        return self.image.get_at((int(self.position.x), int(self.position.y))) == pg.Color('black')
    
    def is_green(self):
        return self.image.get_at((int(self.position.x), int(self.position.y))) == pg.Color('green')
    
    def update(self, boids, boidguards, ALIGNMENT, COHESION, SEPARATION):
        
        # boid in the range
        neighbors = Rules.find_neighbors(self, boids, boidguards)

        # boidguards in range
        GUARDneighbors = Rules.find_neighbors_boidguards(self,boidguards)

        # alignment
        alignment = ALIGNMENT * Rules.match_velocity(self, neighbors, GUARDneighbors, 3)
        # cohesion
        cohesion = COHESION * Rules.fly_towards_center(self, neighbors)
        # separation
        separation = SEPARATION * Rules.keep_distance_away(self, neighbors)

        # update velocity
        self.velocity += alignment + cohesion + separation

        # check if the new position is black
        if self.is_border() or self.is_black():
            # send the boid back
            self.velocity = -self.velocity

        # check if the new position is green
        if not self.is_green():

            # limit the speed of the boids
            self.velocity.scale_to_length(5)
            
            # update position
            self.position += self.velocity

            # wrap the position of the boidù
            Rules.bound_position(self)