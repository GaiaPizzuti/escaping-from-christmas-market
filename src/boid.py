import pygame as pg
import random
from rules import Rules
import sys
import yaml

sys.path.append(".")
with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

MAP = config["image"]["path"]
GREEN = config["color"]["target-hex"]

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

    def draw(self, screen):
        pg.draw.circle(screen, 'red', self.position, 5)
    
    def is_black(self, position):
        if position.x < 0 or position.y < 0 or position.x > self.width - 1 or position.y >= self.height - 1:
            return self.image.get_at((int(position.x), int(position.y))) == pg.Color('black')
        return True
    
    def is_green(self, position):
        return self.image.get_at((int(position.x), int(position.y))) == pg.Color(GREEN)
    
    def is_border(self, position):
        return position.x < 0 or position.y < 0 or position.x > self.width - 1 or position.y > self.height - 1
    
    def update(self, boids, ALIGNMENT, COHESION, SEPARATION):
        
        # ant in the range
        neighbors = Rules.find_neighbors(self, boids)

        # alignment
        alignment = ALIGNMENT * Rules.match_velocity(self, neighbors)
        # cohesion
        cohesion = COHESION * Rules.fly_towards_center(self, neighbors)
        # separation
        separation = SEPARATION * Rules.keep_distance_away(self, neighbors)

        # update velocity
        self.velocity += alignment + cohesion + separation

        # limit the speed of the boids
        self.velocity.scale_to_length(2)

        # update position
        self.position += self.velocity

        # wrap the position of the boid
        Rules.bound_position(self)