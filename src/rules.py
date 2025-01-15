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
        