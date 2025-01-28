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
        return self.image.get_at((int(position.x), int(position.y))) == pg.Color(GREEN)
    
    def is_border(self, position):
        return position.x < 0 or position.y < 0 or position.x > self.width - 1 or position.y >= self.height - 1
    
    def update(self, boidguards, target_positions):
        if not target_positions:
            print("No target found")
            return  

        closest_target = min(target_positions, key=lambda pos: (self.position - pos).length())

        direction = closest_target - self.position

        if direction.length() != 0:
            direction = direction.normalize()

        speed_factor = 2  
        self.velocity += direction * speed_factor

        max_speed = 0.5
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed

        self.velocity.scale_to_length(0.3)

        self.position += self.velocity

        GuardRules.bound_position(self)

        if self.is_green(self.position):
            self.reached = True