from code.Const import WIN_WIDTH
from code.Enemy import Enemy
from code.EnemyShot import EnemyShot
from code.Entity import Entity
from code.Player import Player
from code.PlayerShot import PlayerShot


class EntityMediator:

    @staticmethod
    def __verify_collision_window(ent: Entity):
        if isinstance(ent, Enemy):
            if ent.rect.right <= 0:
                ent.health = 0
        if isinstance(ent, PlayerShot):
            if ent.rect.left >= WIN_WIDTH:
                ent.health = 0
        if isinstance(ent, EnemyShot):
            if ent.rect.right <= 0:
                ent.health = 0

    @staticmethod
    def __verify_collision_entity(ent1, ent2):
        valid_interaction = False
        if isinstance(ent1, Enemy) and isinstance(ent2, PlayerShot):
            valid_interaction = True
        elif isinstance(ent1, PlayerShot) and isinstance(ent2, Enemy):
            valid_interaction = True
        elif isinstance(ent1, Player) and isinstance(ent2, EnemyShot):
            valid_interaction = True
        elif isinstance(ent1, EnemyShot) and isinstance(ent2, Player):
            valid_interaction = True

        #aqui aplica-se os danos usando a lógica das 4 perguntas básicas q devem responder sim para haver dano: "Se a borda dir da ent1 estiver depois ou igual a borda esq da ent2, a esq da ent1 antes da dir da ent2, a borda de baixo da ent1 acima da borda superior da ent2 e a de cima da ent1 estiver abaixo da ent2", se todas as perguntas tiverem resposta sim, há colisão, então há dano contabilizado no atributo 'damage' q diminui a vida da ent
        if valid_interaction:  # if valid_interaction == True:
            if (ent1.rect.right >= ent2.rect.left and
                    ent1.rect.left <= ent2.rect.right and
                    ent1.rect.bottom >= ent2.rect.top and
                    ent1.rect.top <= ent2.rect.bottom):
                #ent1.health -= ent2.damage <-- forma antiga
                ent1.take_damage(ent2.damage)  # Aqui chama o take_damage do jogador
                ent2.health -= ent1.damage
                ent1.last_dmg = ent2.name
                ent2.last_dmg = ent1.name

    #o score à ent player1 ou 2 vem quando o atributo 'last_dmg' da ent enemy é preenchido
    @staticmethod
    def __give_score(enemy: Enemy, entity_list: list[Entity]):
        if enemy.last_dmg == 'Player1Shot':
            for ent in entity_list:
                if ent.name == 'Player1':
                    ent.score += enemy.score
        elif enemy.last_dmg == 'Player2Shot':
            for ent in entity_list:
                if ent.name == 'Player2':
                    ent.score += enemy.score

#esse metodo é o que de fato define um comportamento para casos de colisão das entidades com a borda da janela definida e tbm verifica colisão de todas as entidades entre si (inclusive das entidades tiros com as outras), chamando os metodos de colisão para janelas e entities definidos acima em um loop onde passa as entidades de cada iteração como param
    @staticmethod
    def verify_collision(entity_list: list[Entity]):
        for i in range(len(entity_list)):
            entity1 = entity_list[i]
            EntityMediator.__verify_collision_window(entity1)
            for j in range(i + 1, len(entity_list)):
                entity2 = entity_list[j]
                EntityMediator.__verify_collision_entity(entity1, entity2)

    @staticmethod
    def verify_health(entity_list: list[Entity]):
        for ent in entity_list:
            if ent.health <= 0:
                if isinstance(ent, Enemy):
                    EntityMediator.__give_score(ent, entity_list)
                entity_list.remove(ent)

            # Se o player ou o inimigo estiverem com vida e a contagem do piscar for maior que zero, diminui o tempo do piscar em cada iteração do numero setado pelo take_damage até zerar (qnd para de piscar)
            if isinstance(ent, (Player, Enemy)) and ent.blink_timer > 0:
                 ent.blink_timer -= 1  # Diminui o contador do piscar