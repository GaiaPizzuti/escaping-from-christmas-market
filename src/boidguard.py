import pygame as pg
import random
from rules import GuardRules

class BoidGuard(GuardRules):

    def __init__(self, WIDTH, HEIGHT, MAP, GREEN, BLACK):

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

        # target color
        self.GREEN = GREEN

        # obstacle color
        self.BLACK = BLACK

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
        
        # check if the pixel is white
        while self.image.get_at((int(position.x), int(position.y))) != pg.Color('white'):
            position = pg.Vector2(random.randint(0, self.width - 1), random.randint(0, self.height - 1))
        return position
    
    def draw(self, screen):
        """
        draw the boid on the screen with a red circle of radius 4
        """
        pg.draw.circle(screen, 'blue', self.position, 5)
    
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
            check_position = self.position + direction.normalize() * self.radius

            if self.is_black(check_position):
                # invert the direction to avoid the obstacle
                avoidance_force += -direction
        
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
            return self.image.get_at((int(position.x), int(position.y))) == pg.Color(self.BLACK)
        return False

    def is_green(self):
        """
        Function to check if the pixel is green

        Returns:
        -------
        bool
            True if the pixel is green, False otherwise
        """
        return self.image.get_at((int(self.position.x), int(self.position.y))) == pg.Color(self.GREEN)
    
    def update(self, target_positions):
        """
        Functoon to update the position of the boidguard

        Parameters:
        ----------
        target_positions : list
            the list of the target positions
        
        Returns:
        -------
        pg.Vector2
            the new position of the boidguard
        """
        if not target_positions:
            return

        # find the closest target
        closest_target = min(target_positions, key=lambda pos: (self.position - pos).length())
        direction = closest_target - self.position
        if direction.length() != 0:
            direction = direction.normalize()

        # update the position of the boidguard
        speed_factor = 2
        self.velocity += direction * speed_factor

        # limit the speed of the boidguard
        if self.velocity.length() > 2:
            self.velocity.scale_to_length(2)
        
        #  check if there is a black pixel in the path of the boidguard
        if self.is_any_black(self.position + self.velocity):
            self.velocity += self.avoid_obstacles()

        self.position += self.velocity

        # wrap the position of the boid
        GuardRules.bound_position(self)

        # check if the boid has reached the target
        if self.is_green():
            self.reached = True
            return self.position