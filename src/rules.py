import pygame as pg
import numpy as np

class Rules():

    def __init__(self, WIDTH, HEIGHT):

        self.width = WIDTH
        self.height = HEIGHT

    def find_neighbors(self, boids):
        """
        Function to find the neighbors of the boid

        Parameters:
        -----------
        boids: list
            list of boids

        Returns:
        --------
        list
            list of neighbors
        """
        neighbors = []
        for boid in boids:
            if boid.position != self.position:
                if self.position.distance_to(boid.position) < self.radius:
                    neighbors.append(boid)
        return neighbors

    def find_neighbors_boidguards(self, boidguards):
        """
        Function to find the boidguards in the neighborhood of the boid
        """
        neighborsguard = []
        for boidg in boidguards:
            if boidg.position != self.position:
                if self.position.distance_to(boidg.position) < self.GuardRadius:
                    neighborsguard.append(boidg)
        return neighborsguard
    
    def match_velocity(self, boids, boidguards):
        """
        Alignment rule: boids try to match the velocity of their neighbors
        
        Parameters:
        -----------
        boids: list
            list of boids
        boidguards: list
            list of boidguards

        Returns:
        --------
        pg.Vector2
            the updated velocity
        """
        velocity = pg.Vector2(0, 0)
        velocityg = pg.Vector2(0, 0)
        k = self.discipline

        for boid in boids:
            velocity += boid.velocity
        for guards in boidguards:
            velocityg += guards.velocity

        if len(boids) > 1:
            velocity /= (len(boids))
            if len(boidguards) > 1:
                velocityg /= (len(boidguards))
            velocity = (velocity*(1-k)+velocityg*k)
            return (velocity - self.velocity) / 8
        
        return pg.Vector2(0, 0)

    def fly_towards_center(self, boids):
        """
        Cohesion rule: boids try to fly towards the center of mass of neighboring boids

        Parameters:
        -----------
        boids: list
            list of boids
        
        Returns:
        --------
        pg.Vector2
            the updated direction
        """
        center = pg.Vector2(0, 0)
        for boid in boids:
            if boid.position != self.position:
                center += boid.position
            return (center - self.position) / 100
        return pg.Vector2(0, 0)

    def keep_distance_away(self, boids, range=9):
        """
        Separation rule: boids try to keep a small distance away from other objects (boids, obstacles)

        Parameters:
        -----------
        boids: list
            list of boids
        range: int
            the range of the separation
        
        Returns:
        --------
        pg.Vector2
            the updated direction
        """
        distance = pg.Vector2()
        for boid in boids:
            if boid.position != self.position:
                if (boid.position - self.position).length() < range:
                    distance = distance - (boid.position - self.position)
        return distance
    
    # mai usata
    def tend_to_place(self,green_reached):
        if green_reached:
            dist = [self.position.distance_to(pg.Vector2(green_position)) for green_position in green_reached]
            if min(dist) < self.radius*3:
                best_position = green_reached[dist.index(min(dist))]
                updated_direction = best_position - self.position 
                return updated_direction
        else:
            return None
    
    def bound_position(self, margin=100):
        """
        Function to bound the boids to the screen. Change the velocity when they reach margin

        Parameters:
        -----------
        margin: int
            the margin of the screen
        """
        if self.position.x > self.width - margin:
            self.velocity += pg.Vector2(-0.7, 0)
        if self.position.x < margin:
            self.velocity += pg.Vector2(0.7, 0)
        if self.position.y > self.height - margin:
            self.velocity += pg.Vector2(0, -0.7)
        if self.position.y < margin:
            self.velocity += pg.Vector2(0, 0.7)

    
class GuardRules():

    def __init__(self, WIDTH, HEIGHT):

        self.width = WIDTH
        self.height = HEIGHT

    def find_neighbors(self, boids):
        """
        Function to find the neighbors of the boid

        Parameters:
        -----------
        boids: list
            list of boids

        Returns:
        --------
        list
            list of neighbors
        """
        neighbors = []
        for boid in boids:
            if boid.position != self.position:
                if self.position.distance_to(boid.position) < self.radius:
                    neighbors.append(boid)
        return neighbors
    
    def bound_position(self, margin=100):
        """
        Function to bound the boids to the screen. Change the velocity when they reach margin

        Parameters:
        -----------
        margin: int
            the margin of the screen
        """
        if self.position.x > self.width - margin:
            self.velocity += pg.Vector2(-0.7, 0)
        if self.position.x < margin:
            self.velocity += pg.Vector2(0.7, 0)
        if self.position.y > self.height - margin:
            self.velocity += pg.Vector2(0, -0.7)
        if self.position.y < margin:
            self.velocity += pg.Vector2(0, 0.7)
        
    def move_towards_target(self, target_position):
        """
        Function to move the boid towards the target

        Parameters:
        -----------
        target_position: pg.Vector2
            the position of the target

        Returns:
        --------
        pg.Vector2
            the updated velocity
        """
        # calculate the direction to the target
        direction = target_position - self.position
        if direction.length() != 0:
            direction = direction.normalize()
        
        # update the velocity
        speed_factor = 2
        self.velocity += direction * speed_factor

        # limit the speed of the boidguard
        max_speed = 5
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed

        