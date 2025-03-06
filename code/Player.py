#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame.key

from code.Const import ENTITY_SPEED, WIN_HEIGHT, WIN_WIDTH, PLAYER_KEY_UP, PLAYER_KEY_DOWN, PLAYER_KEY_LEFT, \
    PLAYER_KEY_RIGHT, PLAYER_KEY_SHOOT, ENTITY_SHOT_DELAY
from code.Entity import Entity
from code.PlayerShot import PlayerShot


class Player(Entity):
    def __init__(self, name: str, position: tuple):
        super().__init__(name, position)
        self.shot_delay = ENTITY_SHOT_DELAY[self.name]

    def move(self):
        pressed_key = pygame.key.get_pressed() #obtém todas as teclas pressionadas no momento

        #se a tecla pra cima do player em questão estiver pressionada e o topo da dimensão total do player for maior q 0 (garante estar dentro da tela definida), então move o player pra cima, diminuindo sua posição no eixo y (já q zero é em cima-esquerda da tela)
        if pressed_key[PLAYER_KEY_UP[self.name]] and self.rect.top > 0:
            self.rect.centery -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_DOWN[self.name]] and self.rect.bottom < WIN_HEIGHT:
            self.rect.centery += ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_LEFT[self.name]] and self.rect.left > 0:
            self.rect.centerx -= ENTITY_SPEED[self.name]
        if pressed_key[PLAYER_KEY_RIGHT[self.name]] and self.rect.right < WIN_WIDTH:
            self.rect.centerx += ENTITY_SPEED[self.name]
        pass

    #O proprio player é responsavel pela lógica do tiro. A classe 'PlayerShot' apenas representa o tiro (como entidade) e define q ele será disparado somente reto pera direita e na velocidade da entidade (player1shot, player2shot, enemy1shot ou enemy2shot)
    #Sempre q um player dispara é criado uma entidade 'PlayerShot', q dura até atingir um alvo ou chegar ao fim da tela e depois é destruída
    def shoot(self):
        self.shot_delay -= 1
        if self.shot_delay == 0:
            self.shot_delay = ENTITY_SHOT_DELAY[self.name]
            pressed_key = pygame.key.get_pressed()
            if pressed_key[PLAYER_KEY_SHOOT[self.name]]:
                return PlayerShot(name=f'{self.name}Shot', position=(self.rect.centerx, self.rect.centery))
            else:
                return None
        else:
            return None
