import pygame as pg
import random
from rules import GuardRules
import sys
import yaml

sys.path.append(".")
with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

MAP = config["image"]["path"]
GREEN = config["color"]["target-hex"]

class BoidGuard(GuardRules):

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
        position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        
        # check if the pixel is white
        while self.image.get_at((int(position.x), int(position.y))) != pg.Color('white'):
            position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return position
    
    def draw(self, screen):
        pg.draw.circle(screen, 'blue', self.position, 5)

    def is_black(self, position):
        if position.x < 0 or position.y < 0 or position.x > self.width - 1 or position.y >= self.height - 1:
            return self.image.get_at((int(position.x), int(position.y))) == pg.Color('black')
        return True
    
    def is_green(self, position):
        return self.image.get_at((int(position.x), int(position.y))) == pg.Color(GREEN)
    
    def is_border(self, position):
        return position.x < 0 or position.y < 0 or position.x > self.width - 1 or position.y >= self.height - 1
    
    def update(self, boidguards, ALIGNMENT, COHESION, SEPARATION): #############
        
        # ant in the range
        neighbors = GuardRules.find_neighbors(self, boidguards)

        # alignment
        alignment = ALIGNMENT * self.velocity
        # cohesion
        cohesion = COHESION * GuardRules.fly_towards_center(self, neighbors)
        # separation
        separation = SEPARATION * GuardRules.keep_distance_away(self, neighbors)

        # update velocity
        self.velocity += alignment + cohesion + separation

        # limit the speed of the boids
        self.velocity.scale_to_length(5)


        # update position
        self.position += self.velocity

        # wrap the position of the boidù
        GuardRules.bound_position(self)
