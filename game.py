import pygame
import math

from scripts.entities import Player, Enemy
from scripts.utils import normalize, draw_text
from scripts.bullet import Bullet
from scripts.spawner import spawn_enemy
from scripts.upgrades import Upgrades

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

        self.movement = {
            'right' : False,
            'left' : False,
            'up' : False,
            'down' : False,
        }

        self.shooting = False

        self.player = Player(self, (100,100))

        self.enemies = []

        self.spawn_rate = 60
        self.spawn_cooldown = 0 
        
        self.bullets = []
        self.bullet_cooldown = 0
        self.bullet_max_cooldown = 12

        self.score = 100

        self.scroll = [0, 0]

        self.in_menu = True

        self.health_bar = pygame.Rect(10, 10, 200, 10)
        self.health_bar_bg = pygame.Rect(10, 10, 200, 10)

        self.upgrades = Upgrades(self)
        self.number_of_upgrades = 0
        self.number_of_upgrades_used = 0

        pygame.font.init()


    def run(self):
        while self.in_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    self.in_menu = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.in_menu = False



            self.screen.fill((0,0,0))

            draw_text(self.screen, 'Press any button to start', pygame.font.Font(None, 22), (255,255,255), (400,300))

            self.clock.tick(60)

            pygame.display.flip()

        while self.player.hp > 0:
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])

            self.scroll[0] += (self.player.rect.centerx - self.scroll[0] - self.screen.get_width() / 2) / 20
            self.scroll[1] += (self.player.rect.centery - self.scroll[1] - self.screen.get_height() / 2) / 20


            self.spawn_cooldown -= 1

            if self.spawn_cooldown <= 0:
                print(self.player.rect.center)
                self.enemies.append(spawn_enemy(self, (self.player.rect.center), 500))
                self.spawn_cooldown = self.spawn_rate


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement['up'] = True
                    if event.key == pygame.K_DOWN:
                        self.movement['down'] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement['right'] = True
                    if event.key == pygame.K_LEFT:
                        self.movement['left'] = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement['up'] = False
                    if event.key == pygame.K_DOWN:
                        self.movement['down'] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement['right'] = False
                    if event.key == pygame.K_LEFT:
                        self.movement['left'] = False
                # hi
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.shooting = True
                    
                        if self.number_of_upgrades > 0:
                            self.upgrades.click(pygame.mouse.get_pos())
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    self.shooting = False

            self.bullet_cooldown -= 1

            if self.shooting and self.bullet_cooldown <= 0:
                self.bullets.append(Bullet(self, self.player.rect.center, self.player.damage, normalize((mpos[0] - self.player.rect.centerx, mpos[1] - self.player.rect.centery)), self.enemies))
                self.bullet_cooldown = self.bullet_max_cooldown

            self.screen.fill((0,0,0))

            for enemy in self.enemies:
                enemy.follow_player(self.player, self.enemies)
                enemy.render(self.screen, self.scroll)

            for bullet in self.bullets:
                bullet.render(self.screen, self.scroll)
                bullet.move()

            self.player.move(self.movement)
            self.player.render(self.screen, self.scroll)

            self.health_bar.width = self.health_bar_bg.width * (self.player.hp / self.player.hp_max)
            pygame.draw.rect(self.screen, (40,40,40), self.health_bar_bg)
            pygame.draw.rect(self.screen, (255, 50, 25), self.health_bar)

            draw_text(self.screen, str(self.score), pygame.font.Font(None, 42), (255,255,255), (400, 25))

            if math.floor(self.score / 10) > self.number_of_upgrades + self.number_of_upgrades_used:
                self.number_of_upgrades += 1
            
            if self.number_of_upgrades > 0:
                self.upgrades.render(self.screen)

            self.clock.tick(60)

            pygame.display.flip()

while True:
    Game().run()
