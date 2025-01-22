import pygame as pg

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
    def match_velocity(self, boids, boidguards, k = 0):
        velocity = pg.Vector2(0, 0)

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

    