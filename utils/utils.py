import yaml
import sys
import pygame as pg


def find_target_position(screen, target_color):
    target_position = None
    for y in range(screen.get_height()):
        for x in range(screen.get_width()):
            if screen.get_at((x, y)) == target_color:
                target_position = pg.Vector2(x, y)
                break
        if target_position:
            break
    return target_position

def get_config():
   sys.path.append(".")
   
   with open("utils/config.yaml", "r") as f:
    config = yaml.safe_load(f)

    WIDTH = config["image"]["width"]
    HEIGHT = config["image"]["height"]
    BORDER_COLOR = config["color"]["border"]
    OBJ_COLOR = config["color"]["target"]
    MAP = config["image"]["path"]

    BOIDS = config["people"]["num"]
    BOIDGUARDS = config["security"]["nums"]

    ALIGNMENT = config["parameters"]["alignment"]
    COHESION = config["parameters"]["cohesion"]
    SEPARATION = config["parameters"]["separation"]
    
    return WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION
