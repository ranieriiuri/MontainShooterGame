#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY
from code.EnemyShot import EnemyShot
from code.Entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        self.blink_timer = 0 #Adicionando o contador p piscar

    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

    def take_damage(self, damage):
        self.health -= damage
        self.blink_timer = 10  # Define o tempo de piscamento quando tomar dano

    def render(self, screen):
        if self.blink_timer % 2 == 0:  # Alterna a visibilidade durante o piscamento
            screen.blit(self.surf, self.rect)
        if self.blink_timer > 0:
            self.blink_timer -= 1  # Decrementa o blink_timer