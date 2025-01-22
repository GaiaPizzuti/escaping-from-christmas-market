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

        # boolean to check if the boid has reached the target
        self.reached = False
    
    def set_position(self):
        position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        
        # check if the pixel is white
        while self.image.get_at((int(position.x), int(position.y))) != pg.Color('white'):
            position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return position
    
    def draw(self, screen):
        pg.draw.circle(screen, 'blue', self.position, 5)

    def is_black(self, position):
        if position.x > 0 and position.y > 0 and position.x < self.width - 100 and position.y < self.height - 100:
            return self.image.get_at((int(position.x), int(position.y))) == pg.Color('black')
        return False
    
    def is_green(self, position):
        if position.x > 0 and position.y > 0 and position.x < self.width - 100 and position.y < self.height - 100:
            return self.image.get_at((int(position.x), int(position.y))) == pg.Color(GREEN)
        return False
    
    def avoid_obstacles(self):
        # base direction
        avoidance_force = pg.Vector2(0, 0)

        # check the other directions
        for angle in range(0, 360, 45):
            direction = self.velocity.rotate(angle)
            check_position = self.position + direction.normalize() * self.radius

            if self.is_black(check_position):
                # invert the direction to avoid the obstacle
                avoidance_force += -direction
        
        return avoidance_force
    
    def update(self, boids, ALIGNMENT, COHESION, SEPARATION):
        
        # ant in the range
        neighbors = GuardRules.find_neighbors(self, boids)

        # alignment
        alignment = ALIGNMENT * self.velocity

        # cohesion
        cohesion = COHESION * GuardRules.fly_towards_center(self, neighbors)

        # separation
        separation = SEPARATION * GuardRules.keep_distance_away(self, neighbors)

        possible_velocity = self.velocity + alignment + cohesion + separation
        possible_position = self.position + possible_velocity

        if self.is_black(possible_position):
            # avoid obstacles
            avoidance_force = self.avoid_obstacles()
            self.velocity += avoidance_force
        
        # limit the speed of the boids
        self.velocity.scale_to_length(2)
        
        # update position
        self.position += self.velocity

        # wrap the position of the boid
        GuardRules.bound_position(self)

        if self.is_green(self.position):
            self.reached = True
            self.velocity = pg.Vector2(0, 0)