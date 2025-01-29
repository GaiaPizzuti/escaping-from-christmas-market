import yaml
import sys
import pygame as pg
import matplotlib.pyplot as plt

def find_target_positions(screen, target_color, WIDTH, HEIGHT):
    """
    Function to find the target positions in the image

    Parameters:
    -----------
    screen: pygame.Surface
        pygame screen object
    target_color: str
        color of the target
    WIDTH: int
        width of the image
    HEIGHT: int
        height of the image

    Returns:
    --------
    target_positions: list
        list of tuples containing the positions of the targets
    """
    target_positions = []
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if screen.get_at((x, y)) == pg.Color(target_color):
                target_positions.append((x, y))
    return target_positions


def get_config():
   """
   Function to get the configuration from the config.yaml file

    Returns:
    --------
    WIDTH: int
        width of the image
    HEIGHT: int
        height of the image
    BORDER_COLOR: str
        color of the border
    OBJ_COLOR: str
        color of the target
    MAP: str
        path to the image
    BOIDS: int
        number of boids
    BOIDGUARDS: int
        number of boidguards
    ALIGNMENT: float
        alignment parameter
    COHESION: float
        cohesion parameter
    SEPARATION: float
        separation parameter
   """
   sys.path.append(".")
   
   with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

    WIDTH = config["image"]["width"]
    HEIGHT = config["image"]["height"]
    BORDER_COLOR = config["color"]["border-hex"]
    OBJ_COLOR = config["color"]["target-hex"]
    MAP = config["image"]["path"]

    BOIDS = config["people"]["num"]
    BOIDGUARDS = round((config["security"]["percentage"] * BOIDS))

    ALIGNMENT = config["parameters"]["alignment"]
    COHESION = config["parameters"]["cohesion"]
    SEPARATION = config["parameters"]["separation"]
    
    return WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION

def plot_boids_data(time_log, boids_log, boidguards_log):
    """
    Function to plot the number of Boids and BoidGuards over time

    Parameters:
    -----------
    time_log: list
        list of time values
    boids_log: list
        list of boids values
    boidguards_log: list
        list of boidguards values
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time_log, boids_log, label="Boids", color="red", linewidth=2)
    plt.plot(time_log, boidguards_log, label="BoidGuards", color="blue", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Number")
    plt.title("Evolution of number of Boids and BoidGuards")
    plt.legend()
    plt.grid()
    plt.show()