import pygame

from scripts.utils import normalize
from scripts.bullet import Bullet

class Entity:
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos

        self.hp = 10

        self.hp_max = self.hp

        self.color = (255,0,0)
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 10, 10)

    def render(self, screen, scroll):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.rect.x - scroll[0], self.rect.y - scroll[1], self.rect.width, self.rect.height))

class Player(Entity):
    def __init__(self, game, pos):
        super().__init__(game, pos)

        self.speed = 5
        self.damage = 1

    def move(self, movement):
        velocity = ((movement['right'] - movement['left']), (movement['down'] - movement['up']))

        velocity = normalize(velocity)

        self.rect.x += velocity[0] * self.speed
        self.rect.y += velocity[1] * self.speed



class Enemy(Entity):
    def __init__(self, game, pos):
        super().__init__(game, pos)

        self.speed = 3
        self.hp_max = 3
        self.hp = self.hp_max
        self.color = (0, 255, 0)

        
        self.health_bar = pygame.Rect(10, 10, self.rect.width, 3)
        self.health_bar_bg = pygame.Rect(10, 10, self.rect.width, 3)

    def follow_player(self, player, enemies):

        vector = normalize((player.rect.x - self.rect.x, player.rect.y - self.rect.y))


        self.rect.x += vector[0] * self.speed 

        for enemy in enemies:
            if enemy is not self:
                if self.rect.colliderect(enemy.rect):
                    if vector[0] > 0:
                        self.rect.right = enemy.rect.left
                    else:
                        self.rect.left = enemy.rect.right

        self.rect.y += vector[1] * self.speed 

        for enemy in enemies:
            if enemy is not self:
                if self.rect.colliderect(enemy.rect):
                    if vector[1] > 0:
                        self.rect.bottom = enemy.rect.top
                    else:
                        self.rect.top = enemy.rect.bottom

        if self.rect.colliderect(player.rect):
            player.hp = max(0, player.hp - 1)
            self.hp -= 1

        if self.hp <= 0:
            self.game.score += round(self.hp_max / 3)
            enemies.remove(self)

    def render(self, screen, scroll):
        super().render(screen, scroll)
        self.health_bar.topleft = (self.rect.x , self.rect.y - 5)
        self.health_bar_bg.topleft = (self.rect.x , self.rect.y - 5)
        self.health_bar.width = self.health_bar_bg.width * (self.hp / self.hp_max)

        pygame.draw.rect(screen, (40,40,40), pygame.Rect(self.health_bar_bg.topleft[0] - scroll[0], self.health_bar_bg.topleft[1] - scroll[1], self.health_bar_bg.width, self.health_bar_bg.height))
        pygame.draw.rect(screen, (255, 50, 25),  pygame.Rect(self.health_bar.topleft[0] - scroll[0], self.health_bar.topleft[1] - scroll[1], self.health_bar.width, self.health_bar_bg.height))


class MegaEnemy(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)

        print("I have spawn")

        self.speed = 1
        self.hp_max = 100
        self.hp = self.hp_max
        self.color = (0, 0, 255)

        self.rect.width = 25
        self.rect.height = 25

        self.health_bar = pygame.Rect(10, 10, self.rect.width, 3)
        self.health_bar_bg = pygame.Rect(10, 10, self.rect.width, 3)

class EnemyShooter(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)

        print("I have spawn haha")

        self.speed = 1
        self.hp_max = 100
        self.hp = self.hp_max
        self.color = (0, 0, 255)

        self.rect.width = 25
        self.rect.height = 25

        self.health_bar = pygame.Rect(10, 10, self.rect.width, 3)
        self.health_bar_bg = pygame.Rect(10, 10, self.rect.width, 3)

        self.shoot_cooldown = 0
        self.shoot_cooldown_max = 30

    def follow_player(self, player, enemies):
        super().follow_player(player, enemies)

        self.shoot_cooldown -= 1

        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_cooldown_max
            self.game.bullets.append(Bullet(self.game, self.rect.center, 1, normalize((self.game.player.rect.centerx - self.rect.centerx, self.game.player.rect.centery  - self.rect.centery)), self.game.player))

