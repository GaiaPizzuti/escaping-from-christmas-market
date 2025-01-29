import pygame as pg
import random
import numpy as np
import yaml
import sys

from rules import Rules

sys.path.append(".")
with open("utils/config.yaml", "r") as file:
    config = yaml.safe_load(file)

MAP = config["image"]["path"]
GREEN = config["color"]["target-hex"]
BLACK = config["color"]["border-hex"]

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

        # radius to see the other boids
        self.radius = 50

        # radius to see the other boidguards
        self.GuardRadius = 100

        # radius to see the target
        self.TargetRadius = 30

        # set discipline
        self.discipline = np.random.uniform(0.7,0.9)

        # boolean to check if the boid has reached the target
        self.reached = False
    
    def set_position(self):
        """
        create a random position and check if the pixel is white

        Returns:
        -------
        pg.Vector2
            the position of the boid
        """
        position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        
        while self.image.get_at((int(position.x), int(position.y))) != pg.Color('white'):
            position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return position

    def draw(self, screen):
        """
        draw the boid on the screen with a red circle of radius 4
        """
        pg.draw.circle(screen, 'red', self.position, 4)
    
    def avoid_obstacles(self):
        """
        Function to avoid obstacles and search a new possibile direction by rotating the velocity

        Returns:
        -------
        pg.Vector2
            the new direction to avoid obstacles
        """
        avoidance_force = pg.Vector2(0, 0)

        # check the other directions
        for angle in range(0, 360, 45):
            direction = self.velocity.rotate(angle)
            if direction.length() != 0:
                direction = direction.normalize()
            check_position = self.position + direction * self.radius

            if self.is_black(check_position):
                # invert the direction to avoid the obstacle
                avoidance_force -= direction
        
        return avoidance_force
    
    def is_any_black(self, target_position):
        """
        Function to check if there is a black pixel in the path of the boid

        Parameters:
        ----------
        target_position : pg.Vector2
            the position of the target
        
        Returns:
        -------
        bool
            True if there is a black pixel in the path of the boid, False otherwise
        """
        direction = target_position - self.position
        distance = int(direction.length())

        if distance == 0:
            return False

        step = direction.normalize()  

        for i in range(distance + 1):  
            check_position = self.position + step * i
            if self.is_black(check_position):
                return True  

        return False  

    def is_black(self, position):
        """
        Function to check if the pixel is black

        Parameters:
        ----------
        position : pg.Vector2
            the position of the pixel
        
        Returns:
        -------
        bool
            True if the pixel is black, False otherwise
        """
        if position.x > 0 and position.y > 0 and int(position.x) < self.width - 100 and int(position.y) < self.height - 100:
            return self.image.get_at((int(position.x), int(position.y))) == pg.Color(BLACK)
        return False

    def is_green(self):
        """
        Function to check if the pixel is green

        Returns:
        -------
        bool
            True if the pixel is green, False otherwise
        """
        return self.image.get_at((int(self.position.x), int(self.position.y))) == pg.Color(GREEN)


    def search_target(self, targets, radius):
        """
        Function to search a smart point to move

        Parameters:
        ----------
        targets : list
            list of targets
        radius : int
            the radius to search the target

        Returns:
        -------
        pg.Vector2
            the position of the target reached
        """
        closest_target = None
        min_distance = float("inf")

        for target in targets:
            distance = self.position.distance_to(target)
            if distance < radius and distance < min_distance:
                closest_target = target
                min_distance = distance
        
        return closest_target
    
    def update(self, boids, boidguards, ALIGNMENT, COHESION, SEPARATION, green_reached, TARGET):
        """
        Function to update the position of the boid

        Parameters:
        ----------
        boids : list
            list of boids
        boidguards : list
            list of boidguards
        ALIGNMENT : float
            alignment factor
        COHESION : float
            cohesion factor
        SEPARATION : float
            separation factor
        green_reached : list
            list of reached targets
        TARGET : list
            list of targets

        Returns:
        -------
        pg.Vector2
            the position of the target reached
        """

        closest_target = self.search_target(TARGET, self.TargetRadius)

        if closest_target != None:
            direction = closest_target - self.position

            if direction.length() != 0:
                direction = direction.normalize()

            # update the velocity
            self.velocity += direction
        #elif green_reached:

        #    closest_target = self.search_target(green_reached, self.GuardRadius)
        #    if closest_target != None:
        #        direction = closest_target - self.position

        #        if direction.length() != 0:
        #            direction = direction.normalize()

                # update the velocity
        #        self.velocity += direction
        else:
            
            # find the neighbors
            neighbors = Rules.find_neighbors(self, boids)

            # find the boidguards in the radius
            GUARDneighbors = Rules.find_neighbors_boidguards(self,boidguards)

            # apply the rules
            alignment = ALIGNMENT * Rules.match_velocity(self, neighbors, GUARDneighbors)
            cohesion = COHESION * Rules.fly_towards_center(self, neighbors)
            separation = SEPARATION * Rules.keep_distance_away(self, neighbors)
            
            # update the velocity
            next_velocity = self.velocity + alignment + cohesion + separation  

            # check if there is an obstacle in the path     
            possible_position = self.position + next_velocity

            if self.is_any_black(possible_position):
                next_velocity += self.avoid_obstacles()
                
            self.velocity = next_velocity

        # limit the speed of the boids
        if self.velocity.length() > 2:
            self.velocity.scale_to_length(2)
            
        self.position += self.velocity

        # avoid the borders
        Rules.bound_position(self)

        if self.is_green():
            self.reached = True
            return self.position
