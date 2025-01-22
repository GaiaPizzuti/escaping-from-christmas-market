import yaml
import sys
import pygame as pg


def find_target_positions(screen, target_color):
    """
    Trova tutte le posizioni dei target (gruppi di pixel dello stesso colore) nella schermata.
    Restituisce una lista di vettori 2D che rappresentano i centri dei gruppi di target.

    :param screen: Schermata (superficie) in cui cercare i target
    :param target_color: Colore del target (tupla RGB)
    :return: Lista di vettori 2D con le posizioni dei target
    """
    target_positions = []
    visited = set()  # Per tenere traccia dei pixel già visitati

    def explore_group(x, y):
        # Funzione di esplorazione per un gruppo di pixel connessi
        pixels_to_check = [(x, y)]
        group_pixels = []

        while pixels_to_check:
            px, py = pixels_to_check.pop()
            if (px, py) not in visited and screen.get_at((px, py)) == target_color:
                visited.add((px, py))
                group_pixels.append((px, py))

                # Aggiungi i vicini (sinistra, destra, sopra, sotto)
                if px > 0:
                    pixels_to_check.append((px - 1, py))
                if px < screen.get_width() - 1:
                    pixels_to_check.append((px + 1, py))
                if py > 0:
                    pixels_to_check.append((px, py - 1))
                if py < screen.get_height() - 1:
                    pixels_to_check.append((px, py + 1))
                

        return group_pixels

    # Scansiona l'intera schermata alla ricerca di gruppi di target
    for y in range(screen.get_height()):
        for x in range(screen.get_width()):
            if (x, y) not in visited and screen.get_at((x, y)) == target_color:
                # Esplora il gruppo di pixel connessi
                group_pixels = explore_group(x, y)
                if group_pixels:
                    # Calcola il centro del gruppo di pixel
                    avg_x = sum(px for px, py in group_pixels) / len(group_pixels)
                    avg_y = sum(py for px, py in group_pixels) / len(group_pixels)
                    target_positions.append(pg.Vector2(avg_x, avg_y))

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
    BOIDGUARDS = config["security"]["nums"]

    ALIGNMENT = config["parameters"]["alignment"]
    COHESION = config["parameters"]["cohesion"]
    SEPARATION = config["parameters"]["separation"]
    
    return WIDTH, HEIGHT, BORDER_COLOR, OBJ_COLOR, MAP, BOIDS, BOIDGUARDS, ALIGNMENT, COHESION, SEPARATION
