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
        """
        Aggiorna la velocità e la posizione del Boid Guard per muoversi verso il target più vicino.

        :param boidguards: Lista di altri Boid Guards (non utilizzata in questa versione)
        :param target_positions: Lista delle posizioni dei target (vetrici 2D)
        """
        if not target_positions:
            print("No target found")
            return  # Esci dalla funzione se non ci sono target

        # Trova il target più vicino
        closest_target = min(target_positions, key=lambda pos: (self.position - pos).length())

        # Calcola la direzione verso il target più vicino
        direction = closest_target - self.position

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

        # Limita la velocità
        self.velocity.scale_to_length(5)

        # Aggiorna la posizione
        self.position += self.velocity

        # wrap the position of the boidù
        GuardRules.bound_position(self)


        if self.is_green(self.position):
            self.reached = True
            self.velocity = pg.Vector2(0, 0)