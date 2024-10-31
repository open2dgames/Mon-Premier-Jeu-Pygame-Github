import pygame

class Bullet:
    def __init__(self, game, pos, damage, target_vel, targets):
        self.game = game

        self.bullets = self.game.bullets

        self.targets = targets
        
        self.x = pos[0]
        self.y = pos[1]

        self.damage = damage

        self.speed = 6

        self.target_vel = target_vel

        self.lifetime = 0
        self.max_lifetime = 90 

    def render(self, screen, scroll):
        pygame.draw.circle(screen, (255,255,255), (self.x - scroll[0], self.y - scroll[1]), 2)

    def move(self):
        self.x += self.target_vel[0] * self.speed
        self.y += self.target_vel[1] * self.speed

        if isinstance(self.targets, list):
            for target in self.targets:
                if target.rect.collidepoint((self.x, self.y)):
                    target.hp -= self.damage
                    self.bullets.remove(self)
        else:
            if self.targets.rect.collidepoint((self.x, self.y)):
                self.targets.hp -= self.damage
                self.bullets.remove(self)
                    
        self.lifetime += 1 

        if self.lifetime >= self.max_lifetime:
            self.bullets.remove(self)