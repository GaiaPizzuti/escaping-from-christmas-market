import pygame as pg
import random
import numpy as np
from rules import Rules
import sys
import yaml

sys.path.append(".")
with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

MAP = config["image"]["path"]
GREEN = config["color"]["target-hex"]
BLACK = config["color"]["obstacle-hex"]

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
        self.GuardRadius = 100
        self.TargetRadius = 30

        # set discipline
        self.discipline = np.random.uniform(0.7,0.9)

        # boolean to check if the boid has reached the target
        self.reached = False
    
    def set_position(self):
        position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        
        # check if the pixel is white
        while self.image.get_at((int(position.x), int(position.y))) != pg.Color('white'):
            position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return position

    def draw(self, screen):
        pg.draw.circle(screen, 'red', self.position, 5)
    
    def avoid_obstacles(self):
        avoidance_force = pg.Vector2(0, 0)

        # check the other directions
        for angle in range(0, 360, 45):
            direction = self.velocity.rotate(angle)
            if direction.length() != 0:
                direction = direction.normalize()
            check_position = self.position + direction * self.radius

            if self.is_black(check_position):
                # invert the direction to avoid the obstacle
                avoidance_force += -direction
        
        return avoidance_force
    
    def is_any_black(self, position):
        
        direction = (self.position - position).normalize()
        distance = int(self.position.distance_to(position))

        for i in range(distance):
            check_position = self.position + direction * i
            if self.is_black(check_position):
                return True
        return False

    def is_black(self, position):
        if position.x > 0 and position.y > 0 and int(position.x) < self.width - 100 and int(position.y) < self.height - 100:
            return self.image.get_at((int(position.x), int(position.y))) == pg.Color(BLACK)
        return False

    def is_green(self, position):
        if position.x > 0 and position.y > 0 and int(position.x) < self.width - 100 and int(position.y) < self.height - 100:
            return self.image.get_at((int(position.x), int(position.y))) == pg.Color(GREEN)
        return False

    
    def update(self, boids, boidguards, ALIGNMENT, COHESION, SEPARATION, green_reached, TARGET):
        
        closest_target = None
        min_distance = float("inf")
        nearby_targets = False

        for i in TARGET:
            distance = self.position.distance_to(i)
            if distance < self.TargetRadius and distance < min_distance:
                closest_target = i
                min_distance = distance
                nearby_targets = True

                
        if nearby_targets:
            direction = closest_target - self.position

            if direction.length() != 0:
                direction = direction.normalize()

            # Aggiorna la velocità, scalata da un fattore di velocità
            speed_factor = 2  # Velocità di movimento del Boid 
            self.velocity += direction * speed_factor

        else:

            neighbors = Rules.find_neighbors(self, boids, boidguards)
            GUARDneighbors = Rules.find_neighbors_boidguards(self,boidguards)

            alignment = ALIGNMENT * Rules.match_velocity(self, neighbors, GUARDneighbors)
            cohesion = COHESION * Rules.fly_towards_center(self, neighbors)
            separation = SEPARATION * Rules.keep_distance_away(self, neighbors)
            
            next_velocity = self.velocity + alignment + cohesion + separation       
            possible_position = self.position + next_velocity
            direction2 = Rules.tend_to_place(self,green_reached)
            possible_position2 = self.position + (direction2 or pg.Vector2(0,0))


            if self.is_any_black(possible_position):
                avoidance_force = self.avoid_obstacles()
                next_velocity += avoidance_force

            self.velocity = next_velocity

            if self.is_any_black(possible_position2) == False and self.position != possible_position2:
                self.velocity = direction2

        # limit the speed of the boids
        #if np.linalg.norm(self.velocity) > 0:self.velocity = self.velocity / np.linalg.norm(self.velocity) * 2
        if self.velocity.length() > 2:
            self.velocity.scale_to_length(2)
            
        self.position += self.velocity

        Rules.bound_position(self)

        desired_position = None

        if self.is_green(self.position):
            desired_position = self.position ######### INPUT of tend_to_place()
            print("Target reached")
            self.reached = True
            self.velocity = pg.Vector2(0, 0)
        
        return desired_position
