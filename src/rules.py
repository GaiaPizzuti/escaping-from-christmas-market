import pygame as pg

class Rules():

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

    # alignment, ants try to match the velocity of their neighbors
    def match_velocity(self, boids):
        velocity = pg.Vector2(0, 0)
        for ant in boids:
            velocity += ant.velocity
        if len(boids) > 1:
            velocity /= len(boids)
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