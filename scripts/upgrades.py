import pygame

import random

from scripts.utils import draw_text


class Upgrades:
    def __init__(self, game):
        self.game = game

        self.upgrade_screen = pygame.Surface((800,600), pygame.SRCALPHA)
        self.upgrade_screen.fill((0,0,0,0))

        self.upgrades = [
            GiveLife(game),
            GiveSpeed(game),
            GiveDamage(game),
        ]

        self.cards = [
            pygame.Rect(10, 150, 200, 300),
            pygame.Rect(250, 150, 200, 300),
            pygame.Rect(500, 150, 200, 300),
        ]

        self.actual_upgrades = []
        self.update_upgrades()

    def render(self, screen):
        for card in self.cards:
            pygame.draw.rect(self.upgrade_screen, (40, 40, 40, 120), card)
            draw_text(screen, self.actual_upgrades[self.cards.index(card)].upgrade_name, pygame.font.Font(None, 24), (255,255,255), (card.x + 100, 160))
            
        screen.blit(self.upgrade_screen, (0,0))

    def click(self, mpos):
        for card in self.cards:
            if card.collidepoint(mpos):
                self.actual_upgrades[self.cards.index(card)].power_up()
                self.update_upgrades()
                self.game.number_of_upgrades -= 1
                self.game.number_of_upgrades_used += 1

    def update_upgrades(self):
        self.actual_upgrades = []
        for i in range(3): self.actual_upgrades.append(self.upgrades[random.randint(0, len(self.upgrades) - 1)]) 


class Upgrade:
    def __init__(self, game, upgrade_name="", description=""):
        self.game = game 
        self.upgrade_name = upgrade_name
        self.description = description

    def power_up(self):
        pass

class GiveLife(Upgrade):
    def __init__(self, game, upgrade_name="Regain 1 hp", description="Regain 1 hp"):
        super().__init__(game, upgrade_name, description)

    def power_up(self):
        self.game.player.hp = min(self.game.player.hp_max, self.game.player.hp + 1)

class GiveSpeed(Upgrade):
    def __init__(self, game, upgrade_name="Increase speed", description="Increase speed by 1"):
        super().__init__(game, upgrade_name, description)

    def power_up(self):
        self.game.player.speed += 1

class GiveDamage(Upgrade):
    def __init__(self, game, upgrade_name="Increase damage", description="Increase damage by 0.5"):
        super().__init__(game, upgrade_name, description)

        if self.game.player.damage >= 2:
            self.description="Increase damage by 1"

    def power_up(self):
        if self.game.player.damage < 2:
            self.game.player.damage += .5
        else: 
            self.game.player.damage += 1
            print("max damage haha")
