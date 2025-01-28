import pygame as pg
import numpy as np

class Rules():

    def __init__(self, WIDTH, HEIGHT):

        self.width = WIDTH
        self.height = HEIGHT


    # boid rules

    def find_neighbors(self, boids, boidguards):
        neighbors = []
        for boid in boids:
            if boid.position != self.position:
                if self.position.distance_to(boid.position) < self.radius:
                    neighbors.append(boid)

        for boidg in boidguards:
            if boidg.position != self.position:
                if self.position.distance_to(boidg.position) < self.radius:
                    neighbors.append(boidg)

        return neighbors

    def find_neighbors_boidguards(self,boidguards):
        neighborsguard = []
        for boidg in boidguards:
            if boidg.position != self.position:
                if self.position.distance_to(boidg.position) < self.radius:
                    neighborsguard.append(boidg)
        return neighborsguard
    
    # alignment, ants try to match the velocity of their neighbors
    def match_velocity(self, boids, boidguards):
        velocity = pg.Vector2(0, 0)
        k = self.discipline

        for boid in boids:
            velocity += boid.velocity
        for guards in boidguards:
            velocity += guards.velocity*k
        if len(boids) > 1:
            velocity /= (len(boids) + len(boidguards)*k)
            return (velocity - self.velocity) / 8
        return pg.Vector2(0, 0)
    
    # cohesion, boids try to fly towards the center of mass of neighboring boids
    def fly_towards_center(self, boids):
        center = pg.Vector2(0, 0)
        for boid in boids:
            if boid.position != self.position:
                center += boid.position
            return (center - self.position) / 100
        return pg.Vector2(0, 0)

    # separation, boids try to keep a small distance away from other objects (boids, obstacles)
    def keep_distance_away(self, boids, range=9):
        distance = pg.Vector2()
        for boid in boids:
            if boid.position != self.position:
                if (boid.position - self.position).length() < range:
                    distance = distance - (boid.position - self.position)
        return distance
    
    def tend_to_place(self,green_reached,step_size=10):
        if green_reached:
            dist = [self.position.distance_to(pg.Vector2(green_position)) for green_position in green_reached]
            if min(dist) < self.radius*8:
                best_position = green_reached[dist.index(min(dist))]
                updated_direction = best_position - self.position 
                print(f"Adjusting velocity towards desired_position {best_position}, from vector: {green_reached}")
                return updated_direction
        else:
            return None
    
    # bound the boids to the screen. Change the velocity when they reach margin
    def bound_position(self, margin=100):
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

    # ant rules

    def find_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid.position != self.position:
                if self.position.distance_to(boid.position) < self.radius:
                    neighbors.append(boid)
        return neighbors
    
    # cohesion, boids try to fly towards the center of mass of neighboring boids
    def fly_towards_center(self, boids):
        center = pg.Vector2(0, 0)
        for boid in boids:
            if boid.position != self.position:
                center += boid.position
            return (center - self.position) / 100
        return pg.Vector2(0, 0)

    # separation, boids try to keep a small distance away from other objects (boids, obstacles)
    def keep_distance_away(self, boids, range=9):
        distance = pg.Vector2()
        for boid in boids:
            if boid.position != self.position:
                if (boid.position - self.position).length() < range:
                    distance = distance - (boid.position - self.position)
        return distance
    
    # bound the boids to the screen. Change the velocity when they reach margin
    def bound_position(self, margin=100):
        if self.position.x > self.width - margin:
            self.velocity += pg.Vector2(-0.7, 0)
        if self.position.x < margin:
            self.velocity += pg.Vector2(0.7, 0)
        if self.position.y > self.height - margin:
            self.velocity += pg.Vector2(0, -0.7)
        if self.position.y < margin:
            self.velocity += pg.Vector2(0, 0.7)
        
    def move_towards_target(self, target_position):
        # Calcola la direzione verso il target
        direction = target_position - self.position
        
        # Normalizza la direzione per ottenere un vettore unitario
        if direction.length() != 0:
            direction = direction.normalize()
        
        # Aggiorna la velocità, scalata da un fattore di velocità
        speed_factor = 2  # Velocità di movimento del Boid Guard
        self.velocity += direction * speed_factor

        # Limita la velocità per evitare movimenti eccessivi
        max_speed = 5
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed

        