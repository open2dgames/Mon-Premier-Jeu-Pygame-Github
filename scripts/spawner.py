import pygame 
import random
import math 

from scripts.entities import Enemy, MegaEnemy, EnemyShooter

def spawn_enemy(game, player_pos, radius):
    angle_degrees = random.random() * 360 

    angle_radians = math.radians(angle_degrees)

    spawn_point = (player_pos[0] + radius * math.cos(angle_radians), player_pos[1] + radius * math.sin(angle_radians))

    if game.score > 1:
        return EnemyShooter(game, spawn_point)
    
    return Enemy(game, spawn_point)