#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pygame

from code.Const import ENTITY_SPEED, ENTITY_SHOT_DELAY, EXPLOSION_FRAMES, EXPLOSION_SOUND
from code.EnemyShot import EnemyShot
from code.Entity import Entity


class Enemy(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]
        #self.blink_timer = 0 #Adicionando o contador p piscar
        self.exploding = False
        self.explosion_frames = [pygame.image.load(img) for img in EXPLOSION_FRAMES]  # faz um laço q executa as 5 imagens q formam a explosão
        self.explosion_index = 0
        self.explosion_sound = pygame.mixer.Sound(EXPLOSION_SOUND)


    def move(self):
        self.rect.centerx -= ENTITY_SPEED[self.name]

    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            return EnemyShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))

    def take_damage(self, damage):
        self.health -= damage
        #self.blink_timer = 10  # Define o tempo de piscamento quando tomar dano
        if self.health <= 0:
            self.exploding = True
            self.explosion_sound.play()

    def render(self, screen):
        #if self.blink_timer % 2 == 0:  # Alterna a visibilidade durante o piscamento
        if self.exploding:
            if self.explosion_index < len(self.explosion_frames):
                screen.blit(self.explosion_frames[self.explosion_index], self.rect)
                self.explosion_index += 1  # Avança para o próximo frame da explosão
            else:
                self.health = -1  # Marca para ser removido
        else:
            screen.blit(self.surf, self.rect)
        #if self.blink_timer > 0:
        #    self.blink_timer -= 1  # Decrementa o blink_timer