import yaml
import sys
import pygame as pg
import matplotlib.pyplot as plt

def find_target_positions(screen, target_color, WIDTH, HEIGHT):
    target_positions = []
    
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if screen.get_at((x, y)) == pg.Color(target_color):
                target_positions.append((x, y))
    #print(target_positions)
    return target_positions


def get_config():
   sys.path.append(".")
   
   with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

    WIDTH = config["image"]["width"]
    HEIGHT = config["image"]["height"]
    BORDER_COLOR = config["color"]["border"]
    OBJ_COLOR = config["color"]["target-hex"]
    MAP = config["image"]["path"]

    BOIDS = config["people"]["num"]
    BOIDGUARDS = round((config["security"]["percentage"] * BOIDS))

    ALIGNMENT = config["parameters"]["alignment"]
    COHESION = config["parameters"]["cohesion"]
    SEPARATION = config["parameters"]["separation"]
    
    return WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION

def plot_boids_data(time_log, boids_log, boidguards_log):
    plt.figure(figsize=(10, 6))
    plt.plot(time_log, boids_log, label="Boids", color="red", linewidth=2)
    plt.plot(time_log, boidguards_log, label="BoidGuards", color="blue", linewidth=2)
    plt.xlabel("Time (s)")
    plt.ylabel("Number")
    plt.title("Evolution of number of Boids and BoidGuards")
    plt.legend()
    plt.grid()
    plt.show()
